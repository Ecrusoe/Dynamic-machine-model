from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf

# Modeli yükleyelim
model = tf.keras.models.load_model('my_modelson.h5')

app = Flask(__name__)

def predict_operation(num1, num2, operation):
    if operation == "add":
        op = [1, 0, 0, 0]
    elif operation == "subtract":
        op = [0, 1, 0, 0]
    elif operation == "multiply":
        op = [0, 0, 1, 0]
    elif operation == "divide":
        op = [0, 0, 0, 1]
    else:
        return "Invalid operation"

    input_data = np.array([[num1, num2] + op])
    prediction = model.predict(input_data)
    return prediction[0][0]

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']
        result = predict_operation(num1, num2, operation)
    return render_template('web.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)


