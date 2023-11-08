import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import *

class GoogleTable:
    SHEET_ID = 1
    
    def __init__(self) -> None:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            AUTH_FILE,
            ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(credentials)
        self.worksheet = gc.open_by_url(TABLE_URL).get_worksheet(self.SHEET_ID)
    
    def read_from_table(self) -> list:
        values = self.worksheet.get(CELLS_SKINS)
        values = [value for row in values for value in row]
        return values
        
    def write_to_table(self, items_data: dict):
        items = items_data['items']
        price_list = []
        for item in items:
            price = str(item['price']).replace('.', ',')
            price_list.append([price])
        
        self.worksheet.update(CELLS_PRICE, price_list, value_input_option="USER_ENTERED")