from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  
import numpy as np
import joblib
import os

app = Flask(__name__)
CORS(app)

# Load models and preprocessors
svm_model = joblib.load("svm_model.pkl")
rf_model = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

try:
    pca = joblib.load("pca.pkl")
    apply_pca = True
except FileNotFoundError:
    pca = None
    apply_pca = False


@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        temperature = float(data.get("temperature"))
        humidity = float(data.get("humidity"))
        moisture = float(data.get("moisture"))
        soil_type = data.get("soil_type", "").lower()
        crop_type = data.get("crop_type", "").lower()
        nitrogen = float(data.get("nitrogen"))
        phosphorus = float(data.get("phosphorus"))
        potassium = float(data.get("potassium"))

        if soil_type not in label_encoders['Soil_Type'].classes_:
            return jsonify({"error": f"Invalid soil type: {soil_type}"}), 400
        if crop_type not in label_encoders['Crop_Type'].classes_:
            return jsonify({"error": f"Invalid crop type: {crop_type}"}), 400

        soil_encoded = label_encoders['Soil_Type'].transform([soil_type])[0]
        crop_encoded = label_encoders['Crop_Type'].transform([crop_type])[0]

        user_input = np.array([[temperature, humidity, moisture, soil_encoded, crop_encoded, nitrogen, phosphorus, potassium]])

        user_input_scaled = scaler.transform(user_input)

        if apply_pca:
            user_input_scaled = pca.transform(user_input_scaled)

        svm_proba = svm_model.predict_proba(user_input_scaled)
        rf_proba = rf_model.predict_proba(user_input_scaled)
        final_prediction = np.argmax((svm_proba + rf_proba) / 2)

        recommended_fertilizer = label_encoders['Fertilizer'].inverse_transform([final_prediction])[0]

        return jsonify({"recommended_fertilizer": recommended_fertilizer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
