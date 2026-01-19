# Spam Detection System 🚀

## Overview
This project is an end-to-end Machine Learning solution designed to classify messages as either **Spam** (unwanted) or **Ham** (legitimate). Built with a production-ready MLOps mindset, it features a complete pipeline from data ingestion to deployment, using **MongoDB** for data storage and **FastAPI** for serving predictions.

## 🌟 Key Features
*   **End-to-End Pipeline:** Modular components for Data Ingestion, Validation, Transformation, Model Training, and Evaluation.
*   **Neuro-MF Integration:** Utilizes a custom Model Factory (`neuro_mf`) configuration for automated model selection and hyperparameter tuning.
*   **MongoDB Storage:** Simulates a real-world enterprise environment where training data is fetched from a NoSQL database.
*   **Experiment Tracking:** Detailed logging and artifact management for every run.
*   **FastAPI Deployment:** A high-performance web API provides a user-friendly interface for real-time predictions.
*   **Imbalance Handling:** Built-in strategies (SMOTE) to handle class imbalance in SMS data.

## 🛠️ Tech Stack
<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

</div>

## 📂 Project Structure
```text
├── src/
│   ├── components/         # Core ML logic (Ingestion, Transformation, Trainer)
│   ├── pipeline/           # Orchestration scripts (Training & Prediction)
│   ├── entity/             # Data classes for config and artifacts
│   ├── constant/           # Hardcoded constants and paths
│   └── logger.py           # Custom logging setup
├── notebooks/              # EDA and experiment sandboxes
├── templates/              # HTML frontend for the web app
├── app.py                  # FastAPI entry point
├── upload_data_mongodb.py  # Script to upload raw CSV to MongoDB
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
*   Python 3.8+
*   MongoDB (Atlas or Local)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/manmit-s/spam-detection.git
    cd spam-detection
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory and add your MongoDB connection string:
    ```env
    MONGO_DB_URL="your_mongodb_connection_string"
    ```

### 💡 Usage

#### 1. Upload Data to Database
Before training, populate your MongoDB instance with the seed data:
```bash
python upload_data_mongodb.py
```

#### 2. Run the Web Application
Start the FastAPI server:
```bash
python app.py
```
Access the application at: `http://localhost:8080`

#### 3. Train the Model
You can trigger the training pipeline via the web URL:
*   Visit `http://localhost:8080/train` to start the training process.
*   Monitor progress in the logs.

#### 4. Make Predictions
*   Go to the home page (`/`).
*   Enter an SMS message.
*   Click **Predict** to see if it's Spam or Ham.

## 🐳 Docker Support

You can also run the application using Docker to ensure a consistent environment.

### Using Docker Compose (Recommended)
1.  Ensure you have Docker and Docker Compose installed.
2.  Make sure your `.env` file is created with `MONGO_DB_URL`.
3.  Run the application:
    ```bash
    docker-compose up --build
    ```
4.  Access the app at `http://localhost:8080`.

### Manual Docker Build
1.  **Build the image:**
    ```bash
    docker build -t spam-detection-app .
    ```
2.  **Run the container:**
    ```bash
    docker run -p 8080:8080 --env-file .env -v $(pwd)/logs:/app/logs -v $(pwd)/artifacts:/app/artifacts spam-detection-app
    ```

## 📊 Pipeline Details

### Data Ingestion
*   Connects to MongoDB.
*   Splits data into Train (80%) and Test (20%) sets.
*   Saves raw data artifacts.

### Data Transformation
*   **Cleaning:** Regex filtering, lowercasing.
*   **NLP:** Stopword removal, Porter Stemming.
*   **Vectorization:** CountVectorizer/TfidfVectorizer.

### Model Training
*   Uses `ModelFactory` to iterate through configured algorithms.
*   Selects the best model based on accuracy score.
*   Saves the model only if it beats the defined threshold.

---
*Developed by Manmit Samal*
