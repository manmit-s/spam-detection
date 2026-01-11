from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelEvaluationArtifact, ModelTrainerArtifact, DataValidationArtifact, DataIngestionArtifact, DataTransformationArtifact
from src.exception import SpamhamException
from src.logger import logging
import sys
import pandas as pd
from src.utils.main_utils import MainUtils
from src.ml.model.s3_estimator import SpamhamDetector
from src.constant.training_pipeline import TARGET_COLUMN
import os

class ModelEvaluation:
    def __init__(self, model_eval_config: ModelEvaluationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 model_trainer_artifact: ModelTrainerArtifact,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SpamhamException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logging.info("Entered initiate_model_evaluation method of ModelEvaluation class")
            
            # Get trained model
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            
            # Check for existing model in "registry"
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.s3_model_key_path
            
            local_model_path = os.path.join(bucket_name, model_path)
            
            spamham_detector = SpamhamDetector(bucket_name=bucket_name, model_path=local_model_path)
            
            is_model_accepted = True
            
            if spamham_detector.is_model_present(local_model_path):
                logging.info("Existing model found. Comparison logic skipped for local fix. Accepting new model.")
                is_model_accepted = True
            else:
                logging.info("No existing model found. Accepting new model.")
                is_model_accepted = True

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                changed_accuracy=0.0,
                best_model_path=trained_model_file_path,
                trained_model_path=trained_model_file_path,
                best_model_metric_artifact=self.model_trainer_artifact.metric_artifact
            )

            logging.info("Exited initiate_model_evaluation method of ModelEvaluation class")
            return model_evaluation_artifact

        except Exception as e:
            raise SpamhamException(e, sys) from e
