from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import mysql.connector

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

# Fungsi untuk menyimpan data ke Cloud SQL
def save_to_db(data: PredictionInput, predicted_class: str):
    try:
        conn = mysql.connector.connect(
            host="34.31.54.153",
            user="root",
            password="123456789",
            database="obye_db"
        )
        cursor = conn.cursor()

        sql_query = """
            INSERT INTO predictions (
                gender, age, height, weight, family_history,
                high_caloric_food, freq_vegetables, main_meals, food_between_meals,
                smoking, water_daily, calories_monitor, physical_activity_freq,
                time_using_devices, alcohol_consumption, transportation, obesity, predicted_class
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.gender, data.age, data.height, data.weight, data.family_history,
            data.high_caloric_food, data.freq_vegetables, data.main_meals, data.food_between_meals,
            data.smoking, data.water_daily, data.calories_monitor, data.physical_activity_freq,
            data.time_using_devices, data.alcohol_consumption, data.transportation,
            data.obesity, predicted_class
        )

        cursor.execute(sql_query, values)
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# Fungsi untuk mengambil data berdasarkan ID
def get_predicted_class_by_id(record_id: int):
    try:
        conn = mysql.connector.connect(
            host="34.31.54.153",
            user="root",
            password="123456789",
            database="obye_db"
        )
        cursor = conn.cursor()

        sql_query = "SELECT predicted_class FROM predictions WHERE id = %s"
        cursor.execute(sql_query, (record_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if not result:
            raise HTTPException(status_code=404, detail="Record not found")

        return result[0]

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

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
        predicted_label = [obesity_labels[i] for i in predicted_class][0]

        # Simpan data input dan hasil prediksi ke database
        save_to_db(input_data, predicted_label)

        return {
            "predicted_class": predicted_label
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

# Endpoint untuk mendapatkan hasil prediksi berdasarkan ID
@app.get("/predict/{id}")
async def get_prediction_by_id(id: int):
    try:
        # Ambil hasil prediksi dari database berdasarkan ID
        predicted_class = get_predicted_class_by_id(id)
        return {"predicted_class": predicted_class}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")