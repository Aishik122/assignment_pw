import os 
import sys 
from src.exception import CustomException
from src.logger import logging

import pandas as pd 

from dataclasses import dataclass 

@dataclass
class DataIngestionConfig():
    raw_data_path: str = os.path.join('artifacts',"raw_data")

class DataIngestion():
    def __init__ (self):
        self.ingestion_config = DataIngestionConfig()

    
    def initiate_data_ingestion(self):
          logging.info("data ingestion process started ")
          try:
               pass
          except:
               pass
          