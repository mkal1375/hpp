import re
from bs4 import BeautifulSoup as bs
import requests
from unidecode import unidecode

from sql_command import read_urls


def price_to_int(price):
    new_price = unidecode(price)
    try:
        return int(re.search('([\d\.]+)', new_price).group(1).replace('.', ''))
    except:
        return price


def create_dataset(data):
    try:
        dataset = []
        data[1] = data[1].replace('تهران', '').replace('\u200c', ' ').strip()
        dataset.append(data[0])
        dataset.append(data[1])

        if 'هست' in data:
            dataset.append(True)
        else:
            dataset.append(False)

        if data[-1] == 'مجانی':
            dataset.append(0)
        else:
            dataset.append(price_to_int(data[-1]))

        dataset.append(int(unidecode(data[-2])))

        for item in data[3:-2]:
            if 'تومان' in item:
                item = price_to_int(item)
                dataset.append(item)
                break

        rooms= {
            'بدون اتاق': 0,
            'یک': 1,
            'دو': 2,
            'سه': 3,
            'چهار': 4,
            'پنج و بیشتر': 5
        }
        for item in data:
            if item in rooms.keys():
                dataset.append(rooms[item])

        if len(dataset) == 7:
            return dataset
        else:
            return None
    except Exception as e:
        return None

datasets = []


def main():
    #  Get all saved urls.
    urls = read_urls()
    for url in urls[:20]:
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        soup = soup.find('body')
        items = [item.text for item in soup.select('.value')][2:]
        dataset = create_dataset(items)
        if dataset:
            datasets.append(dataset)
main()
