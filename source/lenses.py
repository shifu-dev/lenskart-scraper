from bs4 import BeautifulSoup
from dataclasses import dataclass
from http import HTTPStatus
from source import writers
import requests
import csv


@dataclass(init=False)
class Details:
    name: str


class Scraper:
    def scrap(self, url: str) -> Details:
        response = requests.get(url)

        if response.status_code != HTTPStatus.OK:
            return None

        details = Details()
        details.name = "not implemented yet"
        return details


class ListScraper:
    def scrap(self, url: str, limit: int) -> list[str]:
        return []


class Exporter:
    def __init__(self, writer: writers.Writer):
        self.writer = writer
        writer.write_headers(["Name"])

    def add(self, details: Details) -> None:
        self.writer.write_row([details.name])

    writer: any


def scrap_all(writer: writers.Writer, limit: int):
    list_scraper = ListScraper()
    list_url = ""
    urls = list_scraper.scrap(list_url, limit)

    exporter = Exporter(writer)
    scraper = Scraper()
    for url in urls:
        print(f"scraping page: {url}")
        details = scraper.scrap(url)
        exporter.add(details)
