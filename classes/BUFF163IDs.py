import os
import requests


class BUFF163IDs:
    URL = "https://raw.githubusercontent.com/ModestSerhat/buff163-ids/main/buffids.txt"
    FILE_NAME = "goods_ids.txt"
    items_dict = {}

    def __init__(self):
        self.update_file_items_id()
        self.store_in_dict()

    def update_file_items_id(self):
        response = requests.get(BUFF163IDs.URL).text

        if os.path.exists(BUFF163IDs.FILE_NAME):
            with open(BUFF163IDs.FILE_NAME, 'r', encoding="utf8") as file:
                existing_content = file.read()

            if existing_content != response:
                with open(BUFF163IDs.FILE_NAME, 'w', encoding="utf8") as file:
                    file.write(response)

        else:
            with open(BUFF163IDs.FILE_NAME, 'w', encoding="utf8") as file:
                file.write(response)

    def store_in_dict(self):
        with open(BUFF163IDs.FILE_NAME, 'r', encoding="utf8") as file:
            for line in file:
                row = line.strip().split(';')
                item_id, item_name = row[0], row[1]
                self.items_dict[item_name] = item_id

    def search_id(self, item_list):
        id_list = [self.items_dict.get(item) for item in item_list]
        return id_list