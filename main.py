from source import eyeglasses
from source import stores
import argparse
import csv


def scrap_store(url):
    scraper = stores.StoreScraper()
    details = scraper.scrap(url)

    if details is None:
        print(f"unknown error when scraping store url {url}.")
        return

    file = open("stores.csv", "w")
    writer = csv.writer(file)
    exporter = stores.StoreExporter(writer)

    exporter.add(details)
    file.close()


def scrap_all_eyeglasses(limit=10000):
    eyeglasses_list_link = (
        "https://www.lenskart.com/eyeglasses/promotions/all-kids-eyeglasses.html"
    )
    eyeglass_links = eyeglasses.list_scrapper().scrap(eyeglasses_list_link, limit=limit)

    file = open("eyeglasses.csv", "w")
    writer = csv.writer(file)
    exporter = eyeglasses.exporter(writer)

    scraper = eyeglasses.scraper()
    for link in eyeglass_links:
        details = scraper.scrap(link)
        exporter.add(details)

    file.close()


parser = argparse.ArgumentParser(
    prog="lenskart-scraper",
    description="scraps any content from lenskart website and outputs in multiple formats",
)

parser.add_argument("--scrap", type=str, required=True)
parser.add_argument("--url", type=str, required=False)
parser.add_argument("--limit", type=int, required=False)
args = parser.parse_args()

if args.scrap == "eyeglasses":
    scrap_all_eyeglasses(args.limit)
if args.scrap == "store":
    if args.url is None:
        "please pass --url too."

    scrap_store(args.url)
else:
    print("we only support eyeglasses for now.")
    exit()
