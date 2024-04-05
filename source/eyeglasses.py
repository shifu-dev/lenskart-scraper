from bs4 import BeautifulSoup
import requests
import csv


class Details:
    name: str
    collection: str
    size: str
    price: int
    currency: str
    coupen_code: str
    rating: int


class Scraper:
    def scrap(self, url) -> Details:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # todo: update this code to fetch from single product page instead, like the one below
        #
        # name = soup.find("p", class_="ProductTitle--13we1dx").text
        # price = soup.find("span", class_="SpecialPriceSpan--1olt47v")
        # price = price.get_text().split("₹")[1]
        # offer = soup.find("div", class_="OfferContainer--zhhshs").text
        # discount = offer.split("₹")[1].split(".")[0].strip()
        # coupen = offer.split(": ")[1]
        # size_details = soup.find("span", class_="ProductSize--64lzs8").text
        # size = size_details.split(": ")[1].split(" •")[0]
        # collection = size_details.split("•")[1].strip()
        # review = soup.find("span", class_="NumberedRatingSpan--fq61xb").text

        # details = Details()
        # details.name = name
        # details.collection = collection
        # details.size = size
        # details.price = price
        # details.price = discount
        # details.coupen_code = coupen
        # details.rating = review

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        product_title = soup.find(class_="Title--1mf9vro hPTYyn").text
        product_price_span = soup.find(class_="SpecialPriceSpan--1olt47v eowfNn")
        product_currency = product_price_span.contents[0].text
        product_price = product_price_span.contents[1].text
        product_size_text = soup.find(class_="Size--13d7slh dCZfjB").text
        product_size = product_size_text[7:]  # 7 for "Size : " in "Size : Wide"

        details = Details()
        details.name = product_title
        details.price = product_price
        details.currency = product_currency
        details.size = product_size
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
        writer.writerow(["Title", "Price", "Currency Type", "Size"])

    def add(self, details) -> None:
        self.writer.writerow(
            [
                details.name,
                details.price,
                details.currency,
                details.size,
            ]
        )

    writer: any


def scrap_all(limit=10000):
    list_scraper = ListScraper()
    eyeglass_list_url = (
        "https://www.lenskart.com/eyeglasses/promotions/all-kids-eyeglasses.html"
    )
    eyeglass_urls = list_scraper.scrap(eyeglass_list_url, limit=limit)

    file = open("eyeglasses.csv", "w")
    writer = csv.writer(file)
    exporter = Exporter(writer)

    scraper = Scraper()
    for url in eyeglass_urls:
        print(f"scraping eyeglass: {url}")
        details = scraper.scrap(url)
        exporter.add(details)

    file.close()
