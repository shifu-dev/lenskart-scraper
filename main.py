import sys
from source.scraper import Scraper


def main(args, argc):
    if argc < 2:
        print("pass the link to scrap.")
        return

    scraper = Scraper()
    url = args[1]
    details = scraper.scrap(url)
    print(details)


if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
