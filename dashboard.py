from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Prediction
from extensions import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Get the 10 most recent predictions for the current user
    recent_predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.date.desc()).limit(10).all()

    # --- Analytics Data Aggregation ---
    from sqlalchemy import func
    import json
    import re
    def extract_price(price_str):
        match = re.search(r'\d+(\.\d+)?', price_str)
        return float(match.group()) if match else 0.0

    # 1. Predictions per day
    predictions_per_day = (
        db.session.query(
            func.date(Prediction.date),
            func.count()
        )
        .filter(Prediction.user_id == current_user.id)
        .group_by(func.date(Prediction.date))
        .order_by(func.date(Prediction.date))
        .all()
    )
    dates, counts = zip(*predictions_per_day) if predictions_per_day else ([], [])

    # 2. Average predicted price per day
    avg_price_per_day = (
        db.session.query(
            func.date(Prediction.date),
            func.avg(Prediction.predicted_price)
        )
        .filter(Prediction.user_id == current_user.id)
        .group_by(func.date(Prediction.date))
        .order_by(func.date(Prediction.date))
        .all()
    )
    avg_dates, avg_prices = zip(*avg_price_per_day) if avg_price_per_day else ([], [])

    # 3. Most predicted brands
    brands = (
        db.session.query(
            Prediction.brand,
            func.count()
        )
        .filter(Prediction.user_id == current_user.id)
        .group_by(Prediction.brand)
        .order_by(func.count().desc())
        .limit(10)
        .all()
    )
    brand_names, brand_counts = zip(*brands) if brands else ([], [])

    # 4. Distribution of predicted prices (extract float from string)
    prices = [extract_price(p.predicted_price) for p in Prediction.query.filter_by(user_id=current_user.id).all() if p.predicted_price]

    # 5. Fuel type breakdown
    fuel_types = (
        db.session.query(
            Prediction.type,
            func.count()
        )
        .filter(Prediction.user_id == current_user.id)
        .group_by(Prediction.type)
        .all()
    )
    fuel_labels, fuel_counts = zip(*fuel_types) if fuel_types else ([], [])

    return render_template(
        'insights.html',
        user=current_user,
        recent_predictions=recent_predictions,
        dates=json.dumps(list(dates)),
        counts=json.dumps(list(counts)),
        avg_dates=json.dumps(list(avg_dates)),
        avg_prices=json.dumps(list(avg_prices)),
        brand_names=json.dumps(list(brand_names)),
        brand_counts=json.dumps(list(brand_counts)),
        prices=json.dumps(prices),
        fuel_labels=json.dumps(list(fuel_labels)),
        fuel_counts=json.dumps(list(fuel_counts)),
    )

@dashboard_bp.route('/delete_prediction/<int:prediction_id>', methods=['POST'])
@login_required
def delete_prediction(prediction_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    if prediction.user_id != current_user.id:
        flash('You are not authorized to delete this prediction.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    db.session.delete(prediction)
    db.session.commit()
    flash('Prediction deleted successfully.', 'success')
    return redirect(url_for('dashboard.dashboard')) 