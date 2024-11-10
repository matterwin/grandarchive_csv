import requests
import csv

page = 1
prefix = "AMB"

url = 'https://api.gatcg.com/cards/search'
params = {'prefix': prefix}

data = []

print("--> Retrieving data ...")

while True:
    params['page'] = page

    res = requests.get(url, params=params)

    if res.status_code != 200:
        print(f"Error getting data")
        break
    
    page_data = res.json()
    data.extend(page_data.get('data', []))

    if not page_data.get('has_more', False):
        break

    page += 1

with open('cards_data.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['collector_number', 'name', 'slug', 'illustrator']    
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for item in data:
        illustrator = item.get('result_editions', [{}])[0].get('illustrator', 'N/A')
        collector_number = item.get('result_editions', [{}])[0].get('collector_number', 'N/A')
        
        writer.writerow({
            'collector_number': collector_number, 
            'name': item.get('name'), 
            'slug': item.get('slug'), 
            'illustrator': illustrator
        })
        
print("Output: ", file.name)
