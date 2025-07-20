from flask import Flask, render_template, request, redirect, url_for, flash
import util
from datetime import datetime
from extensions import db
from models import User, Prediction
from flask_login import LoginManager, current_user, login_required
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect
from auth import auth, google_bp
from dashboard import dashboard_bp
from werkzeug.utils import secure_filename
import os
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Flask-Mail config (replace with your SMTP server details)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'shashindhieravishka@gmail.com'  # replace with your email
app.config['MAIL_PASSWORD'] = 'irtsuomzzsgbhixm'   # replace with your email password or app password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'  # replace with your email

# Initialize extensions
bcrypt = Bcrypt(app)
db.init_app(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
mail = Mail(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard_bp)
app.register_blueprint(google_bp, url_prefix="/google_login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def root():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('auth.login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

@app.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
    vehicle = util.get_vehicles()
    return render_template('prediction.html', user=current_user, vehicle=vehicle)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            current_user.username = username
        # Handle profile picture upload
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_folder = os.path.join('static', 'profile_pics')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                current_user.profile_pic = f'profile_pics/{filename}'
        try:
            db.session.commit()
            flash('Profile updated!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'danger')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=current_user)

@app.route("/estimatedResult", methods = ["POST"])
def estimatedResult():
    try:
        # Get form data
        year = int(request.form["year"])
        present_price = float(request.form["show_room_price"])
        kms = int(request.form["kilometers"])
        vehicle = request.form["vehicle"]
        owner_str = request.form["owner"]
        fuel = request.form["fuel"].lower()  # Convert to lowercase
        seller = request.form["seller"].lower()  # Convert to lowercase
        transmission = request.form["transmission"].lower()  # Convert to lowercase

        # Convert owner string to integer
        owner_mapping = {
            "First": 0,
            "Second": 1, 
            "Third": 2,
            "Fourth & Above": 3
        }
        owner = owner_mapping.get(owner_str, 0)

        # Initialize feature variables
        diesel = 0
        petrol = 0
        individual = 0
        manual = 0

        # Calculate years since manufacture
        year_since_manufacture = datetime.now().year - year

        # Set fuel type flags
        if fuel == "diesel":
            diesel = 1
        elif fuel == "petrol":
            petrol = 1

        # Set seller type flag
        if seller == "individual":
            individual = 1

        # Set transmission flag
        if transmission == "manual":
            manual = 1

        # Validate inputs
        if year_since_manufacture < 0 or present_price <= 0 or kms < 0:
            return "Invalid input values! Please check your data."

        result = util.predict_price(year_since_manufacture, present_price, kms, owner, diesel, petrol, individual, manual, vehicle)

        if result == 1:
            return "Something is wrong please fill proper input!!"
        else:
            estimated_price = str(round(float(result), 2)) + " lakh rupees"

            # Save prediction to database for current user
            if current_user.is_authenticated:
                prediction = Prediction(
                    user_id=current_user.id,
                    type="Car",  # or "Bike" if you have logic to distinguish
                    brand=vehicle.split()[0] if vehicle else "",
                    model=vehicle,
                    mileage=str(kms),
                    predicted_price=estimated_price,
                    date=datetime.utcnow()
                )
                db.session.add(prediction)
                db.session.commit()
            
            # Redirect to results page with all data
            return redirect(url_for('results', 
                result=estimated_price,
                vehicle=vehicle,
                year=year,
                showroom_price=present_price,
                kilometers=kms,
                owner=owner_str,
                fuel=request.form["fuel"],
                seller=request.form["seller"],
                transmission=request.form["transmission"]
            ))
            
    except ValueError as e:
        return "Please fill all fields with valid values!"
    except Exception as e:
        return "Something is wrong please fill proper input!!"

@app.route("/results")
def results():
    # Get data from URL parameters
    result = request.args.get('result', 'N/A')
    vehicle = request.args.get('vehicle', 'N/A')
    year = request.args.get('year', 'N/A')
    showroom_price = request.args.get('showroom_price', 'N/A')
    kilometers = request.args.get('kilometers', 'N/A')
    owner = request.args.get('owner', 'N/A')
    fuel = request.args.get('fuel', 'N/A')
    seller = request.args.get('seller', 'N/A')
    transmission = request.args.get('transmission', 'N/A')
    
    return render_template("result.html", 
        result=result,
        vehicle=vehicle,
        year=year,
        showroom_price=showroom_price,
        kilometers=kilometers,
        owner=owner,
        fuel=fuel,
        seller=seller,
        transmission=transmission
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5022, debug=True)