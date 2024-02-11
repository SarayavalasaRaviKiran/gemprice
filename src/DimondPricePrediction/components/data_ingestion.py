import pandas as pd
import numpy as np
from src.DimondPricePrediction.logger import logging
from src.DimondPricePrediction.exception import customexception
from src.DimondPricePrediction.components.data_transformation import DataTransformation
from src.DimondPricePrediction.components.data_transformation import DataTransformationConfig

from src.DimondPricePrediction.components.model_trainer import ModelTrainerConfig
from src.DimondPricePrediction.components.model_trainer import ModelTrainer

import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    raw_data_path:str=os.path.join("artifacts","raw.csv")
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        
    
    def initiate_data_ingestion(self):
        logging.info("data ingestion started")
        
        try:
            df=pd.read_csv('notebooks\data\gemstone.csv')
            logging.info(" i have read dataset as a df")
            
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info(" Train test split initiated")
            
            logging.info("here i have performed train test split")
            
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            logging.info("train test split completed")
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info("data ingestion part completed")
            
            return (
                 
                
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
            
        except Exception as e:
           logging.info("exception during occured at data ingestion stage")
           raise customexception(e,sys)
        






if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)


    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))