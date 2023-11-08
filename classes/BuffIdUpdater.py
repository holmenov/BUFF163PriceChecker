import os
import requests


class BuffIdUpdater:
    URL = "https://raw.githubusercontent.com/ModestSerhat/buff163-ids/main/buffids.txt"
    FILE_NAME = "goods_ids.txt"
    items_dict = {}

    def __init__(self):
        self.update_file_items_id()
        self.store_in_dict()

    def update_file_items_id(self):
        response = requests.get(BuffIdUpdater.URL)
        new_content = response.text
        if os.path.exists(BuffIdUpdater.FILE_NAME):
            with open(BuffIdUpdater.FILE_NAME, 'r', encoding="utf8") as file:
                existing_content = file.read()

            if existing_content != new_content:
                with open(BuffIdUpdater.FILE_NAME, 'w', encoding="utf8") as file:
                    file.write(new_content)
        else:
            with open(BuffIdUpdater.FILE_NAME, 'w', encoding="utf8") as file:
                file.write(new_content)

    def store_in_dict(self):
        with open(BuffIdUpdater.FILE_NAME, 'r', encoding="utf8") as file:
            for line in file:
                row = line.strip().split(';')
                item_id = row[0]
                item_name = row[1]
                self.items_dict[item_name] = item_id

    def search_id(self, item_list):
        id_list = []
        for item in item_list:
            id_list.append(self.items_dict.get(item))
        return id_list
