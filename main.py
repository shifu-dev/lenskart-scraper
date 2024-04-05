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


def scrap_all_stores(limit=10000):
    list_scraper = stores.StoreListScraper()
    store_list_url = "https://www.lenskart.com/stores"

    print(f"scraping {store_list_url}...")
    store_urls = list_scraper.scrap(store_list_url, limit=limit)
    print(f"found {len(store_urls)} stores.")

    file = open("stores.csv", "w")
    writer = csv.writer(file)
    exporter = stores.StoreExporter(writer)

    scraper = stores.StoreScraper()
    for url in store_urls:
        print(f"scraping store: {url}")
        details = scraper.scrap(url)
        exporter.add(details)

    file.close()


def scrap_all_eyeglasses(limit=10000):
    list_scraper = eyeglasses.list_scrapper()
    eyeglass_list_url = (
        "https://www.lenskart.com/eyeglasses/promotions/all-kids-eyeglasses.html"
    )
    eyeglass_urls = list_scraper.scrap(eyeglass_list_url, limit=limit)

    file = open("eyeglasses.csv", "w")
    writer = csv.writer(file)
    exporter = eyeglasses.exporter(writer)

    scraper = eyeglasses.scraper()
    for url in eyeglass_urls:
        print(f"scraping eyeglass: {url}")
        details = scraper.scrap(url)
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
    exit()

if args.scrap == "stores":
    scrap_all_stores(args.limit)
    exit()

if args.scrap == "store":
    if args.url is None:
        "please pass --url too."

    scrap_store(args.url)
    exit()

else:
    parser.print_help()
    exit()
