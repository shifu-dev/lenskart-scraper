from source import eyeglasses
from source import stores
import argparse

parser = argparse.ArgumentParser(
    prog="lenskart-scraper",
    description="scraps any content from lenskart website and outputs in multiple formats",
)

parser.add_argument("--scrap", type=str, required=True)
parser.add_argument("--url", type=str, required=False)
parser.add_argument("--limit", type=int, required=False)
args = parser.parse_args()

if args.scrap == "eyeglasses":
    eyeglasses.scrap_all(args.limit)

elif args.scrap == "stores":
    stores.scrap_all(args.limit)

elif args.scrap == "store":
    if args.url is None:
        "please pass --url too."

    stores.scrap(args.url)

else:
    parser.print_help()
    exit()
