from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Memuat kembali model dan scaler yang telah digenerate sebelumnya
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

model_names = ["Decision Tree"]

@app.route('/')
def index():
    return render_template('index.html', model_names=model_names, prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Menangkap data parameter kesehatan dari form interface
        input_data = {
            'Pregnancies': float(request.form['Pregnancies']),
            'Glucose': float(request.form['Glucose']),
            'BloodPressure': float(request.form['BloodPressure']),
            'SkinThickness': float(request.form['SkinThickness']),
            'Insulin': float(request.form['Insulin']),
            'BMI': float(request.form['BMI']),
            'DiabetesPedigreeFunction': float(request.form['DiabetesPedigreeFunction']),
            'Age': float(request.form['Age'])
        }
        
        # Konversi dict ke DataFrame agar sesuai format input scaler
        df_input = pd.DataFrame([input_data])
        
        # Transformasi fitur menggunakan scaler asli
        df_scaled = scaler.transform(df_input)
        
        # Eksekusi prediksi dengan model
        pred = model.predict(df_scaled)[0]
        
        # Konversi output biner (0/1) menjadi teks hasil diagnosis
        prediction_result = "Diabetic" if pred == 1 else "Non-Diabetic"
        
        return render_template('index.html', model_names=model_names, prediction=prediction_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)