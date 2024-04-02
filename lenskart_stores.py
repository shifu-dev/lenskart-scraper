import requests
from bs4 import BeautifulSoup

#states_list = ['Andhra Pradesh', 'Andaman and Nicobar', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chennai', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Delhi', 'Goa', 'Gujarat', 'Gwalior', 'Haryana', 'Himachal Pradesh', 'Hyderabad', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Nagaland', 'New Delhi', 'Odisha', 'Patna', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']


def scrape_lenskart_stores(url):
    
    #urlformat: 'https://www.lenskart.com/stores/location/' + state
    
    all_stores = []
    state = url.split('/')[-1]
    
    response = requests.get(url)    
    soup = BeautifulSoup(response.content, 'html.parser')
    stores=soup.find_all('div', class_='StoreCard_imgContainer__P6NMN')
    
    for store in stores:
        name = store.find('a', {'class' : "StoreCard_name__mrTXJ"}).text
        address = store.find('a', {'class' : 'StoreCard_storeAddress__PfC_v'}).text
        timings = store.find('div', {'class' : 'StoreCard_storeAddress__PfC_v'}).text[7:-1]
        phone = store.find('div', {'class' : "StoreCard_wrapper__xhJ0A"}).a.text[1:]
        rating = store.find('div', {'class' : 'StoreCard_storeRating__dJst3'}).text.strip()

        #(['State', 'Area Name', 'Address', 'Timings', 'Phone', 'Rating'])
        all_stores.append((state, name, address,  timings, phone, rating))
    
    #returns the list of all stores in the given state
    return all_stores




