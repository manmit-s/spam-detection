import sys
from typing import Optional

import numpy as np
import pandas as pd

from src.configuration.mongo_db_connection import MongoDBClient
from src.constant.database import DATABASE_NAME
from src.exception import SpamhamException


class SpamhamData:
    """
    This class help to export entire mongo db record as pandas dataframe
    Now modified to load from local CSV for local testing
    """

    def __init__(self):
        """
        """
        # We don't need MongoDB client for local CSV loading
        pass

    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            """
            export entire collectin as dataframe:
            return pd.DataFrame of collection
            """
            # DATA_SOURCE_PATH should be absolute or relative to the execution root (app.py)
            # Assuming the notebook data is the source of truth
            csv_path = r"c:\NEW\PROGRAMMING\DATA SCIENCE WITH GEN AI\Projects\Machine Learning\Project 3 - Spam Detection\Spam Detection\notebooks\data\spamHam_eda.csv"
            
            if not pd.io.common.file_exists(csv_path):
                 # Fallback to relative path if absolute fails
                 csv_path = "notebooks/data/spamHam_eda.csv"
            
            df = pd.read_csv(csv_path)

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise SpamhamException(e, sys)
