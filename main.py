import asyncio
import aiohttp

from classes.BUFF163Checker import BUFF163Checker
from classes.BUFF163IDs import BUFF163IDs
from classes.GoogleTable import GoogleTable
from utils.utils import *
from config import COPY_TO_CLIPBOARD, CREATE_XLSX, SLICE


async def main():
    prices_manager = BUFF163Checker()
    buff_id_updater = BUFF163IDs()
    google_tables = GoogleTable()
    
    items_list = google_tables.read_from_table()
    item_id_list = buff_id_updater.search_id(items_list)    
    
    async with aiohttp.ClientSession() as session:
        tasks = [prices_manager.check_prices(session, item_id, SLICE) for item_id in item_id_list]
        items_data = await asyncio.gather(*tasks)
    
    items_data = {'items': items_data}

    google_tables.write_to_table(items_data)
    
    if COPY_TO_CLIPBOARD: copy_in_clipboard(items_data)
    if CREATE_XLSX: write_to_csv(items_data)

if __name__ == "__main__":  
    asyncio.run(main())