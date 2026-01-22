from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.components.data_validation import DataValidation
from Networksecurity.logging.logger import logging
from Networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,DataValidationConfig
from Networksecurity.exception.exception import NetworkSecurityException
import sys

if __name__ == "__main__":
    try:
        logging.info("Initializing Training Pipeline Config")
        training_pipeline_config = TrainingPipelineConfig()

        logging.info("Initializing Data Ingestion Config")
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)

        logging.info("Starting data ingestion")
        data_ingestion = DataIngestion(data_ingestion_config)   # ✅ FIXED

        # Debugging: Check if Mongo is returning data
        df = data_ingestion.export_collection_as_dataframe()
        print("Data fetched from MongoDB:", df.shape)

        if df.empty:
            raise Exception("MongoDB collection is empty. Insert data before running pipeline.")

        # Continue the ingestion
        data_ingestion.export_data_into_feature_store(df)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()

        print(dataingestionartifact)
        logging.info("Data ingestion completed successfully")

        data_validation_config=DataValidationConfig(training_pipeline_config)
        Data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=Data_validation.initiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

