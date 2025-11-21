import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging

class NetworkDataExtract():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def csv_to_json_convertor(self,file_path):

        """
        This function converts a CSV file to a list of JSON objects.
        Each JSON object represents a row in the CSV file.
        """
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            json_records = list(json.loads(df.T.to_json()).values())
            return json_records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    def insert_data_mongodb(self,records,database,collection_name):
        
        """
        This function inserts a list of JSON objects into a MongoDB collection.
        """
        try:
            self.database=database
            self.collection_name=collection_name
            self.records=records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=ca)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection_name]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
if __name__ == "__main__":
    FILE_PATH="network_data\phisingData.csv"
    database="NetworkSecurity"
    collection_name="PhishingData"
    obj=NetworkDataExtract()
    records=obj.csv_to_json_convertor(FILE_PATH)
    print(records)
    no_of_records=obj.insert_data_mongodb(records,database,collection_name)
    print(f"No of records inserted: {no_of_records}")