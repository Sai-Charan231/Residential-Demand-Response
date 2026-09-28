+from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3
import numpy as np
import joblib
import re
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a secure random key in production

DATABASE = 'database.db'

# -----------------------------------
# Database connection helpers
# -----------------------------------
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# -----------------------------------
# Load ML models and scaler
# -----------------------------------
scaler = joblib.load('scaler.pkl')
model_rf = joblib.load('model_random_forest.pkl')
model_lgbm = joblib.load('model_lightgbm.pkl')
model_mlp = joblib.load('model_mlp_ann.pkl')
X_test = joblib.load('X_test.pkl')
y_test = joblib.load('y_test.pkl')

input_features = [
    "OutdoorTemperature", "IndoorTemperature", "ACSetpoint", "DesiredTemperature",
    "ElectricityPrice", "ShiftableLoad", "NonShiftableLoad",
    "MiscLoad", "ACPower", "TotalDemand"
]

def get_metrics(model, X, y):
    preds = model.predict(X)
    mse = mean_squared_error(y, preds)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, preds)
    r2 = r2_score(y, preds)
    return {"MSE": round(mse, 5), "RMSE": round(rmse, 5),
            "MAE": round(mae, 5), "R2": round(r2, 5)}

# -----------------------------------
# Routes
# -----------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        if not username or not email or not password:
            flash('Please fill out all fields!', 'warning')
            return render_template('signup.html')

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'danger')
            return render_template('signup.html')

        db = get_db()
        cursor = db.execute('SELECT * FROM users WHERE username = ?', (username,))
        account = cursor.fetchone()

        if account:
            flash('Username already exists!', 'danger')
            return render_template('signup.html')

        hashed_pw = generate_password_hash(password)
        db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                   (username, email, hashed_pw))
        db.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        db = get_db()
        cursor = db.execute('SELECT * FROM users WHERE username = ?', (username,))
        account = cursor.fetchone()

        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password!', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if not session.get('loggedin'):
        flash('Please log in to use prediction features.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            values = [float(request.form[f]) for f in input_features]
            arr = np.array(values).reshape(1, -1)
            arr_scaled = scaler.transform(arr)

            pred_rf = model_rf.predict(arr_scaled)[0]
            pred_lgbm = model_lgbm.predict(arr_scaled)[0]
            pred_mlp = model_mlp.predict(arr_scaled)[0]

            return render_template('result.html',
                                   input=request.form,
                                   pred_rf=pred_rf,
                                   pred_lgbm=pred_lgbm,
                                   pred_mlp=pred_mlp)
        except Exception as e:
            flash(f"Error during prediction: {str(e)}", 'danger')

    return render_template('predict.html', features=input_features)

@app.route('/metrics')
def metrics():
    try:
        m_rf = get_metrics(model_rf, X_test, y_test)
        m_lgbm = get_metrics(model_lgbm, X_test, y_test)
        m_mlp = get_metrics(model_mlp, X_test, y_test)
        return render_template('metrics.html', metrics={
            'Random Forest': m_rf, 'LightGBM': m_lgbm, 'MLP-ANN': m_mlp
        })
    except Exception as e:
        flash(f"Error calculating metrics: {str(e)}", 'danger')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
