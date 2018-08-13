import re
from time import sleep
from urllib.parse import urljoin

from selenium import webdriver
from bs4 import BeautifulSoup as bs
from mysql import connector

from setting import settings

def read_urls():
    try:
        # Edit setting.py if you need!
        db = connector.connect(**settings['mysql'])
        cr = db.cursor(buffered=True)
        query = 'SELECT * FROM {};'.format(settings['urls_table'])
        try:
            cr.execute(query)
            db.commit()
            return [url[0] for url in cr.fetchall()]
        except Exception as e:
            print("i can't select urls form <{}> table :( \n".format(settings['urls_table'], ))
            print(e)
            db.rollback()
            cr.close()
            db.close()
            sleep(5)
            exit()

    except Exception as e:
        print("i can't connect to <{}> database :( \n".format(settings['mysql']['database']))
        print(e)
        sleep(5)
        exit()



def save(home_url):
    try:
        # Edit setting.py if you need!
        db = connector.connect(**settings['mysql'])
        cr = db.cursor()
        query = 'INSERT INTO {} VALUES("{}")'.format(settings['urls_table'], home_url)
        try:
            cr.execute(query)
            db.commit()
            cr.close()
            db.close()
        except Exception as e:
            print("i can't insert <> into <> table :( \n".format(home_url, settings['urls_table'], ))
            print(e)
            db.rollback()
            cr.close()
            db.close()
            sleep(5)
            exit()

    except Exception as e:
        print("i can't connect to <{}> database :( \n".format(settings['mysql']['database']))
        print(e)
        sleep(5)
        exit()

def main():
    old_links = read_urls()
    browser = webdriver.Firefox()
    browser.get('https://divar.ir/tehran/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/browse/%D8%A7%D8%AC%D8%A7%D8%B1%D9%87-%D9%85%D8%B3%DA%A9%D9%88%D9%86%DB%8C-%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86-%D8%AE%D8%A7%D9%86%D9%87-%D8%B2%D9%85%DB%8C%D9%86/%D8%A7%D9%85%D9%84%D8%A7%DA%A9-%D9%85%D8%B3%DA%A9%D9%86/')

    for i in range(2): # 5 times = 3 page (3 * 48 home)
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        sleep(1)
    page_source = browser.page_source
    soup = bs(page_source, 'html.parser')
    homes_links = soup.select('.post-card-link')
    for home_link in homes_links:
        home_link = home_link['href']
        home_link = re.search(r'\/([\w\-]+)$', home_link).group(1)
        home_link = urljoin('http://divar.ir/v/', home_link)
        if home_link not in old_links:
            save(home_link)

main()