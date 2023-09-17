import sqlite3
import json


connection = sqlite3.connect('wpd.db')
cursor = connection.cursor()


def create_db():
    create_table_query = """
    CREATE TABLE kelimeler (
        id INTEGER PRIMARY KEY,
        kelime TEXT,
        anlam TEXT,
        fonetik_en TEXT,
        fonetik_us TEXT
    )
    """
    cursor.execute(create_table_query)


def drop_table():
    drop_table_query = """
    DROP TABLE kelimeler
    """
    cursor.execute(drop_table_query)
    create_db()


def add_word():
    try:
        with open('dictionary.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for kelime, anlam in data.items():
                try:
                    insert_query = 'INSERT INTO kelimeler (kelime, anlam) VALUES (?, ?)'
                    cursor.execute(insert_query, (kelime, anlam))
                except sqlite3.Error as e:
                    print("Veritabanı hatası:", e)
            connection.commit()
    except sqlite3.Error as e:
        print("Veritabanı hatası:", e)
    finally:
        connection.close()


if __name__ == '__main__':
    try:
        create_db()
        add_word()
    except:
        drop_table()
        add_word()
