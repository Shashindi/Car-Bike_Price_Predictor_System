# Car Price Prediction Web Application

A Flask-based web application that predicts car selling prices using machine learning. The application allows users to input vehicle details and get an estimated selling price.

## Features

- **Vehicle Selection**: Choose from a wide range of vehicles (cars, bikes, scooters)
- **Dynamic Image Display**: Shows vehicle images when selected
- **Comprehensive Input Form**: 
  - Year of manufacture
  - Show room price
  - Kilometers driven
  - Owner type (First, Second, Third, Fourth & Above)
  - Fuel type (Petrol, Diesel, CNG, LPG)
  - Seller type (Dealer, Individual)
  - Transmission (Manual, Automatic)
- **Real-time Price Prediction**: Instant price estimation in lakh rupees
- **Responsive Design**: Works on desktop and mobile devices
- **Form Validation**: Ensures all required fields are filled correctly

## Project Structure

```
Car Price Predictor/
├── app.py                 # Main Flask application
├── util.py               # Utility functions for ML model
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── artifacts/           # ML model files
│   ├── model.pkl       # Trained machine learning model
│   └── columns.json    # Feature column definitions
├── static/             # Static files (CSS, JS, images)
│   ├── car_price_prediction.jpg
│   ├── car.ico
│   ├── car.png
│   └── vehicle images/ # Vehicle images
└── templates/          # HTML templates
    └── carprice.html   # Main application page
```

## Installation

1. **Clone or download the project** to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5001
   ```

## How to Use

1. **Select a Vehicle**: Choose from the dropdown menu
2. **Fill in Details**:
   - Enter the year of manufacture (1900-2024)
   - Input the show room price in rupees
   - Specify kilometers driven
   - Select owner type (First/Second/Third/Fourth & Above)
   - Choose fuel type (Petrol/Diesel/CNG/LPG)
   - Pick seller type (Dealer/Individual)
   - Select transmission (Manual/Automatic)
3. **Click "Estimate Price"** to get the predicted selling price
4. **View Result**: The estimated price will appear in lakh rupees

## Technical Details

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 4
- **Machine Learning**: Scikit-learn with Random Forest model
- **Data Processing**: NumPy, Pandas
- **Model Storage**: Pickle format
- **Feature Engineering**: One-hot encoding for categorical variables

## Model Information

The machine learning model is trained on Indian car market data and predicts prices in lakh rupees. The model considers:

- **Numerical Features**: Year, show room price, kilometers driven, owner number
- **Categorical Features**: Fuel type, seller type, transmission, vehicle model
- **Output**: Predicted selling price in lakh rupees

## Troubleshooting

### Common Issues:

1. **Port already in use**: Change the port in `app.py` line 53
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Model not found**: Ensure `artifacts/model.pkl` exists
4. **Images not loading**: Check if `static/vehicle images/` folder contains vehicle images

### Error Messages:

- "Please fill all fields with valid values!" - Complete all form fields
- "Invalid input values!" - Check your input ranges
- "Something is wrong please fill proper input!!" - Verify all data is correct

## Development

To modify the application:

1. **Add new vehicles**: Update the model training data and retrain
2. **Change styling**: Modify CSS in `templates/carprice.html`
3. **Add features**: Extend `app.py` and `util.py`
4. **Update model**: Retrain with new data and replace `artifacts/model.pkl`

## Credits

- **Developer**: jaysoftic
- **GitHub**: https://github.com/jaysoftic
- **LinkedIn**: https://www.linkedin.com/in/jaysoftic/

## License

This project is for educational and demonstration purposes. 