import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from src.constant.database import DATABASE_NAME, COLLECTION_NAME
from src.constant.env_variable import MONGODB_URL_KEY

# 1. Load Environment Variables
load_dotenv() # <--- This call was missing!

# 2. Load CSV into DataFrame
csv_file_path = "notebooks/data/spamHam_eda.csv" 
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"Could not find the file at {csv_file_path}")

df = pd.read_csv(csv_file_path)

# 3. Connect to MongoDB
mongo_uri = os.getenv(MONGODB_URL_KEY)
if mongo_uri is None:
    raise ValueError(f"Environment variable {MONGODB_URL_KEY} is not set in your .env file")

client = MongoClient(mongo_uri)

# 4. Access DB and Collection
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# 5. Upload data
data = df.to_dict(orient="records")
collection.insert_many(data)

print(f"Successfully inserted {len(data)} documents into MongoDB collection '{COLLECTION_NAME}'!")