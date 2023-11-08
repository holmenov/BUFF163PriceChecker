# BUFF163 Price Updater

With this code you will be able to automatically read the names of CS:GO skins from your Google Sheets and enter the prices on the [Buff163](https://buff.163.com) service into the same Google Sheets.

## Installation

1. Install Python 3.11 or later
2. Clone the repository and write this command in the software folder: `pip install -r requiments.txt`
3. Get your [Google account access key](https://console.cloud.google.com) in JSON format and paste it into the folder with the software.
4. [Here](https://console.cloud.google.com/apis/credentials) get your service account email and add this email as an editor to your Google Sheets.
5. Set up the `config.py` and run the `main.py`.

## Settings

- `TABLE_URL` - Your link to the Google Sheets.
- `SHEET_ID` - Your Sheet ID from the table.
- `CELLS_SKINS` - Cells with names of CS:GO skins.
- `CELLS_PRICE` - Cells with prices of CS:GO skins.
- `AUTH_FILE` - The name of your Google authorization key.
- `CREATE_XLSX` - Create an xlsx file in the software folder.
- `COPY_TO_CLIPBOARD` - Copy results to clipboard.