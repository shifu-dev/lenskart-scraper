import argparse
from source import glasses
from source import stores
from source import lenses
from source import writers
from source import utils

parser = argparse.ArgumentParser(
    prog="lenskart-scraper",
    description="""
        Scraps any content from lenskart website and outputs in multiple formats.
    """,
)

parser.add_argument(
    "target",
    type=str,
    nargs="+",
    help="""
        The target to scrap. This could be a list of urls or following values:
        - 'everything': Scrap all information (includes glasses, lenses and stores).
        - 'glasses': Scrap all glasses information (includes 'eyeglasses', 'sunglasses', ...).
        - 'eyeglasses': Scrap all eyeglasses information.
        - 'sunglasses': Scrap all sunglasses information.
        - 'kidsglasses': Scrap all kidsglasses information.
        - 'computer-glasses': Scrap all computer-glasses information.
        - 'power-sunglasses': Scrap all power-sunglasses information.
        - 'lenses': Scrap all contact lenses information.
        - 'stores': Scrap all stores information (includes 'stores-delhi', ...).
        - 'stores-delhi': Scrap all stores information available in delhi.
        - 'stores-chennai': Scrap all stores information available in chennai.
    """,
)

parser.add_argument(
    "--limit",
    type=int,
    default=1000,
    help="""
        Maximum count of item details to scrap.
        This is only applilcable for targets which contain multiple items,
        like 'eyeglasses' and 'stores'.

        Note: This limit has no effect if more urls are specified than the limit.
    """,
)

parser.add_argument(
    "--out",
    type=str,
    default="console",
    help="""
        The output to write to, valid options are 'console' or a file path.
    """,
)

parser.add_argument(
    "--out-format",
    type=str,
    choices=["csv", "json"],
    help="""
        The format in which to output the scraped infomration.
        The default value for 'console' is 'json'.
        For files with the output format is derived from its extension.
        The default value for file with no extension is 'csv'.
    """,
)

parser.add_argument(
    "--parallel",
    type=int,
    default="0",
    help="""
        Enables parallel scraping. The value represents number of parallel scrapers to run at once.
    """,
)


def main() -> None:
    args = parser.parse_args()

    writer = writers.ConsoleWriter()

    if len(args.target) == 1:
        target: str = args.target[0]

        if target == "everything":
            print("everything: not implementd yet.")
            return

        if target == "glasses":
            glasses.scrap_all(writer, args.limit)
            return

        if target == "eyeglasses":
            glasses.scrap_all_eyeglasses(writer, args.limit)
            return

        if target == "sunglasses":
            glasses.scrap_all_sunglasses(writer, args.limit)
            return

        if target == "kidsglasses":
            glasses.scrap_all_kidsglasses(writer, args.limit)
            return

        if target == "computer-glasses":
            glasses.scrap_all_computer_glasses(writer, args.limit)
            return

        if target == "power-sunglasses":
            glasses.scrap_all_power_sunglasses(writer, args.limit)
            return

        if target == "lenses":
            lenses.scrap_all(writer, args.limit)
            return

        if target == "stores":
            stores.scrap_all(writer, args.limit)
            return

        if target == "stores-delhi":
            stores.scrap_all_delhi(writer, args.limit)
            return

        if target == "stores-chennai":
            stores.scrap_all_chennai(writer, args.limit)
            return

        if not utils.is_url_valid(target):
            print("invalid url or unknown option.")
            glasses.scrap_one(target, writer)
            return

    for url in args.target:
        if not utils.is_url_valid(url):
            print(f"invalid url '{url}'")
            return

    for url in args.target:
        glasses.scrap_one(url, writer)
        return


if __name__ == "__main__":
    main()
