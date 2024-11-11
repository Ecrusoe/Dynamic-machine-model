from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Eğitilen modeli yükle
model = joblib.load('user_input_model (1).pkl')

# Makine öğrenmesi ile tahmin yapma fonksiyonu
def makine_ogrenmesi_tahmin(temp, low_threshold, high_threshold):
    # Modelin tahmini
    predicted_action = model.predict([[temp, low_threshold, high_threshold]])[0]
    
    # Tahmini aksiyonun ne olduğunu belirleme
    if predicted_action == 0:
        return "Motor dursun"
    elif predicted_action == 1:
        return "Motor çalışsın"
    else:
        return "Servo motor çalışsın"

@app.route('/')
def index():
    return render_template('webb.html', result="Henüz bir sonuç yok")

@app.route('/predict', methods=['POST'])
def predict():
    # Kullanıcıdan gelen verileri al
    temp = float(request.form['temp'])
    low_threshold = float(request.form['low_threshold'])
    high_threshold = float(request.form['high_threshold'])

    # Makine öğrenmesi modeliyle tahmin yap
    result = makine_ogrenmesi_tahmin(temp, low_threshold, high_threshold)

    # Tahmin sonucunu web sayfasında göster
    return render_template('webb.html', result=f"Tahmin Sonucu: {result}")

if __name__ == '__main__':
    app.run(debug=True)
