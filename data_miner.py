import hashlib
import re
from bs4 import BeautifulSoup as bs
import requests
from unidecode import unidecode

from sql_command import read_urls, save_home, read_homes_hashes, tik_url


def price_to_int(price):
    new_price = unidecode(price)
    try:
        return int(re.search('([\d\.]+)', new_price).group(1).replace('.', ''))
    except:
        return price


def create_dataset(data):
    try:
        dataset = dict()
        data[1] = data[1].replace('تهران', '', 1).replace('\u200c', ' ').strip()
        dataset['category'] = data[0]
        dataset['neighbourhood'] = data[1]

        if 'هست' in data:
            dataset[' '] = True
        else:
            dataset['isCountryside'] = False

        if data[-1] == 'مجانی':
            dataset['fare'] = 0
        else:
            dataset['fare'] = price_to_int(data[-1])
        dataset['area'] = int(unidecode(data[-2]))

        for item in data[3:-2]:
            if 'تومان' in item:
                item = price_to_int(item)
                dataset['fee'] = item
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
                dataset['rooms'] = rooms[item]

        if len(dataset) == 7:
            return dataset
        else:
            return None
    except Exception as e:
        return None


old_hashes = read_homes_hashes()
def save(home):
    hash = hashlib.sha256(str(home).encode('utf-8')).hexdigest()
    if hash not in old_hashes:
        home['hash'] = hash
        save_home(home)
        return True
    else:
        return False


def main():
    #  Get all saved urls.
    urls = read_urls()
    for url in urls[:5]:
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        soup = soup.find('body')
        items = [item.text for item in soup.select('.value')][2:]
        home = create_dataset(items)
        if home is not None:
            save(home)
        tik_url(url)
main()
