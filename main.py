import sys
from source.scraper import Scraper as eyeglass_scraper
from source.product_list_scrapper import product_list_scrapper
import argparse

parser = argparse.ArgumentParser(
    prog="lenskart-scraper",
    description="scraps any content from lenskart website and outputs in multiple formats",
)

parser.add_argument("--parse")
args = parser.parse_args()

scraper = eyeglass_scraper()
if args.parse == "eyeglasses":
    eyeglasses_list_link = "https://www.lenskart.com/eyeglasses.html?pageCount=95"
    eyeglass_links = product_list_scrapper().scrap(eyeglasses_list_link)
    for link in eyeglass_links:
        details = scraper.scrap(f"https://www.lenskart.com/{link[1]}")
        print(details)
else:
    print("we only support eyeglasses for now.")
    exit()
