import argparse
from source import glasses
from source import stores
from source import lenses

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
        - 'kidsglasses': Scrap all kidsglasses information.
        - 'sunglasses': Scrap all sunglasses information.
        - 'computer-glasses': Scrap all computer-glasses information.
        - 'power-sunglasses': Scrap all power-sunglasses information.
        - 'progressive-glasses': Scrap all progressive-glasses information.
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

    if len(args.target) == 1:
        target: str = args.target[0]

        if target == "everything":
            print("everything")
            return

        if target == "glasses":
            print("glasses")
            return

        if target == "eyeglasses":
            glasses.scrap_all_eyeglasses(args.limit)
            return

        if target == "kidsglasses":
            print("kidsglasses")
            return

        if target == "sunglasses":
            print("sunglasses")
            return

        if target == "computer-glasses":
            print("computer-glasses")
            return

        if target == "power-sunglasses":
            print("power-sunglasses")
            return

        if target == "progressive-glasses":
            print("progressive-glasses")
            return

        if target == "lenses":
            print("lenses")
            return

        if target == "stores":
            print("stores")
            return

        if target == "stores-delhi":
            print("stores-delhi")
            return

        if target == "stores-chennai":
            print("stores-chennai")
            return

    print(f"list of urls passed, target: {args.target}")


if __name__ == "__main__":
    main()
