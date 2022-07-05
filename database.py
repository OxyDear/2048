import sqlite3

bd = sqlite3.connect('2048.sqlite')
cur = bd.cursor()

cur.execute('''
CREATE TABLE if not exists records
(name text, score integer)
''')


def get_best():
    cur.execute('''
    SELECT name gamer, max(score) score from records
    GROUP by name
    ORDER by score DESC
    limit 3
    ''')
    return cur.fetchall()

