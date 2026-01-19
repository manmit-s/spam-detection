# Spam Detection System 🚀

## Overview
This project is an end-to-end Machine Learning solution designed to classify messages as either **Spam** (unwanted) or **Ham** (legitimate). Built with a production-ready MLOps mindset, it features a complete pipeline from data ingestion to deployment, using **MongoDB** for data storage and **FastAPI** for serving predictions.

## 📖 Detailed Report
For a comprehensive architectural breakdown, data pipeline analysis, and technical implementation details, developers are encouraged to read the **[Full Project Report](report.md)**.


## 🌟 Key Features
*   **End-to-End Pipeline:** Modular components for Data Ingestion, Validation, Transformation, Model Training, and Evaluation.
*   **Neuro-MF Integration:** Utilizes a custom Model Factory (`neuro_mf`) configuration for automated model selection and hyperparameter tuning.
*   **MongoDB Storage:** Simulates a real-world enterprise environment where training data is fetched from a NoSQL database.
*   **Experiment Tracking:** Detailed logging and artifact management for every run.
*   **FastAPI Deployment:** A high-performance web API provides a user-friendly interface for real-time predictions.
*   **Imbalance Handling:** Built-in strategies (SMOTE) to handle class imbalance in SMS data.
*   **🐳 Dockerized:** Fully containerized for consistent deployment across any environment.

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
├── Dockerfile              # Docker build instructions
├── docker-compose.yml      # Docker orchestration
├── upload_data_mongodb.py  # Script to upload raw CSV to MongoDB
├── report.md               # Technical breakdown & architectural report
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose (Recommended) **OR** Python 3.8+
*   MongoDB (Atlas or Local)

### 🐳 Run with Docker (Recommended)
This is the fastest way to get the project running without worrying about dependencies.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/manmit-s/spam-detection.git
    cd spam-detection
    ```

2.  **Set up Environment Variables:**
    Create a `.env` file in the root directory:
    ```env
    MONGO_DB_URL="your_mongodb_connection_string"
    ```

3.  **Launch the Application:**
    ```bash
    docker-compose up --build
    ```
    Access the application at: `http://localhost:8080`

---

### 🐍 Run Locally (Manual Setup)

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the FastAPI server:**
    ```bash
    python app.py
    ```

---

## 💡 Usage

#### 1. Populate Database
Before first-time training, upload the seed data to your MongoDB:
```bash
# If using Docker:
docker exec -it spam-detection-app python upload_data_mongodb.py

# If running locally:
python upload_data_mongodb.py
```

#### 2. Train the Model
Trigger the training pipeline via URL:
*   Visit `http://localhost:8080/train` to start the training process.
*   Monitor progress in the logs or terminal.

#### 3. Make Predictions
*   Go to the home page (`http://localhost:8080`).
*   Enter an SMS message and click **Predict**.

## ☁️ Deployment

Since this project is dockerized, you can deploy it to any cloud provider (AWS, Azure, GCP) by:
1.  Building the image: `docker build -t spam-detection-app .`
2.  Pushing to a Container Registry (e.g., Docker Hub).
3.  Running it on services like Azure App Service, AWS App Runner, or ECS.

---
*Developed by Manmit Samal*
