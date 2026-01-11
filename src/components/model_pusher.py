import sys
from src.entity.artifact_entity import ModelPusherArtifact, ModelTrainerArtifact
from src.entity.config_entity import ModelPusherConfig
from src.exception import SpamhamException
from src.logger import logging
from src.utils.main_utils import MainUtils
import shutil
import os

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise SpamhamException(e, sys)

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info("Entered initiate_model_pusher method of ModelPusher class")
            
            # Local path to save the model (simulating S3 bucket)
            bucket_name = self.model_pusher_config.bucket_name
            model_file_name = self.model_pusher_config.s3_model_key_path
            
            # Construct path: bucket_name/model_file_name
            model_registry_path = os.path.join(bucket_name, model_file_name)
            
            os.makedirs(os.path.dirname(model_registry_path), exist_ok=True)
            
            shutil.copy(self.model_trainer_artifact.trained_model_file_path, model_registry_path)
            
            logging.info(f"Model saved to {model_registry_path}")
            
            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=bucket_name,
                s3_model_path=model_registry_path
            )
            
            logging.info("Exited initiate_model_pusher method of ModelPusher class")
            return model_pusher_artifact
            
        except Exception as e:
            raise SpamhamException(e, sys) from e
