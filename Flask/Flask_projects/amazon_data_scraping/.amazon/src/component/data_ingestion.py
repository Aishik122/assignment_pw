import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import logging
import os 


class DataIngestion:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.ingestion_config = DataIngestionConfig()
    
    def web_scrap(self, url="https://www.amazon.in/s?k=mobile&crid=3PJ3JF4CY2VAO&sprefix=mobi%2Caps%2C280&ref=nb_sb_noss_2", nums_page=5):
        logging.info("Data ingestion initiated")
        
        def get_title(soup):
            try:
                title = soup.find("span", attrs={"id":'productTitle'})
                title_string = title.text.strip() if title else ""
            except AttributeError as e:
                logging.error(f"Error fetching title: {e}")
                title_string = ""
            return title_string

        def get_price(soup):
            try:
                price = soup.find("span", attrs={'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span",attrs={'class':'a-price-whole'}).text.strip()
            except AttributeError:
                try:
                    price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()
                except AttributeError:
                    logging.error("Error fetching price")
                    price = ""
            return price

        def get_rating(soup):
            try:
                rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
            except AttributeError:
                try:
                    rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
                except AttributeError:
                    logging.error("Error fetching rating")
                    rating = ""
            return rating

        def get_review_count(soup):
            try:
                review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
            except AttributeError:
                logging.error("Error fetching review count")
                review_count = ""
            return review_count

        def get_availability(soup):
            try:
                available = soup.find("div", attrs={'id':'availability'}).find("span").string.strip()
            except AttributeError:
                logging.error("Error fetching availability")
                available = "Not Available"
            return available

        HEADERS = {'User-Agent': 'Your User-Agent String', 'Accept-Language': 'en-US, en;q=0.5'}
        d = {"title":[], "price":[], "rating":[], "reviews":[], "availability":[]}

        k = nums_page
        while k > 0:
            try:
                webpage = requests.get(url, headers=HEADERS)
                soup = BeautifulSoup(webpage.content, "html.parser")
                links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
                links_list = [link.get('href') for link in links]
                
                for link in links_list:
                    new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
                    new_soup = BeautifulSoup(new_webpage.content, "html.parser")
                    d['title'].append(get_title(new_soup))
                    d['price'].append(get_price(new_soup))
                    d['rating'].append(get_rating(new_soup))
                    d['reviews'].append(get_review_count(new_soup))
                    d['availability'].append(get_availability(new_soup))
                
                next_page_link = soup.find("a", attrs={'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
                if next_page_link:
                    url = "https://www.amazon.in/" + next_page_link.get('href')
                    k -= 1
                    logging.info(f'{k} pages remaining')
                    logging.info(f'Next page URL: {url}')
                else:
                    break

            except Exception as e:
                logging.error(f"Error during scraping: {e}")
                break

        amazon_df = pd.DataFrame.from_dict(d)
        amazon_df['title'].replace('', np.nan, inplace=True)
        amazon_df = amazon_df.dropna(subset=['title'])

        logging.info('Ingestion of the data completed')
        logging.info("Saving Raw data in artifacts")

        os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
        amazon_df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
        return self.ingestion_config.raw_data_path


class DataIngestionConfig:
    raw_data_path = os.path.join('artifacts', 'raw_data.csv')


if __name__ == '__main__':
    obj = DataIngestion()
    raw_data = obj.web_scrap()