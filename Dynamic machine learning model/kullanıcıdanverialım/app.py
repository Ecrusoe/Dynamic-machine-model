from flask import Flask, request, render_template
import numpy as np
from dynamic_model import DynamicModel

app = Flask(__name__)

# Modeli başlat
dynamic_model = DynamicModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train():
    min_value = int(request.form['min_value'])
    max_value = int(request.form['max_value'])
    sensor_value = int(request.form['sensor_value'])
    label = int(request.form['label'])  # Kullanıcı cihazın çalışmasını mı istedi? 1: Çalışıyor, 0: Kapalı

    # Yeni veri ekleyip modeli güncelle
    dynamic_model.update_model([sensor_value, min_value, max_value], label)
    dynamic_model.save_model()  # Modeli kaydet

    return "Model başarıyla güncellendi."

@app.route('/predict', methods=['POST'])
def predict():
    sensor_value = int(request.form['sensor_value'])
    min_value = int(request.form['min_value'])
    max_value = int(request.form['max_value'])

    # Tahmin yapma
    prediction = dynamic_model.predict([sensor_value, min_value, max_value])
    
    if prediction is not None:
        status = "Çalışıyor" if prediction == 1 else "Kapalı"
    else:
        status = "Model henüz eğitilmedi"

    return render_template('result.html', status=status)

if __name__ == '__main__':
    app.run(debug=True)
