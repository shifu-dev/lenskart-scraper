from bs4 import BeautifulSoup
import requests
import json

class details:
    brand_name = ""
    product_type = ""
    frame_type = ""
    frame_shape = ""
    collection = ""
    frame_size = ""
    price = 0
    coupon_code = ""
    rating = ""
    weight_group = ""
    material = ""
    product_warranty = ""
    gender = "" 
    purchase_count = 0
    product_quantity = 0

    def __str__(self) -> str:
        result = (
            f"Brand Name: {self.brand_name}\n"
            f"Product Type: {self.product_type}\n"
            f"Frame Type: {self.frame_type}\n"
            f"Frame Shape: {self.frame_shape}\n"
            f"Collection: {self.collection}\n"
            f"Frame Size: {self.frame_size}\n"
            f"Price: {self.price}\n"
            f"Coupon Code: {self.coupon_code}\n"
            f"Rating: {self.rating}\n"
            f"Weight Group: {self.weight_group}\n"
            f"Material: {self.material}\n"
            f"Product Warranty: {self.product_warranty}\n"
            f"Gender: {self.gender}\n"
            f"Purchase Count: {self.purchase_count}\n"
            f"Product Quantity: {self.product_quantity}\n"
        )
        return result


class scraper:
    def scrap(self,url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            data = json.loads(script_tag.string)
            
            product_data = data['props']['pageProps']['data']['productDetailData']
            technical_product_info = product_data['technicalProductInfo']
            general_product_info = product_data['generalProductInfo']
            
            brand_name = next((item['value'] for item in technical_product_info if item['name'] == 'Brand Name'), None)
            product_type = next((item['value'] for item in technical_product_info if item['name'] == 'Product Type'), None)
            frame_type = next((item['value'] for item in technical_product_info if item['name'] == 'Frame Type'), None)
            frame_shape = next((item['value'] for item in technical_product_info if item['name'] == 'Frame Shape'), None)

            collection = next((item['value'] for item in general_product_info if item['name'] == 'Collection'), None)
            frame_size = next((item['value'] for item in general_product_info if item['name'] == 'Frame Size'), None)
            weight_group = next((item['value'] for item in general_product_info if item['name'] == 'Weight Group'), None)
            material = next((item['value'] for item in general_product_info if item['name'] == 'Material'), None)
            product_warranty = next((item['value'] for item in general_product_info if item['name'] == 'Product Warranty'), None)
            gender = next((item['value'] for item in general_product_info if item['name'] == 'Gender'), None)

            price = product_data['price']['basePrice']
            rating = product_data['productRating']
            purchase_count = product_data['purchaseCount']
            product_quantity = product_data['productQuantity']

            details.brand_name = brand_name
            details.product_type = product_type
            details.frame_type = frame_type
            details.frame_shape = frame_shape
            details.collection = collection
            details.frame_size = frame_size
            details.price = price
            details.coupon_code = ""
            details.rating = rating
            details.weight_group = weight_group
            details.material = material
            details.product_warranty = product_warranty
            details.gender = gender
            details.purchase_count = purchase_count
            details.product_quantity = product_quantity

            return details