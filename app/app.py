from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, "model", "diet_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "model", "gender_encoder.pkl"), "rb") as f:
    gender_encoder = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    age = int(data["age"])
    gender = data["gender"]
    height = float(data["height"])
    weight = float(data["weight"])
    exercise = int(data["exercise"])
    sleep = int(data["sleep"])

    # BMI calculation
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)

    # BMI category
    if bmi < 18.5:
        bmi_category = "Underweight"
    elif bmi < 25:
        bmi_category = "Normal"
    elif bmi < 30:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obese"

    gender_encoded = gender_encoder.transform([gender])[0]

    input_data = np.array([[
        age,
        gender_encoded,
        height,
        weight,
        bmi,
        exercise,
        sleep
    ]])

    prediction = model.predict(input_data)[0]

    return jsonify({
        "bmi": bmi,
        "bmi_category": bmi_category,
        "diet": prediction
    })


if __name__ == "__main__":
    app.run(debug=True)
