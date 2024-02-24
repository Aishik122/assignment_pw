import os 
import BeautifulSoup
import sys 
import requests
from src.exception import CustomException
from src.logger import logging
from data_collection_bs4 import ProductInfoExtractor

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
            # add your user agent 
            HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

            # The webpage URL
            URL = "https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2"

            # HTTP Request
            webpage = requests.get(URL, headers=HEADERS)

            # Soup Object containing all data
            soup = BeautifulSoup(webpage.content, "html.parser")

            # Fetch links as List of Tag Objects
            links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

            # Store the links
            links_list = []

            # Loop for extracting links from Tag Objects
            for link in links:
                links_list.append(link.get('href'))

            d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
    
            # Loop for extracting product details from each link 
            for link in links_list:
                new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                # Function calls to display all necessary product information
                d['title'].append(get_title(new_soup))
                d['price'].append(get_price(new_soup))
                d['rating'].append(get_rating(new_soup))
                d['reviews'].append(get_review_count(new_soup))
                d['availability'].append(get_availability(new_soup))

    
            amazon_df = pd.DataFrame.from_dict(d)
            amazon_df['title'].replace('', np.nan, inplace=True)
            amazon_df = amazon_df.dropna(subset=['title'])
            amazon_df.to_csv("amazon_data.csv", header=True, index=False)


        except Exception as e:
            pass
          