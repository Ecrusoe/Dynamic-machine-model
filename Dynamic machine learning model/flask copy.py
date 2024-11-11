from flask import Flask, render_template, request
import pandas as pd
import requests
import os

app = Flask(__name__)
data_file = 'user_data.csv'

# CSV dosyasını oluştur
if not os.path.isfile(data_file):
    df = pd.DataFrame(columns=['temperature', 'low_threshold', 'high_threshold', 'num_motors', 'motor_actions'])
    df.to_csv(data_file, index=False)

@app.route('/')
def index():
    return render_template('index.html', result="Henüz bir sonuç yok")

@app.route('/submit', methods=['POST'])
def submit():
    temp = float(request.form['temp'])
    low_threshold = float(request.form['low_threshold'])
    high_threshold = float(request.form['high_threshold'])
    num_motors = int(request.form['num_motors'])
    
    motor_actions = []
    for i in range(num_motors):
        action_low = request.form.get(f'motor{i}_action_low')
        action_high = request.form.get(f'motor{i}_action_high')
        motor_actions.append(f"{action_low}, {action_high}")

    # Veriyi CSV dosyasına ekle
    new_data = pd.DataFrame({
        'temperature': [temp],
        'low_threshold': [low_threshold],
        'high_threshold': [high_threshold],
        'num_motors': [num_motors],
        'motor_actions': [str(motor_actions)]
    })
    new_data.to_csv(data_file, mode='a', header=False, index=False)

    return render_template('index.html', result="Veri başarıyla kaydedildi!")

@app.route('/retrain', methods=['POST'])
def retrain():
    # Makine öğrenmesi modelini eğitmek için API çağrısı yap
    response = requests.post('http://localhost:5001/retrain', json={'data_file': data_file})
    
    if response.status_code == 200:
        return render_template('index.html', result="Model başarıyla güncellendi!")
    else:
        return render_template('index.html', result="Model güncellenirken bir hata oluştu.")

if __name__ == '__main__':
    app.run(debug=True)
