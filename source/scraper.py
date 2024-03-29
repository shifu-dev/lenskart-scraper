from bs4 import BeautifulSoup
import requests
from source.product_details import Details


class Scraper:
    def scrap(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        product_title = soup.find("h1", attrs={"class": "Title--1mf9vro hPTYyn"}).text

        product = Details()
        product.product_title = product_title
        return product
