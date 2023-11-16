import aiohttp
from aiohttp.client_exceptions import ContentTypeError
import asyncio
from urllib.parse import urlencode
from loguru import logger

from classes.BUFF163IDs import BUFF163IDs


class BUFF163Checker:
    def __init__(self) -> None:
        self.BUFF163IDs = BUFF163IDs()

    async def export_data(self, data: dict, item_id: int, slicing: int) -> (str, float):
        if len(data["data"]["items"]) == 0:
                logger.warning(f"Not offers found for item with id: {item_id}")

        else:
            item_name = str(data["data"]["goods_infos"][item_id]["market_hash_name"])

            items = data["data"]["items"][:slicing]

            items_prices = [float(item['price']) for item in items]

            avg_price = round(sum(items_prices) / len(items_prices), 2)

            return item_name, avg_price

    async def check_prices(self, session: aiohttp.ClientSession, item_id: int, slicing: int) -> dict:
        base_url = 'https://buff.163.com/api/market/goods/'
        params = {
            'game': 'csgo',
            'page_num': '1',
            'goods_id': item_id
        }

        sell_url = f'{base_url}sell_order?{urlencode(params)}'

        async with session.get(sell_url) as response:
            try:
                data = await response.json()
            except ContentTypeError:
                await asyncio.sleep(1)
                return await self.check_prices(session, item_id, slicing)

            item_name, avg_price = await self.export_data(data, item_id, slicing)
            item_data = {"item_name": item_name, "price": avg_price}
            
            logger.success(f"Successfully checked the item: {item_data['item_name']}")
            
            return item_data