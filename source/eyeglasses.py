from bs4 import BeautifulSoup
import requests


class details:
    title = ""
    collection = ""
    size = ""
    price = 0
    currency = ""
    coupen_code = ""
    rating = ""

    def __str__(self) -> str:
        result = (
            f"title: {self.title}\n"
            f"collection: {self.collection}\n"
            f"size: {self.size}\n"
            f"price: {self.price}\n"
            f"currency: {self.currency}\n"
            f"coupen_code: {self.coupen_code}\n"
            f"rating: {self.rating}\n"
        )

        return result


class scraper:
    def scrap(self, url):
        print(f"scraping {url}...")

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # todo: update this code to fetch from single product page instead, like the one below
        #
        # title = soup.find("p", class_="ProductTitle--13we1dx").text
        # price = soup.find("span", class_="SpecialPriceSpan--1olt47v")
        # price = price.get_text().split("₹")[1]
        # offer = soup.find("div", class_="OfferContainer--zhhshs").text
        # discount = offer.split("₹")[1].split(".")[0].strip()
        # coupen = offer.split(": ")[1]
        # size_details = soup.find("span", class_="ProductSize--64lzs8").text
        # size = size_details.split(": ")[1].split(" •")[0]
        # collection = size_details.split("•")[1].strip()
        # review = soup.find("span", class_="NumberedRatingSpan--fq61xb").text

        # details = details()
        # details.title = title
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

        details.title = product_title
        details.price = product_price
        details.currency = product_currency
        details.size = product_size
        return details


class list_scrapper:
    def scrap(self, url):

        print(f"scrapping {url}...")

        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        products_tag = soup.find_all(class_="ProductContainer--jvh5co hOkCDF")

        print(f"found {len(products_tag)} products.")

        products = []
        for product_tag in products_tag:
            # product_id = product_tag.get("id")
            product_url = product_tag.contents[0].get("href")[1:]
            products.append(f"https://lenskart.com/{product_url}")

        return products


class exporter:
    def __init__(self, writer):
        self.writer = writer
        writer.writerow(["Title", "Price", "Currency Type", "Size"])

    def add(self, details):
        self.writer.writerow(
            [
                details.title,
                details.price,
                details.currency,
                details.size,
            ]
        )

    writer: any
