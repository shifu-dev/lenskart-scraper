from bs4 import BeautifulSoup
import requests


class sunglasses_scraper:
    def scrap(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_names = [item.text for item in soup.find_all(class_='ProductTitle--13we1dx')]
            product_ratings = [item.text for item in soup.find_all(class_='NumberedRatingSpan--fq61xb')]
            product_prices = [item.text for item in soup.find_all(class_='SpecialPriceSpan--1olt47v')]
            product_sizes = [item.text for item in soup.find_all(class_='ProductSize--64lzs8')]
            products = []
            for name, rating, price, size in zip(product_names, product_ratings, product_prices, product_sizes):
                size_start_index = size.find('Size:') + len('Size:')
                size_end_index = size.find('•') - 1
                size = size[size_start_index:size_end_index].strip()
                product_info = {
                    'name': name,
                    'rating': rating,
                    'price': price,
                    'size': size
                }
                products.append(product_info)
            return products
        else:
            print("Getting some error to fetch the data.")
