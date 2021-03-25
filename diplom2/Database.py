import sqlalchemy
import json
from data.config import password_bd


def create_bd():
    """ создание базы данных """
    try:
        engine = sqlalchemy.create_engine(f"postgresql://postgres:{password_bd}@localhost:5432/postgres")
        connection = engine.connect()
        connection.execute('''COMMIT''')
        connection.execute('''CREATE DATABASE users''')
        create_tables()
    except (sqlalchemy.exc.ProgrammingError, sqlalchemy.exc.OperationalError):
        pass


def get_connect():
    """ установка соединения с БД """
    try:    # на случай недоступности бд
        engine = sqlalchemy.create_engine(f'postgresql://postgres:{password_bd}@localhost:5432/users')
        connection = engine.connect()
        return connection
    except sqlalchemy.exc.OperationalError:
        return 'нет связи'


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
    if con == 'нет связи':
        return ''
    try:
        con.execute("INSERT INTO Bots_user (name) VALUES(%s)", (str(name),))
    except sqlalchemy.exc.IntegrityError:
        pass

    for i, y in doc.items():
        id_vk = i.split('id')[1]     # будем записывать id предложенных страниц
        # переменная(кортеж) для связывания таблиц
        bots_user_id = con.execute("SELECT id FROM Bots_user WHERE name =  %s", (str(name),)).fetchone()
        con.execute("INSERT INTO User_vk_id ( vk_id, bot_user_id) VALUES (%s, %s)",
                    (id_vk, bots_user_id[0]))
        for photo in y:
            # аналогично
            vk_user_id = con.execute("SELECT id FROM User_vk_id WHERE vk_id =  %s", (id_vk,)).fetchone()
            con.execute("INSERT INTO Photo ( photo_link, vk_id) VALUES (%s, %s)",
                        (photo, vk_user_id[0]))


def get_data(name):
    """ Получение истории поиска"""
    con = get_connect()
    history_list = []
    if con == 'нет связи':
        return history_list
    tup = con.execute("SELECT vk_id FROM User_vk_id uk JOIN Bots_user bu ON bot_user_id = bu.id WHERE name =  %s",
                      (str(name),)).fetchall()
    for i in tup:
        history_list.append(i[0])
    return history_list


if __name__ == '__main__':
    create_bd()








