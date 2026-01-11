import os

PRED_SCHEMA_FILE_PATH = os.path.join('config', 'prediction_schema.yml')

PREDICTION_DATA_BUCKET = "spam-ham-data"
PREDICTION_INPUT_FILE_NAME = "customer_pred_data.csv"
PREDICTION_OUTPUT_FILE_NAME = "customer_predictions.csv"
MODEL_BUCKET_NAME = "model-registry"