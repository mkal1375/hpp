import re

from bs4 import BeautifulSoup as bs
import requests
from unidecode import unidecode
from sql_command import read_urls


def price_to_int(price):
    new_price = price
    new_price = unidecode(price)
    try:
        return int(re.search('([\d\.]+)', new_price).group(1).replace('.', ''))
    except:
        return price

def main():
    #  Get all saved urls.
    urls = read_urls()
    for url in urls:
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        soup = soup.find('body')
        items = [item.text for item in soup.select('.value')][2:]
main()
