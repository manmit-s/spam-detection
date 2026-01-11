# Spam Detection Model Codebase Analysis Report

## 1. Introduction & Project Overview
This project is a machine learning system designed to classify SMS messages as either **Spam** (unwanted) or **Ham** (legitimate). The codebase implements a complete **MLOps (Machine Learning Operations)** pipeline, handling everything from raw data insertion to model deployment.

The system is built as a modular Python application where each step of the machine learning lifecycle (Ingestion, Transformation, Training, Evaluation, Deployment) is encapsulated in its own "Component".

**Key Workflow:**
1.  **Data Ingestion:** Raw CSV data is uploaded to a MongoDB database.
2.  **Training Pipeline:** Data is pulled from MongoDB, cleaned, transformed, and used to train a model.
3.  **Deployment:** A web application (FastAPI) provides an interface for users to enter messages and get predictions.

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

### 3.2. Vectorization (`CountVectorizer`)
After cleaning, the text is converted into a matrix of numbers using a "Bag of Words" approach.
*   **CountVectorizer:** It counts how many times each word appears in a message.
*   *Result:* High-dimensional numerical arrays representing the text.

### 3.3. Target Encoding (`OrdinalEncoder`)
The label column (Spam vs Ham) is text. The `OrdinalEncoder` converts these labels into numbers (e.g., Ham=0, Spam=1).

---

## 4. Handling Imbalanced Data
*Addressing the disparity between Spam and Ham classes.*

The codebase imports a library for handling imbalance (`SMOTETomek` from `imblearn`), which is a technique to artificially generate synthetic examples of the minority class (Spam) to balance the dataset.

> **Note:** While the library is imported in `data_transformation.py`, the specific lines of code that *apply* SMOTE are not active in the main transformation flow in the analyzed files. The system currently proceeds by concatenating the vectorized features directly. This suggests the dataset might be sufficiently balanced, or this feature is planned for future implementation.

---

## 5. Model Architecture
*The "Brain" of the system.*

The project uses a sophisticated approach to model selection, leveraging a custom library named **`neuro_mf` (Neuro Model Factory)**.

### 5.1. Model Factory (`src/components/model_trainer.py`)
Instead of hardcoding a single algorithm (like "Logistic Regression"), the system uses `ModelFactory`.
*   **Function:** It reads a configuration file (`model.yaml`) which lists multiple algorithms and their settings (hyperparameters).
*   **AutoML Capabilities:** It likely trains multiple models and automatically selects the one that performs best based on an "Expected Accuracy" threshold.

### 5.2. The Wrapper Model (`SpamhamDetectionModel`)
To ensure the model is easy to use after training, it is wrapped in a custom class:
*   **Encapsulation:** This class holds the **trained model** AND the **preprocessing tools** (Vectorizer and Encoder) together.
*   **Smart Prediction:** When you ask it to predict "Win cash now", it automatically runs the cleaning and vectorization steps *inside* the class before passing the numbers to the actual model. This prevents "data leakage" and makes deployment very easy.

---

## 6. Training Process
*Teaching the model.*

The training logic is orchestrated by the **`TrainPipeline`** (`src/pipeline/train_pipeline.py`).

1.  **Ingestion:** Get data from MongoDB.
2.  **Validation:** Check if data schema is correct (columns, types).
3.  **Transformation:** Clean text and vectorise.
4.  **Trainer:**
    *   Load transformed data.
    *   Ask `ModelFactory` to find the best model.
    *   If the best model's accuracy > `expected_accuracy`, save it.
    *   If not, raise an error (prevents bad models from being saved).
5.  **Evaluation:** Compare the new model against the currently deployed model (if any).
6.  **Pusher:** If the new model is better, push it to the deployment storage (S3 bucket).

---

## 7. Validation & Testing
*Grading the model.*

The system uses standard classification metrics to evaluate performance. The **`ModelTrainer`** calculates:
*   **F1 Score:** A balanced measure of precision and recall.
*   **Precision:** "Of all the messages predicted as Spam, how many were actually Spam?"
*   **Recall:** "Of all the actual Spam messages, how many did we catch?"

There is also a separate script **`train_and_export.py`** which serves as a standalone experiment. It runs a `GridSearchCV` (exhaustive search) on standard algorithms like Naive Bayes (`GaussianNB`) to find the best parameters, providing a "sandbox" for testing new ideas outside the main pipeline.

---

## 8. Deployment & Usage
*How users interact with the model.*

The application is deployed using **FastAPI**, a modern, high-performance web framework (`app.py`).

### 8.1. The Web Application
*   **Frontend:** Simple HTML templates (`index.html`, `prediction.html`) allow users to type a message.
*   **Backend:**
    *   **`/train` Route:** Triggers the entire `TrainPipeline` manually. Useful for retraining when new data arrives.
    *   **`/predict` Route:** Accepts a message, runs it through the `PredictionPipeline`, and displays whether it is Spam or Ham.

### 8.2. Prediction Pipeline (`src/pipeline/prediction_pipeline.py`)
This is the bridge between the user and the saved model.
1.  **Load Model:** Downloads the latest trained model from the S3 bucket (or local artifacts).
2.  **Predict:** Passes the user's text to the model and returns the result.

---

## 9. Error Handling & Logging
*Keeping the system healthy.*

### 9.1. Custom Exceptions (`src/exception.py`)
The project defines a `SpamhamException` class.
*   **Feature:** Whenever an error occurs (e.g., "File not found"), this custom exception captures the **file name** and **line number** where the error happened.
*   **Benefit:** deeply simplifies debugging.

### 9.2. Logging (`src/logger.py`)
A `logging` system records every major step.
*   **What is logged:** "Entered data ingestion", "Connected to MongoDB", "Model training started".
*   **Why:** If the app crashes, the logs tell us exactly what the system was doing immediately before the crash.

---

## 10. Conclusion
This codebase represents a professional-grade pattern for Machine Learning. It goes beyond simple "notebook coding" by implementing:
*   **Modularity:** Each step is a separate component.
*   **Reproducibility:** Pipelines ensure training happens the same way every time.
*   **Scalability:** Uses MongoDB and S3-compatible structure (artifacts) for data management.

**Key Takeaway:** The system effectively transforms raw noisy text into reliable predictions by chaining together rigorous preprocessing, automated model selection, and a user-friendly web interface.
