from source import eyeglasses
import argparse
import csv


def scrap_all_eyeglasses(limit=10000):
    eyeglasses_list_link = "https://www.lenskart.com/eyeglasses/promotions/all-kids-eyeglasses.html"
    eyeglass_links = eyeglasses.list_scrapper().scrap(eyeglasses_list_link, limit=limit)

    file = open("eyeglasses.csv", "w")
    writer = csv.writer(file)
    exporter = eyeglasses.exporter(writer)

    for link in eyeglass_links:
        details = scraper.scrap(link)
        exporter.add(details)

    file.close()


parser = argparse.ArgumentParser(
    prog="lenskart-scraper",
    description="scraps any content from lenskart website and outputs in multiple formats",
)

parser.add_argument("--parse", type=str, required=True)
parser.add_argument("--limit", type=int, required=False)
args = parser.parse_args()

scraper = eyeglasses.scraper()
if args.parse == "eyeglasses":
    scrap_all_eyeglasses(args.limit)
else:
    print("we only support eyeglasses for now.")
    exit()
