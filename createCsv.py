import requests
import csv

url = 'https://api.gatcg.com/cards/search'
page = 1
prefix = "AMB"

params = {}

data = []

print("--> Retrieving data ...")

while True:
    params['page'] = page

    res = requests.get(url, params=params)

    if res.status_code != 200:
        print(f"Error getting data")
        break
    
    page_data = res.json()

    for item in page_data.get('data', []):
        for edition in item.get('result_editions', []):
            filtered_item = {
                'set': edition.get('set', {}).get('name', 'N/A'),
                'collector_number': edition.get('collector_number', 'N/A'),
                'name': edition.get('name'),
                'slug': edition.get('slug'),
                'rarity': edition.get('rarity'),
                'illustrator': edition.get('illustrator', 'N/A')
            }
            data.append(filtered_item)

        for edition in item.get('editions', []):
            filtered_item = {
                'set': edition.get('set', {}).get('name', 'N/A'),
                'collector_number': edition.get('collector_number', 'N/A'),
                'name': edition.get('name'),
                'slug': edition.get('slug'),
                'rarity': edition.get('rarity'),
                'illustrator': edition.get('illustrator', 'N/A')
            }
            data.append(filtered_item)

    if not page_data.get('has_more', False):
        break

    print("Page", params.get('page'))

    page += 1

with open('cards_data.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['set', 'collector_number', 'name', 'slug', 'rarity', 'illustrator']    
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
        
print("Output: ", file.name)
