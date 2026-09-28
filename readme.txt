Occupancy Prediction Flask App
Overview
This Flask web application predicts residential occupancy based on sensor input data using machine learning models (Random Forest, LightGBM, and MLP-ANN). It supports user signup, login with secure password hashing, and displays model performance metrics. SQLite is used as a lightweight database backend.

Features
User registration and login with session management

Secure password hashing using Werkzeug

Input forms for occupancy prediction

Display of model metrics (MSE, RMSE, MAE, R2)

Integration of pretrained ML models and scaler

Requirements
Python 3.10 or 3.11

Flask==2.3.2

numpy==1.25.0

scikit-learn==1.3.0

joblib==1.2.0

Werkzeug==2.3.7

Setup Instructions
Clone or download the project folder containing app.py, bd.py, schema.sql, the templates directory, and model files (scaler.pkl etc.).

Create and activate a Python virtual environment (recommended):

bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows CMD
Install dependencies:

bash
pip install -r requirements.txt
Initialize the SQLite database (run once):

bash
python bd.py
This creates database.db with the necessary users table.

Start the Flask app:

bash
python app.py
Open your browser and navigate to:
http://127.0.0.1:5000/

Using the Application
Register a new user via the “Sign Up” page.

Log in with your credentials.

Access the prediction page to input sensor values.

View model performance on the metrics page.

Log out when finished.

Troubleshooting
ModuleNotFoundError: Ensure all dependencies are installed in the active environment.

Database errors: Make sure bd.py has been run successfully and database.db exists.

Python version: Use Python 3.10+ for compatibility with current dependencies.

Model loading errors: Confirm model files (scaler.pkl, etc.) exist in the project root.

Secret key: Change app.secret_key in app.py to a strong, unique string in production.

Project Structure
text
/occupancy_app/
├── app.py
├── bd.py
├── database.db
├── schema.sql
├── scaler.pkl
├── model_random_forest.pkl
├── model_lightgbm.pkl
├── model_mlp_ann.pkl
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── predict.html
│   ├── metrics.html
│   └── result.html
├── requirements.txt
└── README.txt