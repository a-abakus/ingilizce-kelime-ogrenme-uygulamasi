from sqlite3 import connect
from os.path import join


def db_connection(db):
    connection = connect(db)
    return connection.cursor(), connection


cursor, c = db_connection(join('assets', 'database', 'wpd.db'))


def connection_close():
    c.close()


def rand_query():
    q = 'SELECT kelime, anlam, fonetik_en, fonetik_us FROM kelimeler ORDER BY RANDOM() LIMIT 1'
    result = cursor.execute(q).fetchone()
    return result


def select_query(word, x):
    if x == 0:
        q = f"SELECT fonetik_en, fonetik_us FROM kelimeler WHERE kelime='{word}'"
        result = cursor.execute(q).fetchall()
        results = []
        [results.extend(list(row)) for row in result]
    else:
        q = f"SELECT fonetik_en, fonetik_us FROM kelimeler WHERE anlam='{word}'"
        result = cursor.execute(q).fetchall()
        results = []
        [results.extend(list(row)) for row in result]
    return results


def word_is_exist(word, x):
    if x == 0:
        q = f"SELECT * FROM kelimeler WHERE kelime = '{word}'"
        result = cursor.execute(q).fetchall()
        results = []
        [results.extend(list(row)) for row in result]
    else:
        q = f"SELECT * FROM kelimeler WHERE anlam = '{word}'"
        result = cursor.execute(q).fetchall()
        results = []
        [results.extend(list(row)) for row in result]
    return results


def check_word(word):
    q = f"SELECT * FROM kelimeler WHERE kelime = '{word}'"
    result = cursor.execute(q).fetchall()
    if len(result) == 0 or result is None:
        q = f"SELECT * FROM kelimeler WHERE anlam = '{word}'"
        cursor.execute(q)
        return 'anlam'
    return 'kelime'


def add_phon(word, pho_s):
    res = check_word(word)
    if res == 'kelime':
        insert_query = f"UPDATE kelimeler SET fonetik_en='{pho_s[0]}'," \
                       f"fonetik_us='{pho_s[1]}' WHERE kelime ='{word}'"
        cursor.execute(insert_query)
    else:
        insert_query = f"UPDATE kelimeler SET fonetik_en='{pho_s[0]}'," \
                       f"fonetik_us='{pho_s[1]}' WHERE anlam ='{word}'"
        cursor.execute(insert_query)
