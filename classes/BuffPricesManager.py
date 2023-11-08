import time
import urllib
import pandas as pd
import requests
import pyperclip

from classes.BuffIdUpdater import BuffIdUpdater
from classes.ResultSender import GoogleTable
from classes.BeautifulLogs import logger

from config import *

class BuffPricesManager:
    def __init__(self):
        self.BuffIdUpdater = BuffIdUpdater()

    def fetch_sell_prices(self, item_id, num_offers_to_check):
        base_url = f"https://buff.163.com/api/market/goods/"
        params = {
            "game": "csgo",
            "page_num": "1",
            "goods_id": item_id
        }
        sell_url = base_url + 'sell_order' + '?' + urllib.parse.urlencode(params)
        
        try:
            resp = requests.get(sell_url).json()
        except requests.exceptions.JSONDecodeError:
            logger.warning('Requests limit. Sleep 5 seconds.')
            time.sleep(5)
            return self.fetch_sell_prices(item_id, num_offers_to_check)
        
        if len(resp["data"]["items"]) == 0:
            logger.warning(f"Not offers found for item with id: {item_id}")
        else:
            item_name = resp["data"]["goods_infos"][item_id]["market_hash_name"]
            items = resp["data"]["items"][:num_offers_to_check]
            for item in items:
                price = float(item["price"])
                item_data = {"item_name": item_name, "price": price}
            return item_data

    def write_to_csv(self, items_data: dict):
        df = pd.DataFrame(items_data['items'])
        df = df.rename(columns={'item_name': 'Item Name', 'price': 'Price'})
        df.to_excel('prices.xlsx', sheet_name='Prices', index=False)

    def copy_in_clipboard(self, items_data):
        items = items_data['items']
        all_prices = ''
        for price in items:
            price = str(price['price']).replace('.', ',')
            all_prices = all_prices + price + '\n'
        pyperclip.copy(all_prices)

    def run(self):
        google_tables = GoogleTable()
        items_list = google_tables.read_from_table()
        item_id_list = self.BuffIdUpdater.search_id(items_list)
        items_data = {'items': []}

        for item_id in item_id_list:
            item_data = self.fetch_sell_prices(item_id, 1)
            items_data['items'].append(item_data)
            logger.success(f"Successfully checked the item: {item_data['item_name']}")
        
        google_tables.write_to_table(items_data)
        
        if COPY_TO_CLIPBOARD: self.copy_in_clipboard(items_data)
        if CREATE_XLSX: self.write_to_csv(items_data)