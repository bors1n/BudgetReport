import json
import requests

import pandas as pd

#подключение к ноушен
file = open('/Users/bors1n/DataspellProjects/dsProject/budget_report/api_key.json')
#file = open('/home/admin/projects/budgeting_report/BudgetReport/api_key.json')
data = json.load(file)
#мой секретный токен
secret = data['secret_key']
#database id
database = data['database_id']
file.close()

headers = {
    "Authorization": f"Bearer {secret}",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json"
}

url = f"https://api.notion.com/v1/databases/{database}/query"
print(url)

r = requests.post(url, headers=headers)

db = r.json()

#Собираею csv файл.

data_dict = {
    'Category': [],
    'Amount': [],
    'Date': [],
    'Type': [],
    'Description': []
}

for i in range(len(db['results'])):

    category = db['results'][i]['properties']['Category']['multi_select'][0]['name']
    amount = db['results'][i]['properties']['Amount']['number']
    date = db['results'][i]['properties']['Date']['date']['start']
    type = db['results'][i]['properties']['Type']['select']['name']
    description = db['results'][i]['properties']['Description ']['title'][0]['text']['content']

    data_dict['Category'].append(category)
    data_dict['Amount'].append(amount)
    data_dict['Date'].append(date)
    data_dict['Type'].append(type)
    data_dict['Description'].append(description)

all_data = pd.DataFrame(data_dict)
all_data.to_csv('/Users/bors1n/DataspellProjects/dsProject/budget_report/all_data.csv')
#all_data.to_csv('/home/admin/projects/budgeting_report/BudgetReport/all_data.csv')
print('done')
