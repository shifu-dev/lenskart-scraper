from bs4 import BeautifulSoup
from dataclasses import dataclass
from http import HTTPStatus
from source import writers
from source import runners
import requests
import re
import json

contact_lens_ids = []


@dataclass(init=False)
class Details:
    id = ""
    model_name = ""
    brand_name = ""
    image_url = ""
    market_price = 0
    lenskart_price = 0
    purchaseCount = 0
    size = ""
    color = ""
    width = 0
    totalNoOfRatings = ""
    avgRating = ""
    quantity = 0


class Scraper:
    def scrap(self, url) -> Details:
        print(contact_lens_ids)
        response = requests.get(url)

        if response.status_code != HTTPStatus.OK:
            return None

        # getting the Json containing the sunglasses info from API
        url = f"https://api-gateway.juno.lenskart.com/v2/products/category/{category_id}?response-size=1000&response=0"
        response = requests.get(url)
        data = json.loads(response.content)
        if "result" in data:
            length = len(data["result"]["product_list"])

            for i in range(length):
                id = data["result"]["product_list"][i]["id"]
                brand_name = data["result"]["product_list"][i]["brand_name"]
                purchaseCount = data["result"]["product_list"][i]["purchaseCount"]
                model_name = data["result"]["product_list"][i]["model_name"]
                image_url = data["result"]["product_list"][i]["image_url"]
                avgRating = data["result"]["product_list"][i]["avgRating"]
                market_price = data["result"]["product_list"][i]["prices"][0]["price"]
                lenscart_price = data["result"]["product_list"][i]["prices"][1]["price"]
                quantity = data["result"]["product_list"][i]["qty"]

                # raw level cleaning data

                if "size" in data["result"]["product_list"][i]:
                    size = data["result"]["product_list"][i]["size"]
                else:
                    size = 0

                if "color" in data["result"]["product_list"][i]:
                    color = data["result"]["product_list"][i]["color"]
                else:
                    color = None

                if ("width") in data["result"]["product_list"][i]:
                    width = data["result"]["product_list"][i]["width"]
                else:
                    width = None

                if ("totalNoOfRatings") in data["result"]["product_list"][i]:
                    totalNoOfRatings = data["result"]["product_list"][i][
                        "totalNoOfRatings"
                    ]
                else:
                    totalNoOfRatings = 0

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
        details.quantity = quantity
        return details


class ListScraper:
    def scrap(self, url: str, limit: int) -> list[str]:

        print(f"scrapping {url}...")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        pattern = '<h2 class="bold bgcolor123">(.*?)</h2>.*?(<a.*?)</li>'
        matches = re.findall(pattern, str(soup), re.S)
        contact = matches[1]
        contact_lens_urls = []

        # dictionary creation of all urls with corresponding category name
        for html_content in contact:
            url_regex = r'<a\s+href="([^"]+)">'
            url = re.findall(url_regex, html_content)
            contact_lens_urls.append(url)

        return contact_lens_urls


class Exporter:
    def __init__(self, writer):
        self.writer = writer
        self.writer.write_headers(
            [
                "Id"
                "Name"
                "Brand Name"
                "Image Url"
                "Market Price"
                "Price"
                "Purchase Count"
                "Size"
                "Color"
                "Width"
                "Number of Ratings"
                "Avg Rating"
                "Quantity"
            ]
        )

    def add(self, details: Details) -> None:
        self.writer.write_row(
            [
                details.id,
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
                details.quantity,
            ]
        )

    writer: any


def scrap_all(writer: writers.Writer, runner: runners.ScraperRunner, limit: int):
    # list_url = "https://www.lenskart.com/contact-lenses.html"
    # list_scraper = ListScraper()
    # urls = list_scraper.scrap(list_url, limit)

    scraper = Scraper()
    result = scraper.scrap(
        "https://www.lenskart.com/soflens-59-6-lens-per-box-bausch-lomb.html"
    )
    print(result)

    # exporter = Exporter(writer)
    # scraper = Scraper()
    # details = runner.run(scraper, urls)

    # for detail in details:
    #     exporter.add(detail)
