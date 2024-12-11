from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import tensorflow as tf

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Muat model TensorFlow (.h5)
try:
    model = tf.keras.models.load_model("models/model.h5")
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# Daftar label kelas obesitas asli (urutannya sesuai saat pelatihan)
obesity_labels = [
    "Underweight", "Normal weight", "Obesity Type I",
    "Obesity Type II", "Obesity Type III", "Overweight Level I", "Overweight Level II"
]

# Skema untuk input data
class PredictionInput(BaseModel):
    gender: int
    age: int
    height: float
    weight: float
    family_history: int
    high_caloric_food: int
    freq_vegetables: int
    main_meals: int
    food_between_meals: int
    smoking: int
    water_daily: int
    calories_monitor: int
    physical_activity_freq: int
    time_using_devices: int
    alcohol_consumption: int
    transportation: int
    obesity: int

# Endpoint root
@app.get("/")
async def root():
    return {"message": "Obesity Classification API is running"}

# Endpoint prediksi
@app.post("/predict")
async def predict(input_data: PredictionInput):
    try:
        # Konversi input data ke dalam array numpy
        input_array = np.array([
            [
                input_data.gender,
                input_data.age,
                input_data.height,
                input_data.weight,
                input_data.family_history,
                input_data.high_caloric_food,
                input_data.freq_vegetables,
                input_data.main_meals,
                input_data.food_between_meals,
                input_data.smoking,
                input_data.water_daily,
                input_data.calories_monitor,
                input_data.physical_activity_freq,
                input_data.time_using_devices,
                input_data.alcohol_consumption,
                input_data.transportation,
                input_data.obesity,
            ]
        ])

        # Lakukan prediksi menggunakan model
        predictions = model.predict(input_array)

        # Ambil kelas obesitas yang diprediksi
        predicted_class = np.argmax(predictions, axis=1)

        # Konversi angka kelas menjadi label kelas
        predicted_label = [obesity_labels[i] for i in predicted_class]

        # Mengembalikan hasil prediksi
        return {
            "probabilities": predictions.tolist(),
            "predicted_class": predicted_label
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
