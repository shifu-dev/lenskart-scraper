import requests
from bs4 import BeautifulSoup
from source import writers
from http import HTTPStatus
import csv
from dataclasses import dataclass
from source import writers
from source import runners


@dataclass(init=False)
class Details:
    name: str
    address: str
    timing: str
    service: str
    contact_number: int
    gmap_link: str
    rating: int
    nearby_stores: list


class Scraper:
    def scrap(self, url: str) -> Details:
        print(f"scraping '{url}'.")

        response = requests.get(url)
        if response.status_code != HTTPStatus.OK:
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        details = Details()

        details.name = soup.find("h1", class_="Home_name__J6U_a").text.strip()
        details.address = soup.find("div", class_="Home_wrapper__ARCSA").text.strip()
        timing_text = soup.find("div", class_="Home_infoBox__PV5Wz").text.strip()
        details.timing = timing_text.split(".Close")[1]
        details.service = (
            soup.find_all("span", class_="Home_miniHead__KKq3S")[1]
            .find_next_sibling()
            .text.strip()
        )
        tel_links = soup.find_all("a", href=lambda href: href and "tel:" in href)
        details.contact_number = tel_links[1]["href"].split(":")[1]
        details.gmap_link = soup.find(
            "a", href=lambda href: href and "maps.google.com" in href
        )["href"]
        review_count = soup.find("div", class_="Home_count__Y0nOJ").text.strip()
        rating = (
            soup.find("div", class_="Home_rating__BaBug").text.strip() + review_count
        )
        details.rating = rating

        nearby_stores = soup.find_all("div", class_="StoreCard_halfCard__X8eye")
        nearby_store_details = []
        for store in nearby_stores:
            nearby_store_name = (
                store.find("div", class_="StoreCard_name__mrTXJ")
                .find("span")
                .text.strip()
            )
            nearby_store_address = (
                store.find("div", class_="storeDetials").find("span").text.strip()
            )
            nearby_store_distance = nearby_store_address.split(".")[1:][0]
            nearby_store_details.append(
                {"Store Name": nearby_store_name, "Distance": nearby_store_distance}
            )

        details.nearby_stores = nearby_store_details

        return details


class ListScraper:

    # todo: implement this, this is a dummy implementatiom.
    def scrap(self, url: str, limit: int) -> list[str]:
        urls = []
        urls.append(
            "https://www.lenskart.com/stores/lenskart-com-chhatarpur-mehrauli-new-delhi-136896/Home"
        )
        urls.append(
            "https://www.lenskart.com/stores/lenskart-com-jawahar-nagar-optometrists-jawahar-nagar-new-delhi-77003/Home"
        )
        urls.append(
            "https://www.lenskart.com/stores/optometrist-sunglasses-paschim-vihar-new-delhi-60858/Home"
        )
        urls.append(
            "https://www.lenskart.com/stores/optometrist-sunglasses-model-town-new-delhi-60859/Home"
        )
        return urls


class Exporter:

    def __init__(self, writer: writers.Writer):
        self.writer = writer
        self.writer.write_headers(
            [
                "Name",
                "Address",
                "Timing",
                "Service",
                "Contact Number",
                "Google Map Link",
                "Rating",
                "Nearby Stores",
            ]
        )

    def add(self, details: range) -> None:
        self.writer.write_row(
            [
                details.name,
                details.address,
                details.timing,
                details.service,
                details.contact_number,
                details.gmap_link,
                details.rating,
                details.nearby_stores,
            ]
        )

    writer: object


def scrap_all(
    writer: writers.Writer, runner: runners.ScraperRunner, limit: int
) -> None:
    list_scraper = ListScraper()
    list_url = "https://www.lenskart.com/stores"

    print(f"scraping {list_url}...")
    urls = list_scraper.scrap(list_url, limit)
    print(f"found {len(urls)} stores.")

    exporter = Exporter(writer)
    scraper = Scraper()
    details = runner.run(scraper, urls)

    for detail in details:
        exporter.add(detail)
