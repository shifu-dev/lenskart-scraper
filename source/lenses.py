from bs4 import BeautifulSoup
from dataclasses import dataclass
from http import HTTPStatus
import requests
import csv


@dataclass(init=False)
class Details:
    name: str


class Scraper:
    def scrap(self, url) -> Details:
        response = requests.get(url)

        if response.status_code != HTTPStatus.OK:
            return None

        details = Details()
        details.name = "not implemented yet"
        return details


class ListScraper:
    def scrap(self, url, limit=10000) -> list[str]:
        return []


class Exporter:
    def __init__(self, writer):
        self.writer = writer
        writer.writerow(["Name"])

    def add(self, details: Details) -> None:
        self.writer.writerow([details.name])

    writer: any


def scrap_all(limit=10000):
    list_scraper = ListScraper()
    list_url = ""
    urls = list_scraper.scrap(list_url, limit=limit)

    file = open("lenses.csv", "w")
    writer = csv.writer(file)
    exporter = Exporter(writer)

    scraper = Scraper()
    for url in urls:
        print(f"scraping lens: {url}")
        details = scraper.scrap(url)
        exporter.add(details)

    file.close()
