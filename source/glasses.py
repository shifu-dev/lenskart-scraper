from bs4 import BeautifulSoup
from dataclasses import dataclass
from http import HTTPStatus
import requests
import json
import csv


@dataclass(init=False)
class Details:
    name: str
    size: str
    price: int
    currency: str
    brand_name: str
    product_type: str
    frame_type: str
    frame_shape: str
    collection: str
    frame_size: str
    coupon_code: str
    rating: str
    weight_group: str
    material: str
    product_warranty: str
    gender: str
    purchase_count: int
    product_quantity: int


class Scraper:
    def scrap(self, url) -> Details:
        response = requests.get(url)

        if response.status_code != HTTPStatus.OK:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        product_name = soup.find(class_="Title--1mf9vro hPTYyn").text
        product_price_span = soup.find(class_="SpecialPriceSpan--1olt47v eowfNn")
        product_currency = product_price_span.contents[0].text
        product_size_text = soup.find(class_="Size--13d7slh dCZfjB").text
        product_size = product_size_text[7:]  # 7 for "Size : " in "Size : Wide"

        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        data = json.loads(script_tag.string)

        product_data = data["props"]["pageProps"]["data"]["productDetailData"]
        technical_product_info = product_data["technicalProductInfo"]
        general_product_info = product_data["generalProductInfo"]

        brand_name = next(
            (
                item["value"]
                for item in technical_product_info
                if item["name"] == "Brand Name"
            ),
            None,
        )
        product_type = next(
            (
                item["value"]
                for item in technical_product_info
                if item["name"] == "Product Type"
            ),
            None,
        )
        frame_type = next(
            (
                item["value"]
                for item in technical_product_info
                if item["name"] == "Frame Type"
            ),
            None,
        )
        frame_shape = next(
            (
                item["value"]
                for item in technical_product_info
                if item["name"] == "Frame Shape"
            ),
            None,
        )

        collection = next(
            (
                item["value"]
                for item in general_product_info
                if item["name"] == "Collection"
            ),
            None,
        )
        frame_size = next(
            (
                item["value"]
                for item in general_product_info
                if item["name"] == "Frame Size"
            ),
            None,
        )
        weight_group = next(
            (
                item["value"]
                for item in general_product_info
                if item["name"] == "Weight Group"
            ),
            None,
        )
        material = next(
            (
                item["value"]
                for item in general_product_info
                if item["name"] == "Material"
            ),
            None,
        )
        product_warranty = next(
            (
                item["value"]
                for item in general_product_info
                if item["name"] == "Product Warranty"
            ),
            None,
        )
        gender = next(
            (
                item["value"]
                for item in general_product_info
                if item["name"] == "Gender"
            ),
            None,
        )

        price = product_data["price"]["basePrice"]
        rating = product_data["productRating"]
        purchase_count = product_data["purchaseCount"]
        product_quantity = product_data["productQuantity"]

        details = Details()
        details.name = product_name
        details.currency = product_currency
        details.size = product_size
        details.brand_name = brand_name
        details.product_type = product_type
        details.frame_type = frame_type
        details.frame_shape = frame_shape
        details.collection = collection
        details.frame_size = frame_size
        details.price = price
        details.coupon_code = ""
        details.rating = rating
        details.weight_group = weight_group
        details.material = material
        details.product_warranty = product_warranty
        details.gender = gender
        details.purchase_count = purchase_count
        details.product_quantity = product_quantity

        return details


class ListScraper:
    def scrap(self, url, limit=10000) -> list[str]:

        print(f"scrapping {url}...")

        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        products_tag = soup.find_all(
            class_="ProductContainer--jvh5co hOkCDF", limit=limit
        )

        print(f"found {len(products_tag)} products.")

        products = []
        for product_tag in products_tag:
            # product_id = product_tag.get("id")
            product_url = product_tag.contents[0].get("href")[1:]
            products.append(f"https://lenskart.com/{product_url}")

        return products


class Exporter:
    def __init__(self, writer):
        self.writer = writer
        writer.writerow(
            [
                "Name",
                "Size",
                "Price",
                "Currency",
                "Brand",
                "Product Type",
                "Frame Type",
                "Frame Shape",
                "Frame Size",
                "Collection",
                "Coupon Code",
                "Rating",
                "Weight Group",
                "Material",
                "Warranty",
                "Gender",
                "Purchase Count",
                "Product Quantity",
            ]
        )

    def add(self, details) -> None:
        self.writer.writerow(
            [
                details.name,
                details.size,
                details.price,
                details.currency,
                details.brand_name,
                details.product_type,
                details.frame_type,
                details.frame_shape,
                details.frame_size,
                details.collection,
                details.coupon_code,
                details.rating,
                details.weight_group,
                details.material,
                details.product_warranty,
                details.gender,
                details.purchase_count,
                details.product_quantity,
            ]
        )

    writer: any


def scrap_all_eyeglasses(limit=10000):
    list_scraper = ListScraper()
    list_url = "https://www.lenskart.com/eyeglasses.html"
    urls = list_scraper.scrap(list_url, limit=limit)

    file = open("eyeglasses.csv", "w")
    writer = csv.writer(file)
    exporter = Exporter(writer)

    scraper = Scraper()
    for url in urls:
        print(f"scraping eyeglass: {url}")
        details = scraper.scrap(url)
        exporter.add(details)

    file.close()
