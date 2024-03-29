from bs4 import BeautifulSoup
import requests
from source.product_details import Details


class Scraper:
    def scrap(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        product_title = soup.find("h1", attrs={"class": "Title--1mf9vro hPTYyn"}).text
        product_price_span = soup.find("span",attrs={ "class": "SpecialPriceSpan--1olt47v eowfNn" })
        product_currency = product_price_span.contents[0].text
        product_price = product_price_span.contents[1].text
        product_size_text = soup.find("p", attrs={ "class": "Size--13d7slh dCZfjB" }).text
        product_size = product_size_text[7:]

        product = Details()
        product.product_title = product_title
        product.product_price = product_price
        product.product_currency = product_currency
        product.product_size = product_size
        return product
