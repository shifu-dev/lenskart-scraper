from bs4 import BeautifulSoup
from dataclasses import dataclass
from http import HTTPStatus
from typing import Final
from source import writers
import requests
import json

EYEGLASSES_URL: Final[str] = "https://www.lenskart.com/eyeglasses.html"
SUNGLASSES_URL: Final[str] = "https://www.lenskart.com/sunglasses.html"
KIDSGLASSES_URL: Final[str] = (
    "https://www.lenskart.com/eyeglasses/promotions/all-kids-eyeglasses.html"
)
COMPUTER_GLASSES_URL: Final[str] = (
    "https://www.lenskart.com/eyeglasses/collections/all-computer-glasses.html"
)
POWER_SUNGLASSES_URL: Final[str] = "https://www.lenskart.com/power-sunglasses-main.html"


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
    def scrap(self, url: str) -> Details:
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
    def scrap(self, url: str, limit: int) -> list[str]:

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
    def __init__(self, writer: writers.Writer):
        self.writer = writer
        writer.write_headers(
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
        self.writer.write_row(
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

    writer: writers.Writer


def _scrap_all(list_url: str, writer: writers.Writer, limit: int) -> None:
    list_scraper = ListScraper()
    urls = list_scraper.scrap(list_url, limit)

    exporter = Exporter(writer)
    scraper = Scraper()
    for url in urls:
        print(f"scraping eyeglass: {url}")
        details = scraper.scrap(url)
        exporter.add(details)


def scrap_one(url: str, writer: writers.Writer) -> None:
    scraper = Scraper()
    exporter = Exporter(writer)

    details = scraper.scrap(url)
    exporter.add(details)


def scrap_all(writer: writers.Writer, limit: int) -> None:

    list_scraper = ListScraper()

    eyeglass_urls = list_scraper.scrap(EYEGLASSES_URL, limit)
    sunglass_urls = list_scraper.scrap(SUNGLASSES_URL, limit)
    kidsglass_urls = list_scraper.scrap(KIDSGLASSES_URL, limit)
    computer_glass_urls = list_scraper.scrap(COMPUTER_GLASSES_URL, limit)
    power_sunglass_urls = list_scraper.scrap(POWER_SUNGLASSES_URL, limit)
    urls = set(
        eyeglass_urls
        + sunglass_urls
        + kidsglass_urls
        + computer_glass_urls
        + power_sunglass_urls
    )

    print(f"found {len(urls)} items.")

    exporter = Exporter(writer)
    scraper = Scraper()
    for url in urls:
        print(f"scraping page {url}.")
        details = scraper.scrap(url)
        exporter.add(details)

    return


def scrap_all_eyeglasses(writer: writers.Writer, limit: int) -> None:
    return _scrap_all(EYEGLASSES_URL, writer, limit)


def scrap_all_sunglasses(writer: writers.Writer, limit: int) -> None:
    return _scrap_all(SUNGLASSES_URL, writer, limit)


def scrap_all_kidsglasses(writer: writers.Writer, limit: int) -> None:
    return _scrap_all(KIDSGLASSES_URL, writer, limit)


def scrap_all_computer_glasses(writer: writers.Writer, limit: int) -> None:
    return _scrap_all(COMPUTER_GLASSES_URL, writer, limit)


def scrap_all_power_sunglasses(writer: writers.Writer, limit: int) -> None:
    return _scrap_all(POWER_SUNGLASSES_URL, writer, limit)
