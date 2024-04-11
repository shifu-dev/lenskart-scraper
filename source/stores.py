import requests
import bs4
from http import HTTPStatus
from dataclasses import dataclass
from source import writers
from source import runners


@dataclass(init=False)
class Details:
    name = ""
    address = ""
    timing = ""
    service = ""
    contact_number = 0
    gmap_link = ""
    rating = 0
    nearby_stores = []


class Scraper:
    def scrap(self, url: str) -> Details:
        print(f"scraping '{url}'.")

        try:
            response = requests.get(url)
            if response.status_code != HTTPStatus.OK:
                return None

            soup = bs4.BeautifulSoup(response.content, "html.parser")

            details = Details()

            details.name = soup.find("h1", class_="Home_name__J6U_a").text.strip()
            details.address = soup.find(
                "div", class_="Home_wrapper__ARCSA"
            ).text.strip()
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
                soup.find("div", class_="Home_rating__BaBug").text.strip()
                + review_count
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

        except Exception as error:
            return None


class ListScraper:

    def scrap(self, url: str, limit: int) -> list[str]:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        script = soup.find(id="__NEXT_DATA__").contents[0]

        prefix = '"slug":"'
        urls: list[str] = []
        i = 0
        count = 0
        while i < len(script):
            i = script.find(prefix, i)

            if i == -1:
                break

            begin = i + len(prefix)
            end = script.find('"', begin)

            if end == -1:
                print("error parsing script.")
                exit()

            url = f"https://www.lenskart.com/stores/{script[begin:end]}/Home"
            urls.append(url)
            i = end
            count += 1

            if count == limit:
                break

        return urls

    def scrap_for_location(self, location: str, limit: int) -> list[str]:
        url = f"https://www.lenskart.com/stores/location/{location}"
        return self.scrap(url, limit)

    def scrap_all_locations(self, location: str, limit: int) -> list[str]:
        locations = [
            "Delhi",
            "Bangalore",
            "Mumbai",
            "Ahmedabad",
            "Chennai",
            "Hyderabad",
        ]

        urls: list
        for location in locations:
            print(f"scraping location {location}.")
            urls += self.scrap_for_location(location)

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
        if details is None:
            details = Details()

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


def _scrap_all_by_location(
    location: str, writer: writers.Writer, runner: runners.ScraperRunner, limit: int
) -> None:
    list_scraper = ListScraper()
    print(f"scraping location {location}.")
    urls = list_scraper.scrap_for_location(location, limit)

    print(f"found {len(urls)} stores.")

    exporter = Exporter(writer)
    scraper = Scraper()
    details = runner.run(scraper, urls)

    for detail in details:
        exporter.add(detail)


def scrap_all_delhi(
    writer: writers.Writer, runner: runners.ScraperRunner, limit: int
) -> None:
    return _scrap_all_by_location("delhi", writer, runner, limit)


def scrap_all_chennai(
    writer: writers.Writer, runner: runners.ScraperRunner, limit: int
) -> None:
    return _scrap_all_by_location("chennai", writer, runner, limit)


def scrap_all(
    writer: writers.Writer, runner: runners.ScraperRunner, limit: int
) -> None:
    list_scraper = ListScraper()
    urls = list_scraper.scrap_all_locations(limit)
    print(f"found {len(urls)} stores.")

    exporter = Exporter(writer)
    scraper = Scraper()
    details = runner.run(scraper, urls)

    for detail in details:
        exporter.add(detail)
