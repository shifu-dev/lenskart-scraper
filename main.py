import argparse
import os
from source import glasses
from source import stores
from source import lenses
from source import writers
from source import utils


def setup_arg_parsing() -> argparse.ArgumentParser:
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
        choices=["csv"],
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

    return parser


def parse_and_get_writer(args) -> writers.Writer:
    out = args.out
    out_format = args.out_format

    if out is None or out == "":
        print("error: no output specified.")
        exit()

    if out == "console":
        if args.out_format is not None:
            print(
                "warning: ignored option:"
                "'out-format' doesn't have any effect with output type 'console'"
                f", {args.out_format}."
            )

        return writers.ConsoleWriter()

    # consider output is a file path
    #
    # output format is not specified, so we will try to deduce it using the output file path
    if out_format is None:

        ext = os.path.splitext(out)[1]

        if ext == ".csv":
            return writers.CsvWriter(path=out)

        else:
            print(f"error: cannot deduce output format from output file path '{out}'.")
            exit()

    elif out_format == "csv":
        return writers.CsvWriter(path=out)

    else:
        print(f"error: unkown output format '{out_format}'")
        exit()


def parse_and_scrap_target(args, writer: writers.Writer) -> None:

    if len(args.target) == 1:
        target: str = args.target[0]
        limit = args.limit

        if target == "everything":
            print("sorry: target everything is not implementd yet.")
            return

        if target == "glasses":
            glasses.scrap_all(writer, limit)
            return

        if target == "eyeglasses":
            glasses.scrap_all_sunglasses(writer, limit)
            return

        if target == "sunglasses":
            glasses.scrap_all_sunglasses(writer, limit)
            return

        if target == "kidsglasses":
            glasses.scrap_all_kidsglasses(writer, limit)
            return

        if target == "computer-glasses":
            glasses.scrap_all_computer_glasses(writer, limit)
            return

        if target == "power-sunglasses":
            glasses.scrap_all_power_sunglasses(writer, limit)
            return

        if target == "lenses":
            lenses.scrap_all(writer, limit)
            return

        if target == "stores":
            stores.scrap_all(writer, limit)
            return

        if target == "stores-delhi":
            stores.scrap_all_delhi(writer, limit)
            return

        if target == "stores-chennai":
            stores.scrap_all_chennai(writer, limit)
            return

        # the target could be a single url or an invalid target
        if not utils.is_url_valid(target):
            print("error: invalid url or target")
            return

    # the target could be a list of urls
    for url in args.target:
        if not utils.is_url_valid(url):
            print(f"error: invalid url '{url}'")
            return

    for url in args.target:
        glasses.scrap_one(url, writer)
        return


# --------------------------------------------------------------------------------------------------
# main()
# --------------------------------------------------------------------------------------------------

parser = setup_arg_parsing()
args = parser.parse_args()
writer = parse_and_get_writer(args)
parse_and_scrap_target(args, writer)
