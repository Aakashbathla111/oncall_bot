import schedule
import time
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta


def hit_curl():
    context = getcontext()
    url = "https://api.flock.com/hooks/sendMessage/b1520c67-2f57-47e9-bb75-651c632dd78d"
    headers = {'Content-Type': 'application/json'}
    json_payload = {
        "text": context
    }
    response = requests.post(url, headers=headers, json=json_payload)


def getcontext():
    json_keyfile_path = '/Users/int-aakash.a/Downloads/oncalls-dev-b02f4d031c62.json'

# Connect to Google Sheets using service account credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    gc = gspread.authorize(credentials)

# Replace 'your_spreadsheet_key' with the key of your Google Spreadsheet
    spreadsheet_key = '1BrQxNhXigEgf0o8QNkX7iX3ZODw3CjOhRBmHTJKWWOg'

# Open the Google Spreadsheet using its key
    workbook = gc.open_by_key(spreadsheet_key)

    worksheet = workbook.sheet1
    columns_to_read = ['Date', 'T1', 'T2'] 

    df = pd.DataFrame(worksheet.get_all_records(empty2zero=False), columns = columns_to_read)
    today = datetime.today()
    if today.weekday() == 1:
        target_date = today.strftime('%Y-%m-%d')
    else:
        days_since_last_tuesday = (today.weekday() - 1) % 7
    previous_tuesday = today - timedelta(days=days_since_last_tuesday)
    target_date = previous_tuesday.strftime('%Y-%m-%d')
    index_of_date = df['Date'].index[df['Date'] == target_date].tolist()

    if index_of_date:
        index = index_of_date[0]
    # Get the value in the 'People' column at the found index
        people_value1 = df.loc[index, 'T1']
        people_value2 = df.loc[index, 'T2']
        context = 'Oncalls devs for today are ' + people_value1 + '(L1), ' + people_value2 + '(L2)'
    else:
        context = 'Spreadsheet needs  to be updated'
    return context


# schedule.every().day.at("22:21").do(hit_curl)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

