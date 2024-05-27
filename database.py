import sqlite3
import random

id_to_num = dict()



def get_id_value(choice):
    global id_to_num
    chosen_id = 0
    for k, v in id_to_num.items():
        if v == choice:
            chosen_id = k
    return chosen_id


def create_table():
    con = sqlite3.connect('db.sql3')
    cur = con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS 
            movies (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, type TEXT, 
            description TEXT)
    ''')
    con.commit()
    con.close()


# def add_my_movies():
#     con = sqlite3.connect('db.sql3')
#     cur = con.cursor()
#     movies = [
#         ('Мгла', 'триллер', 'Маленький городок накрывает сверхъестественный туман, отрезая людей от внешнего мира'),
#         ('Митчеллы против машин', 'мультфильм', 'искусственный интеллект вдруг начинает восстание машин.'),
#         ('Анатомия падения', 'драма', 'Известную писательницу обвиняют в убийстве мужа'),
#         ('Рождённый стать королём', 'фэнтези', 'Подросток находит Эскалибур'),
#         ('Укрытие', 'сериал', 'Люди живут в бункере'),
#         ('Загадочная история Бенджамина Баттона', 'драма', 'Мужчина рождается старым и молодеет'),
#         ('Звук свободы', 'триллер', 'Спецагент пытается раскрыть сеть по торговле детьми.'),
#         ('Принцесса Мононоке', 'аниме', 'принцесса Мононоке - повелительница зверей и дочь волчицы'),
#         ('Кролик Джо Джо', 'драма', 'Воображаемый друг мальчика - Гитлер, а его мама прячет еврейку')
#     ]
#     cur.executemany('''
#     INSERT INTO movies (name, type, description)
#     VALUES (?, ?, ?)
#     ''', movies)
#     con.commit()
#     con.close()


# def get_all_movies(offset=0, limit=5):
#     con = sqlite3.connect('db.sql3')
#     cur = con.cursor()
#     cur.execute('SELECT * FROM movies LIMIT ? OFFSET ?', (limit, offset))
#     movies = cur.fetchall()
#     con.close()
#     global id_to_num
#     id_to_num = {k: v for k, v in zip([el[0] for el in movies], [x for x in range(1, len(movies) + 1)])}
#     res = ''
#     for el in movies:
#         res += f"{id_to_num[el[0]]}. Название: \"{el[1]}\"\nЖанр: {el[2]}\nОписание: {el[3]}\n\n"
#
#     return res, len(movies) == limit


def get_random_movie():
    con = sqlite3.connect('db.sql3')
    cur = con.cursor()
    cur.execute('SELECT * FROM movies')
    movies = cur.fetchall()
    global id_to_num
    id_to_num = {k: v for k, v in zip([el[0] for el in movies], [x for x in range(1, len(movies) + 1)])}
    res = ''
    indices = list(id_to_num.keys())
    chosen_id = random.choice(indices)
    for i, el in enumerate(movies):
        if el[0] == chosen_id:
            res += f"Название: \"{el[1]}\"\nЖанр: {el[2]}\nОписание: {el[3]}\n\n"
    con.close()
    return res, chosen_id


def get_movies():
    con = sqlite3.connect('db.sql3')
    cur = con.cursor()
    cur.execute('SELECT * FROM movies')
    movies = cur.fetchall()
    global id_to_num
    id_to_num = {k: v for k, v in zip([el[0] for el in movies], [x for x in range(1, len(movies) + 1)])}
    res = ''
    for i, el in enumerate(movies):
        res += f"{id_to_num[el[0]]}. Название: \"{el[1]}\"\nЖанр: {el[2]}\nОписание: {el[3]}\n\n"
        con.close()
    return res


def get_movie_id(choice):
    con = sqlite3.connect('db.sql3')
    cur = con.cursor()
    chosen_id = get_id_value(choice)
    cur.execute('SELECT name FROM movies WHERE id=?', (chosen_id, ))
    movie = cur.fetchone()
    con.close()
    return movie[0] if movie else None


def add_new_movie(lst):
    con = sqlite3.connect('db.sql3')
    cur = con.cursor()
    cur.execute('INSERT INTO movies(name, type, description) VALUES(?, ?, ?)', lst)
    con.commit()
    con.close()


def delete_movie(choice):
    con = sqlite3.connect('db.sql3')
    cur = con.cursor()
    chosen_id = get_id_value(choice)
    cur.execute('DELETE FROM movies WHERE id == ?', (chosen_id,))
    con.commit()
    con.close()

