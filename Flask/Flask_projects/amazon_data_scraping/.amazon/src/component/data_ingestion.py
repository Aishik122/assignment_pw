from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from src.logger import logging
from src.component.exception import CustomException
import os 


from dataclasses import dataclass 

@dataclass
class DataIngestionConfig:
    raw_data_path:str = os.path.join('artifacts','raw_data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    
    def web_scrap(self,url="https://www.amazon.in/s?k=mobile&crid=3PJ3JF4CY2VAO&sprefix=mobi%2Caps%2C280&ref=nb_sb_noss_2",nums_page=5):
        logging.info("data ingestion initiated")
        def get_title(soup):
            try:
            # Outer Tag Object
                
                title = soup.find("span", attrs={"id":'productTitle'})
            
                # Inner NavigatableString Object
                title_value = title.text

                # Title as a string value
                title_string = title_value.strip()

            except AttributeError:
                title_string = ""

            return title_string

    # Function to extract Product Price
        def get_price(soup):

            try:
                price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

            except AttributeError:

                try:
                    # If there is some deal price
                    price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

                except:
                    price = ""

            return price

    # Function to extract Product Rating
        def get_rating(soup):

            try:
                rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
            
            except AttributeError:
                try:
                    rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
                except:
                    rating = ""	

            return rating

    # Function to extract Number of User Reviews
        def get_review_count(soup):
            try:
                review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

            except AttributeError:
                review_count = ""	

            return review_count

    # Function to extract Availability Status
        def get_availability(soup):
            try:
                available = soup.find("div", attrs={'id':'availability'})
                available = available.find("span").string.strip()

            except AttributeError:
                available = "Not Available"	

            return available

        # add your user agent 
        HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})


        d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
        
        # Loop for extracting product details from each link 
        k=nums_page

        while k>0:
            # The webpage URL
            URL =url
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


            for link in links_list:
                new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                # Function calls to display all necessary product information
                d['title'].append(get_title(new_soup))
                d['price'].append(get_price(new_soup))
                d['rating'].append(get_rating(new_soup))
                d['reviews'].append(get_review_count(new_soup))
                d['availability'].append(get_availability(new_soup))

            
            npc=soup.find_all("a",attrs = {'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
            next_page_link=npc[0].get('href')
            npcc='https://www.amazon.in/'+next_page_link
            URL=npcc
            
            k-=1
            logging.info(f'{k} pages remaining ')
            print(k)
            print(URL)

        
        amazon_df = pd.DataFrame.from_dict(d)
        amazon_df['title'].replace('', np.nan, inplace=True)
        amazon_df = amazon_df.dropna(subset=['title'])
        
        logging.info('Ingesion of the data completed')

        logging.info("Saving Raw data in artifacts")
        os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)

        amazon_df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
        return self.ingestion_config.raw_data_path
        
    

if __name__ == '__main__':
    obj = DataIngestion()
    raw_data=obj.web_scrap()

