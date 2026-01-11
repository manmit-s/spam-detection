
from src.exception import SpamhamException
from src.ml.model.estimator import SpamhamDetectionModel
import sys
from pandas import DataFrame
import os
import shutil
from src.utils.main_utils import MainUtils


class SpamhamDetector:
    """
    This class is used to save and retrieve src model from local storage and to do prediction
    """

    def __init__(self, bucket_name, model_path):
        """
        :param bucket_name: Name of your model bucket (Ignored for local)
        :param model_path: Location of your model
        """
        self.bucket_name = bucket_name
        self.model_path = os.path.join(bucket_name, model_path) if bucket_name else model_path
        self.loaded_model: SpamhamDetectionModel = None

    def is_model_present(self, model_path):
        try:
            return os.path.exists(model_path)
        except Exception as e:
            print(e)
            return False

    def load_model(self) -> SpamhamDetectionModel:
        """
        Load the model from the model_path
        :return:
        """
        if not self.is_model_present(self.model_path):
            raise SpamhamException(f"Model not found at {self.model_path}", sys)
        
        return MainUtils.load_object(self.model_path)

    def save_model(self, from_file, remove: bool = False) -> None:
        """
        Save the model to the model_path
        :param from_file: Your local system model path
        :param remove: By default it is false that mean you will have your model locally available in your system folder
        :return:
        """
        try:
            if remove:
                shutil.move(from_file, self.model_path)
            else:
                shutil.copy(from_file, self.model_path)
        except Exception as e:
            raise SpamhamException(e, sys) from e

    def predict(self, dataframe: DataFrame):
        """
        :param dataframe:
        :return:
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe)
        except Exception as e:
            raise SpamhamException(e, sys)
