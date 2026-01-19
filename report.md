# Spam Detection Model Codebase Analysis Report

## 1. Introduction & Project Overview
This project is a machine learning system designed to classify SMS messages as either **Spam** (unwanted) or **Ham** (legitimate). The codebase implements a complete **MLOps (Machine Learning Operations)** pipeline, handling everything from raw data insertion to model deployment.

The system is built as a modular Python application where each step of the machine learning lifecycle (Ingestion, Transformation, Training, Evaluation, Deployment) is encapsulated in its own "Component".

**Key Workflow:**
1.  **Data Ingestion:** Raw CSV data is uploaded to a MongoDB database.
2.  **Training Pipeline:** Data is pulled from MongoDB, cleaned, transformed, and used to train a model.
3.  **Deployment:** A web application (FastAPI) provides an interface for users to enter messages and get predictions.
4.  **Containerization:** The entire system is dockerized for consistent environment reproduction and easy cloud scaling.

---

## 2. Data Ingestion
*How raw data is loaded and structured.*

The project uses a **MongoDB** database to store the dataset. This simulates a real-world scenario where data resides in a central database rather than just local CSV files.

### 2.1. Uploading Data (`upload_data_mongodb.py`)
This standalone script is the entry point for raw data.
*   **Function:** Reads a local CSV file (`notebooks/data/spamHam_eda.csv`).
*   **Action:** Connects to a MongoDB instance (cloud or local) using credentials from the environment variables and inserts the data as "documents" into a collection.
*   **Analogy:** Think of this as "stocking the warehouse" (MongoDB) with raw materials (SMS messages) delivered by a truck (the CSV file).

### 2.2. Ingesting Data for Training (`src/components/data_ingestion.py`)
This component creates the connection between the "warehouse" (MongoDB) and the "factory" (ML Pipeline).
*   **`export_data_into_feature_store`**: Queries MongoDB to retrieve the data and saves it locally as a CSV file (the "Feature Store"). This ensures the training process works on a stable snapshot of data.
*   **`split_data_as_train_test`**: Splits the dataset into two parts:
    *   **Training Set:** Used to teach the model.
    *   **Testing Set:** Used to grade the model's performance.
    *   *Result:* Two distinct CSV files are saved in the `artifacts` folder.

---

## 3. Preprocessing
*Cleaning and converting text into numbers.*

Computers cannot understand raw text like "Win a free lottery!". We must convert these messages into numerical formats. This happens in **`src/components/data_ingestion.py`** and **`src/components/data_transformation.py`**.

### 3.1. Text Cleaning & Tokenization
The system implements a custom cleaning process for every message:
1.  **Regex Filtering:** Removes all non-alphabetical characters (e.g., numbers, punctuation).
2.  **Lowercasing:** Converts "Win" and "WIN" to "win" so they are treated as the same word.
3.  **Stemming (PorterStemmer):** Cuts words down to their root form.
    *   *Example:* "running", "runs", "ran" $\rightarrow$ "run".
    *   *Why?* It reduces the complexity of the data.
4.  **Stopword Removal:** Removes common words like "the", "is", "in" which carry little meaning.

---

## 4. Containerization & Portability (NEW)
*Ensuring the system runs everywhere.*

A major addition to the project is the implementation of **Docker**, which solves the "it works on my machine" problem.

### 4.1. Dockerization Strategy
*   **Dockerfile:** Uses a **multi-stage build** based on `python:3.9-slim`.
    *   **Builder Stage:** Compiles heavy dependencies and installs requirements into a virtual environment.
    *   **Runner Stage:** A lightweight final image that only contains the application and its dependencies, significantly reducing the final image size to ~1GB.
*   **Docker Compose:** Orchestrates the application, environment variables (`.env`), and volumes (mapping `logs` and `artifacts` to the local machine).

### 4.2. Cross-Platform Compatibility
The system is configured to handle both Windows and Linux environments. The build process automatically handles Windows-specific libraries like `wincertstore`, ensuring the container can run on any Linux-based cloud server (AWS/Azure).

---

## 5. Model Architecture
*The "Brain" of the system.*

The project uses a sophisticated approach to model selection, leveraging a custom library named **`neuro_mf` (Neuro Model Factory)**.

### 5.1. Model Factory (`src/components/model_trainer.py`)
Instead of hardcoding a single algorithm (like "Logistic Regression"), the system uses `ModelFactory`.
*   **Function:** It reads a configuration file (`model.yaml`) which lists multiple algorithms and their settings (hyperparameters).
*   **AutoML Capabilities:** It trains multiple models and automatically selects the one that performs best based on an "Expected Accuracy" threshold.

### 5.2. The Wrapper Model (`SpamhamDetectionModel`)
To ensure the model is easy to use after training, it is wrapped in a custom class:
*   **Encapsulation:** This class holds the **trained model** AND the **preprocessing tools** (Vectorizer and Encoder) together.
*   **Smart Prediction:** It handles the entire "Text $\rightarrow$ Prediction" flow internally, making it plug-and-play for the web application.

---

## 6. Training Process
*Teaching the model.*

The training logic is orchestrated by the **`TrainPipeline`** (`src/pipeline/train_pipeline.py`).

1.  **Ingestion:** Retrieve data from MongoDB.
2.  **Validation:** Check schema consistency.
3.  **Transformation:** Clean and vectorize text.
4.  **Trainer:** Iterate through models to find the best performer.
5.  **Evaluation:** Compare metrics like F1 Score, Precision, and Recall.
6.  **Pusher:** Export the best model to persistent storage.

---

## 7. Deployment & Logging
*Serving the model and monitoring health.*

### 7.1. Web Application (`app.py`)
*   **FastAPI:** Serves the model through a high-performance REST API.
*   **Dynamic Configuration:** Host and Port are configurable via environment variables, with defaults set for Docker compatibility (`0.0.0.0:8080`).

### 7.2. Monitoring & Debugging
*   **Custom Exceptions:** `SpamhamException` provides detailed traceback info (file/line) for faster debugging.
*   **Logging:** Centralized `logging` system tracks the flow of both Training and Prediction pipelines. In Docker, these logs are persisted to a local folder via volume mounting.

---

## 8. Conclusion
This project has evolved into a robust, portable MLOps system. By combining modular Python architecture with Docker containerization and automated model selection, the system is ready for real-world deployment on cloud platforms like AWS or Azure.

**Key Takeaway:** The move to a containerized multi-stage build has transformed this from a local script into a scalable production asset.

---
*Developed by Manmit Samal*
