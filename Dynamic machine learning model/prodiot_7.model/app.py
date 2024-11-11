from flask import Flask, request, jsonify
import numpy as np
from keras.models import load_model
import os

app = Flask(__name__)

# Modeli yükleme (model daha önce kaydedilmiş olmalı)
MODEL_PATH = 'device_control_model.h5'

# Modeli yükleyen fonksiyon
def load_trained_model():
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print("Model yüklendi.")
        return model
    else:
        print("Model bulunamadı!")
        return None

# Modeli sadece bir kez yükleme
model = load_trained_model()

# Ana sayfa
@app.route('/')
def index():
    return "Sensör verilerini almak ve cihazları kontrol etmek için API kullanabilirsiniz."

# Sensör verilerini ve cihaz ayarlarını alacak API
@app.route('/control', methods=['POST'])
def control_device():
    if not model:
        return jsonify({'error': 'Model bulunamadı! Lütfen önce modeli eğitin.'}), 500

    # Kullanıcıdan gelen verileri al
    data = request.json

    # Sensör verilerini alıyoruz (nem, sıcaklık, ışık vb.)
    humidity = data.get('humidity')
    temperature = data.get('temperature')
    light = data.get('light')

    # Sensör verilerini bir numpy array'e çevir
    sensor_data = np.array([[humidity, temperature, light]])

    # Model ile tahmin yap
    predictions = model.predict(sensor_data)

    # Çıkış verileri (Motor durumu, Servo açısı, LED durumu)
    motor_status = predictions[0][0]
    servo_angle = predictions[1][0]
    led_status = predictions[2][0]

    # Tahmin edilen sonuçları döndür
    return jsonify({
        'motor_status': int(motor_status > 0.5),  # Motor aç/kapat
        'servo_angle': float(servo_angle),  # Servo motor açısı
        'led_status': int(led_status > 0.5)  # LED aç/kapat
    })

if __name__ == '__main__':
    app.run(debug=True)
