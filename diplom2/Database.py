import sqlalchemy
import json

PASSWORD = 'пароль'


def create_bd():

    """ создание базы данных """

    try:
        engine = sqlalchemy.create_engine(f"postgresql://postgres:{PASSWORD}@localhost:5432/postgres")
        connection = engine.connect()
        connection.execute('''COMMIT''')
        connection.execute('''CREATE DATABASE users''')
        create_tables()
    except sqlalchemy.exc.ProgrammingError:
        pass


def get_connect():

    """ установка соединения с БД """

    engine = sqlalchemy.create_engine(f'postgresql://postgres:{PASSWORD}@localhost:5432/users')
    connection = engine.connect()
    return connection


def create_tables():

    """ создание таблиц """

    con = get_connect()

    con.execute('''CREATE TABLE IF NOT EXISTS Bots_user (
        id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL UNIQUE);''')

    con.execute('''CREATE TABLE IF NOT EXISTS User_vk_id (
        id SERIAL PRIMARY KEY,
        vk_id INTEGER NOT NULL,
        bot_user_id INTEGER REFERENCES Bots_user(id));''')  # unique не будем ставить т.к. разным пользователям могут
                                                            # попасться одинаковые странички

    con.execute('''CREATE TABLE IF NOT EXISTS Photo (
        id SERIAL PRIMARY KEY,
        photo_link TEXT NOT NULL, 
        vk_id INTEGER REFERENCES User_vk_id(id));''')


def insert_inf(name):   # name - имя пользователя запустившего бота

    """ заполнение базы данных """

    create_bd()    # создаст бд при первом обращении к ней
    with open('canditat.json', 'r') as f:
        doc = json.load(f)
    con = get_connect()
    try:
        con.execute("INSERT INTO Bots_user (name) VALUES(%s)", (name,))
    except sqlalchemy.exc.IntegrityError:
        pass

    for i, y in doc.items():
        id_vk = i.split('id')[1]     # будем записывать id предложенных страниц
        # переменная(кортеж) для связывания таблиц
        bots_user_id = con.execute("SELECT id FROM Bots_user WHERE name =  %s", (name,)).fetchone()
        con.execute("INSERT INTO User_vk_id ( vk_id, bot_user_id) VALUES (%s, %s)",
                    (id_vk, bots_user_id[0]))
        for photo in y:
            # аналогично
            vk_user_id = con.execute("SELECT id FROM User_vk_id WHERE vk_id =  %s", (id_vk,)).fetchone()
            con.execute("INSERT INTO Photo ( photo_link, vk_id) VALUES (%s, %s)",
                        (photo, vk_user_id[0]))


def get_data(name):     # для поиска повторов в основном модуле
    con = get_connect()
    tup = con.execute("SELECT vk_id FROM User_vk_id uk JOIN Bots_user bu ON bot_user_id = bu.id WHERE name =  %s",
                      (name,)).fetchall()
    return tup


if __name__ == '__main__':
    create_bd()






