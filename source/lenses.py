from bs4 import BeautifulSoup
from dataclasses import dataclass
from http import HTTPStatus
import requests
import csv
import re
from typing import List
import json
contact_lens_ids=[]
@dataclass(init=False)
class Details:
    id:str
    model_name:str
    brand_name:str
    image_url:str
    market_price:int
    lenskart_price:int
    purchaseCount:int
    size:str
    color:str
    width:int
    totalNoOfRatings:str
    avgRating:str
    qty:int


class Scraper:
    def scrap(self, url) -> Details:
        print(contact_lens_ids)
        response = requests.get(url)
        
        if response.status_code != HTTPStatus.OK:
            return None
       

    # getting the Json containing the sunglasses info from API
        for category_id in contact_lens_ids:
            url = f'https://api-gateway.juno.lenskart.com/v2/products/category/{category_id}?page-size=1000&page=0'
            response = requests.get(url)
            data = json.loads(response.content)
            if 'result' in data:
                length = len(data['result']["product_list"])

                for i in range(length):
                    id=['result']["product_list"][i]['id']
                    brand_name=['result']["product_list"][i]['brand_name']
                    purchaseCount=['result']["product_list"][i]['purchaseCount']
                    model_name=['result']["product_list"][i]['model_name']
                    image_url=['result']["product_list"][i]['image_url']
                    avgRating=['result']["product_list"][i]['avgRating']
                    market_price=['result']["product_list"][i]['prices'][0]['price']
                    lenscart_price=['result']["product_list"][i]['prices'][1]['price']
                    qty=['result']["product_list"][i]['qty']

            # raw level cleaning data
                    

                    if 'size' in data['result']["product_list"][i]:
                        size=data['result']["product_list"][i]['size']
                    else:
                        size=0

                    if 'color' in data['result']["product_list"][i]:
                        color=data['result']["product_list"][i]['color']
                    else:
                        color=None

                    if ('width') in data['result']["product_list"][i]:
                        width=data['result']["product_list"][i]['width']
                    else:
                        width=None

                    if ('totalNoOfRatings') in data['result']["product_list"][i]:
                        totalNoOfRatings=data['result']["product_list"][i]['totalNoOfRatings']
                    else:
                        totalNoOfRatings=0


        details = Details()
        details.id = id
        details.model_name = model_name
        details.brand_name = brand_name
        details.image_url = image_url
        details.market_price = market_price
        details.lenskart_price = lenscart_price
        details.purchaseCount = purchaseCount
        details.size = size
        details.color = color
        details.width = width
        details.totalNoOfRatings = totalNoOfRatings
        details.avgRating = avgRating
        details.qty = qty
        print(details)
        return details

class ListScraper:
    def scrap(self, url, limit=10000) -> List[str]:

        print(f"scrapping {url}...")

        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        pattern = '<h2 class=\"bold bgcolor123\">(.*?)</h2>.*?(<a.*?)</li>'

        matches = re.findall(pattern, str(soup), re.S)
        print("Matches")
        contact=matches[1]
        print(contact)
        contact_lens_urls = []

# dictionary creation of all urls with corresponding category name
        for  html_content in contact:
            url_regex_pattern = r'<a\s+href="([^"]+)">'
            temp_urls = re.findall(url_regex_pattern, html_content)
            contact_lens_urls.append (temp_urls)
            print(contact_lens_urls)
# loop through every url and get the ids of the specific category from
        global contact_lens_ids 

# loop through every url from each category in the dictionary

        for each_category_url in contact_lens_urls[1]:
            product_html = requests.get(each_category_url)
    # get id of each category
            each_category_id = re.findall(r"{\"pageProps\":{\"data\":{\"id\":(.*?),\"userData\":", product_html.text, re.S)
            contact_lens_ids.append(each_category_id[0])
            print('Got all cateory ids')
        print(contact_lens_ids)
class Exporter:
    def __init__(self, writer):
        self.writer = writer
        writer.writerow([
            "id"
   " model_name"
    "brand_name"
    "image_url"
    "market_price"
    "lenskart_price"
    "purchaseCount"
    "size"
    "color"
    "width"
    "totalNoOfRatings"
    "avgRating"
    "qty"
        ])

    def add(self, details: Details) -> None:
        self.writer.writerow([details.id,
    details.model_name,
    details.brand_name,
    details.image_url,
    details.market_price,
    details.lenskart_price,
    details.purchaseCount,
    details.size,
    details.color,
    details.width,
    details.totalNoOfRatings,
    details.avgRating,
    details.qty,])

    writer: any


def scrap_all(limit=10000):
    list_scraper = ListScraper()
    list_url = "https://www.lenskart.com/contact-lenses.html"
    urls = list_scraper.scrap(list_url, limit=limit)

    file = open("lenses.csv", "w")
    writer = csv.writer(file)
    exporter = Exporter(writer)

    scraper = Scraper()
    print(scraper)
    # for url in urls:
    #     print(f"scraping lens: {url}")
    #     details = scraper.scrap(url)
    #     exporter.add(details)

    file.close()
scrap_all()

