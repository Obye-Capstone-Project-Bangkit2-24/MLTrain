# MLTrain

Repository ini bertujuan untuk mendukung pembuatan model machine learning, membangun Docker container image untuk Cloud Run, serta menyediakan REST API untuk prediksi model machine learning yang terhubung dengan database di Cloud SQL untuk aplikasi Obye.

## Fitur Proyek

### Fungsi Utama
- Membuat dan melatih model machine learning.
- Membuat Docker Image untuk deployment.
- Membuat REST API untuk melakukan prediksi model machine learning.

### API Endpoint
- **POST /predict**: Membuat prediksi model baru.
- **GET /predict/{id}**: Melihat hasil prediksi dengan ID tertentu.

## Cara Menjalankan Proyek
1. Clone repository ini:
   ```bash
   git clone https://github.com/Obye-Capstone-Project-Bangkit2-24/MLTrain.git
   ```
2. Masuk ke direktori proyek:
   ```bash
   cd MLTrain
   ```
3. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan server:
   ```bash
   uvicorn main:app --reload
   ```

## Tech Stack
- **Jupyter Notebook**: Untuk pembuatan dan pelatihan model.
- **Python**: Bahasa pemrograman utama.
- **Docker**: Membuat container untuk deployment.
- **FastAPI**: Framework untuk REST API.
- **NumPy**: Operasi numerik.
- **Pydantic**: Validasi data.
- **TensorFlow**: Library untuk machine learning.
- **Uvicorn**: Server untuk menjalankan aplikasi.
- **MySQL Connector for Python**: Connector untuk MySQL.
