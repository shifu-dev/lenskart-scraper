import json
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

# get from source url of contact lenses
response = requests.get('https://www.lenskart.com/contact-lenses.html')

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    # extract the contact lens html page
    with open('contact_lenses.html', 'w', encoding='utf-8') as html_file:
        html_file.write(str(soup))
        print("HTML content has been written to 'contact_lenses.html' file.")
else:
    print("Failed to retrieve the webpage.")

# store the contact lens html page
with open('contact_lenses.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

# regex pattern to extract all the urls in the href of categories
pattern = '<h2 class=\"bold bgcolor123\">(.*?)</h2>.*?(<a.*?)</li>'

matches = re.findall(pattern, html_content, re.S)

contact_lens_dict_urls = {}

# dictionary creation of all urls with corresponding category name
for category, html_content in matches:
    url_regex_pattern = r'<a\s+href="([^"]+)">'
    temp_urls = re.findall(url_regex_pattern, html_content)
    contact_lens_dict_urls[category] = temp_urls

# loop through every url and get the ids of the specific category from
contact_lens_dict_ids = {}

# loop through every url from each category in the dictionary
for category in contact_lens_dict_urls:
    category_ids = []
    for each_category_url in contact_lens_dict_urls[category]:
        product_html = requests.get(each_category_url)
        # get id of each category
        each_category_id = re.findall(r"{\"pageProps\":{\"data\":{\"id\":(.*?),\"userData\":", product_html.text, re.S)
        if len(each_category_id) > 0:
            category_ids.append(each_category_id[0])
    contact_lens_dict_ids[category] = category_ids
    print('Got all cateory ids')
print(contact_lens_dict_ids)
for category_key in contact_lens_dict_ids:

    id = []
    model_name = []
    image_url = []
    size = []
    avgRating = []
    market_price = []
    lenscart_price = []
    color = []
    width = []
    totalNoOfRatings = []
    purchaseCount = []
    qty = []
    brand_name = []
    category_name = []

    # using the api get the product details from each category id
    for category_id in contact_lens_dict_ids[category_key]:
        url = f'https://api-gateway.juno.lenskart.com/v2/products/category/{category_id}?page-size=1000&page=0'
        response = requests.get(url)
        data = json.loads(response.content)
        if 'result' in data:
            length = len(data['result']["product_list"])

            for i in range(length):
                id.append(data['result']["product_list"][i]['id'])
                brand_name.append(data['result']["product_list"][i]['brand_name'])
                purchaseCount.append(data['result']["product_list"][i]['purchaseCount'])
                model_name.append(data['result']["product_list"][i]['model_name'])
                image_url.append(data['result']["product_list"][i]['image_url'])
                avgRating.append(data['result']["product_list"][i]['avgRating'])
                market_price.append(data['result']["product_list"][i]['prices'][0]['price'])
                lenscart_price.append(data['result']["product_list"][i]['prices'][1]['price'])
                qty.append(data['result']["product_list"][i]['qty'])

                # raw level cleaning data
                if 'category_name' in data['result']:
                    category_name.append(data['result']['category_name'])
                else:
                    category_name.append(None)

                if 'size' in data['result']["product_list"][i]:
                    size.append(data['result']["product_list"][i]['size'])
                else:
                    size.append(0)

                if 'color' in data['result']["product_list"][i]:
                    color.append(data['result']["product_list"][i]['color'])
                else:
                    color.append(None)

                if ('width') in data['result']["product_list"][i]:
                    width.append(data['result']["product_list"][i]['width'])
                else:
                    width.append(None)

                if ('totalNoOfRatings') in data['result']["product_list"][i]:
                    totalNoOfRatings.append(data['result']["product_list"][i]['totalNoOfRatings'])
                else:
                    totalNoOfRatings.append(0)

    # dynamically generate datasets from scrape data based on each contact lens category
    df = pd.DataFrame(
        {
            "id": id,
            "model_name": model_name,
            "brand_name": brand_name,
            f"{category_key}": category_name,
            "image_url": image_url,
            "market_price": market_price,
            "lenscart_price": lenscart_price,
            "purchaseCount": purchaseCount,
            "size": size,
            "color": color,
            "width": width,
            "totalNoOfRatings": totalNoOfRatings,
            "avgRating": avgRating,
            "quantity": qty
        }
    )

    # storing data sets as excel files
    df.to_excel(f'ContactLens-by-{category_key}.xlsx', index=False)