import os
import sys

import certifi
import pymongo

from src.constant.database import DATABASE_NAME
from src.constant.env_variable import MONGODB_URL_KEY
import dotenv

from src.exception import SpamhamException

dotenv.load_dotenv()


ca = certifi.where()


class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                
                # Modified connection to be more permissive with SSL errors
                # Removed tlsCAFile to avoid conflict with tlsAllowInvalidCertificates
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsAllowInvalidCertificates=True)
            
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:

            raise SpamhamException(e, sys)

           

