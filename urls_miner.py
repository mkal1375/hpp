import re
from time import sleep
from urllib.parse import urljoin

from selenium import webdriver
from bs4 import BeautifulSoup as bs

from sql_command import read_urls, save_url

# TODO: Now every call function read html page from begin but it no need. if every time we send to it new part of page source!
def get_urls(old_urls, page_source):
    counter = 0
    new_urls = []
    soup = bs(page_source, 'html.parser')
    homes_links = soup.select('.post-card-link')
    for home_link in homes_links:
        home_link = home_link['href']
        home_link = re.search(r'\/([\w\-]+)$', home_link).group(1)
        home_link = urljoin('http://divar.ir/v/', home_link)
        if home_link not in old_urls['database']:
            if home_link not in old_urls['running']:
                save_url(home_link)
                new_urls.append(home_link)
                counter += 1
        else:
            return False, counter, new_urls
    return True, counter, new_urls


def main():
    flag = True
    counter = 0
    browser = webdriver.Firefox()
    browser.get(
        'https://divar.ir/tehran/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/browse/%D8%A7%D8%AC%D8%A7%D8%B1%D9%87-%D9%85%D8%B3%DA%A9%D9%88%D9%86%DB%8C-%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86-%D8%AE%D8%A7%D9%86%D9%87-%D8%B2%D9%85%DB%8C%D9%86/%D8%A7%D9%85%D9%84%D8%A7%DA%A9-%D9%85%D8%B3%DA%A9%D9%86/')
    old_urls = dict()
    old_urls['database'] = read_urls()
    old_urls['running'] = []
    while flag and counter <= 1000:
        for i in range(3):
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            sleep(1)
        result, this_counter, new_urls = get_urls(old_urls, browser.page_source)
        old_urls['running'].extend(new_urls)
        if not result:
            flag = False
        else:
            counter += this_counter
        print('result: {} / counter: {} / all: {}'.format(result, this_counter, counter))
    browser.close()
    print('mining is over!')
main()
