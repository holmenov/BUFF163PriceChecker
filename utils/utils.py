import pandas as pd
import pyperclip

def write_to_csv(items_data: dict):
    df = pd.DataFrame(items_data['items'])
    df = df.rename(columns={'item_name': 'Item Name', 'price': 'Price'})
    df.to_excel('prices.xlsx', sheet_name='Prices', index=False)

def copy_in_clipboard(items_data: dict):
    items = items_data['items']
    all_prices = ''
    for price in items:
        price = str(price['price']).replace('.', ',')
        all_prices = all_prices + price + '\n'
    pyperclip.copy(all_prices)