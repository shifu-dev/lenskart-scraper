import requests
from bs4 import BeautifulSoup


class product_list_scrapper:
    def scrap(self, url):

        print(f"scrapping {url}...")

        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        products_tag = soup.find_all(class_="ProductContainer--jvh5co hOkCDF")

        print(f"found {len(products_tag)} products_tag.")

        products = []
        for product_tag in products_tag:
            product_id = product_tag.get("id")
            product_url = product_tag.contents[0].get("href")[1:]
            products.append((product_id, product_url))

        return products


product_list_scrapper().scrap("https://www.lenskart.com/eyeglasses.html?pageCount=95")
