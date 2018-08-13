from mysql import connector
from time import sleep

from setting import settings

# TODO:Create a god function for read and write data.

def read_urls():
    try:
        # Edit setting.py if you need!
        db = connector.connect(**settings['mysql'])
        cr = db.cursor(buffered=True)
        query = 'SELECT url FROM {} WHERE tik=0'.format(settings['urls_table'])
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


def save_url(home_url):
    try:
        # Edit setting.py if you need!
        db = connector.connect(**settings['mysql'])
        cr = db.cursor()
        query = 'INSERT INTO {} VALUES ("{}", 0)'.format(settings['urls_table'], home_url)
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


def save_home(home):
    try:
        # Edit setting.py if you need!
        db = connector.connect(**settings['mysql'])
        cr = db.cursor()
        home['table'] = settings['homes_table']
        query = 'INSERT INTO {table} VALUES("{category}", "{neighbourhood}", {isCountryside}, {fare}, {area}, {fee}, {rooms}, "{hash}")'.format(**home)
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

def read_homes_hashes():
    try:
        # Edit setting.py if you need!
        db = connector.connect(**settings['mysql'])
        cr = db.cursor(buffered=True)
        query = 'SELECT hash FROM {}'.format(settings['homes_table'])
        try:
            cr.execute(query)
            db.commit()
            return [hash[0] for hash in cr.fetchall()]
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

def tik_url(url):
    try:
        # Edit setting.py if you need!
        db = connector.connect(**settings['mysql'])
        cr = db.cursor()
        query = 'UPDATE {} SET tik=1 WHERE url="{}"'.format(settings['urls_table'], url)
        try:
            cr.execute(query)
            db.commit()
            cr.close()
            db.close()
        except Exception as e:
            print("i can't insert <> into <> table :( \n".format(url, settings['urls_table'], ))
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