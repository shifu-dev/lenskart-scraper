# lenskart-scraper

---

### Uage

```
usage: lenskart-scraper [-h] [--limit LIMIT] [--out OUT]
                        [--out-format {csv,json}] [--parallel PARALLEL]
                        target [target ...]

Scraps any content from lenskart website and outputs in multiple formats.

positional arguments:
  target                The target to scrap. This could be a list of urls or
                        following values:

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

options:
  -h, --help            show this help message and exit
  --limit LIMIT         Maximum count of item details to scrap. This is only
                        applilcable for targets which contain multiple items,
                        like 'eyeglasses' and 'stores'. Note: This limit has
                        no effect if more urls are specified than the limit.
  --out OUT             The output to write to, valid options are 'console' or
                        a file path.
  --out-format {csv,json}
                        The format in which to output the scraped infomration.
                        The default value for 'console' is 'json'. For files
                        with the output format is derived from its extension.
                        The default value for file with no extension is 'csv'.
  --parallel PARALLEL   Enables parallel scraping. The value represents number
                        of parallel scrapers to run at once.
```

---
