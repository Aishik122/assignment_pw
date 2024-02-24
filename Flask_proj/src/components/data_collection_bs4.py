import beautifulsoap 
import requests
import pandas as pd
import bs4

class ProductInfoExtractor:
    def __init__(self, soup):
        self.soup = soup

    def get_title(self):
        try:
            title = self.soup.find("span", attrs={"id": 'productTitle'})
            title_value = title.text.strip()
            return title_value
        except AttributeError:
            return ""

    def get_price(self):
        try:
            price = self.soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()
            return price
        except AttributeError:
            try:
                price = self.soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()
                return price
            except:
                return ""

    def get_rating(self):
        try:
            rating = self.soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
            return rating
        except AttributeError:
            try:
                rating = self.soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
                return rating
            except:
                return ""

    def get_review_count(self):
        try:
            review_count = self.soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
            return review_count
        except AttributeError:
            return ""

    def get_availability(self):
        try:
            available = self.soup.find("div", attrs={'id': 'availability'}).find("span").string.strip()
            return available
        except AttributeError:
            return "Not Available"
