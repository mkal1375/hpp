from mysql import connector
from time import sleep

from setting import settings


def read_urls():
    try:
        # Edit setting.py if you need!
        db = connector.connect(**settings['mysql'])
        cr = db.cursor(buffered=True)
        query = 'SELECT * FROM {}'.format(settings['urls_table'])
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


def save_urls(home_url):
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