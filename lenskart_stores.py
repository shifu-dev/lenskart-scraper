import requests
from bs4 import BeautifulSoup

class Scraper:
    def scrape_store(url):
        response = requests.get(url)    
        soup = BeautifulSoup(response.content, 'html.parser')
        
        store_detail = {}

        store_detail["Store Name"] = soup.find('h1', class_='Home_name__J6U_a').text.strip()
        store_detail["Address"] = soup.find('div', class_='Home_wrapper__ARCSA').text.strip()
        timing_text = soup.find('div', class_='Home_infoBox__PV5Wz').text.strip()
        store_detail["Timing"] = timing_text.split('.Close')[1]
        store_detail["Service"] = soup.find_all('span', class_='Home_miniHead__KKq3S')[1].find_next_sibling().text.strip()
        tel_links = soup.find_all('a', href=lambda href: href and 'tel:' in href)
        store_detail["Phone Number"] = tel_links[1]['href'].split(':')[1]
        store_detail["Google Map Link"] = soup.find('a', href=lambda href: href and 'maps.google.com' in href)['href']
        review_count = soup.find('div', class_='Home_count__Y0nOJ').text.strip()
        rating = soup.find('div', class_='Home_rating__BaBug').text.strip()+review_count
        store_detail["Rating"] = rating

        nearby_stores = soup.find_all('div', class_='StoreCard_halfCard__X8eye')
        nearby_store_details = []
        for store in nearby_stores:
            nearby_store_name = store.find('div', class_='StoreCard_name__mrTXJ').find('span').text.strip()
            nearby_store_address = store.find('div', class_='storeDetials').find('span').text.strip()
            nearby_store_distance= nearby_store_address.split('.')[1:][0]
            nearby_store_details.append({
                "Store Name": nearby_store_name,
                "Distance": nearby_store_distance
            })

        store_detail["Nearby Stores"] = nearby_store_details
        
        return store_detail

# store_info = Scraper.scrape_store('https://www.lenskart.com/stores/lenskart-com-chhatarpur-mehrauli-new-delhi-136896/Home')
# print(store_info)
