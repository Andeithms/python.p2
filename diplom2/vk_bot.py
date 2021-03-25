from random import randrange
from tqdm import tqdm
import Database as DB
import vk_api
import time
import json
from data.config import password, login
from group import server1


class MyBot:

    def __init__(self):
        self.password = password
        self.login = login
        self.user_id = ''
        self.vk_session = vk_api.VkApi(self.login, self.password)
        try:
            self.vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

    def collect_info(self, user_id):
        """ сбор информации о пользователе """
        self.user_id = user_id
        vk = self.vk_session.get_api()
        response = vk.users.get(user_ids=self.user_id, fields='sex, bdate, city')  # инфа о юзере
        time.sleep(1)
        sex = self.get_sex(response)
        age = self.get_age(response)
        town = self.get_town(response)
        user_info = [town, age, sex]
        return user_info

    def get_sex(self, resp):

        if resp[0]['sex'] != 0:  # определение пола
            user_sex = resp[0]['sex']
            return user_sex
        else:
            while True:  # если пол не указан, потребуем его написать
                server1.send_msg(self.user_id, 'Укажите пол( м/ж ) ')
                user_sex = server1.listen()[1]
                if user_sex == ('м'):
                    user_sex = 2
                    return user_sex
                elif user_sex == ('ж'):
                    user_sex = 1
                    return user_sex
                else:
                    server1.send_msg(self.user_id, 'Неверный ввод')

    def get_age(self, resp):
        try:
            user_year = resp[0]['bdate'].split('.')[2]
            return user_year
        except (KeyError, IndexError):
            server1.send_msg(self.user_id, 'Введите год рождения, например: 1990) ')
            while True:
                user_year = int(server1.listen()[1])
                if 1900 < user_year < 2100:
                    return user_year
                else:
                    server1.send_msg(self.user_id, 'Неверный ввод')

    def get_town(self, resp):
        try:
            city_id = resp[0]['city']['id']
            return city_id
        except KeyError:
            server1.send_msg(self.user_id, 'Введите свой город, пожалуйста не вводите города не из России ')
            while True:
                user_city = server1.listen()[1].capitalize()
                vk = self.vk_session.get_api()
                resp = vk.database.getCities(country_id=1, q=user_city)  # id города понадобится при поиске
                time.sleep(1)

                for i in resp['items']:
                    if user_city == i['title']:
                        city_id = i['id']
                        return city_id
                server1.send_msg(self.user_id, 'Не получилось найти такой город, проверьте правописание или введите'
                                               ' другой ')

    def selection(self, name, info):
        """ выборка подходящих людей """
        vk = self.vk_session.get_api()
        age_from = 2021 - int(info[1]) - 5
        age_to = 2021 - int(info[1]) + 5
        if info[2] == 1:  # противоположный пол
            unsex = 2
        else:
            unsex = 1

        city_id = info[0]
        server1.send_msg(self.user_id, 'Начинаю поиск пары')
        response = vk.users.search(sex=unsex,
                                   age_from=age_from,
                                   age_to=age_to,
                                   city=city_id,
                                   status=6,
                                   has_photo=1,
                                   count=1000,
                                   offset=randrange(10**2))     # чтобы избежать повторов при недоступности БД

        time.sleep(1)
        cdt_list = []
        history_list = DB.get_data(name)  # получение истории поиска по имени пользователя
        if history_list is not None:
            for i in response['items']:
                if i["can_access_closed"] and (len(cdt_list) < 10) and (i['id'] not in history_list):
                    cdt_list.append(i['id'])
        else:
            for i in response['items']:
                if i["can_access_closed"] and len(cdt_list) < 10:
                    cdt_list.append(i['id'])
        if len(cdt_list) < 1:
            server1.send_msg(self.user_id, 'Никого не нашел:с\n'
                                           'попробуйте поменять город или выполнить поиск еще раз   ')
        return cdt_list

    def get_photo(self, list_):
        """ сбор самых популярных фото """
        vk = self.vk_session.get_api()
        cdt_dict = {}

        for i in tqdm(list_):  # разбираем профили
            photo_dict = {}  # фото : сумма лайков и комментов, понадобится чтобы не потерять ссылку
            response = vk.photos.get(owner_id=i, album_id='profile', extended=1, count=1000)
            time.sleep(1)  # чтобы не получить бан за частые запросы
            photo_list = []  # для самых популярных фото

            for photo in response['items']:  # в этом цикле заполняем словарь фото : популярность
                count_like = photo['likes']['count']
                count_comments = photo['comments']['count']
                popularity = count_like + count_comments  # считаем общее кол-во лайков и комментов у фото
                photo_dict[photo['sizes'][-1]['url']] = popularity

            for x in range(3):  # отбор 3 фото
                max_count = 0

                for y in photo_dict.values():  # определяем наибольшее кол-во лайков
                    if max_count < y:
                        max_count = y

                for y in photo_dict.keys():  # выбираем самые популярные
                    if photo_dict[y] == max_count:
                        photo_list.append(y)
                        photo_dict.pop(y)
                        break

            cdt_dict['https://vk.com/id' + str(i)] = photo_list  # финальный список профиль - фото

        creating_json(cdt_dict)   # после получения результатов создасться json-файл
        self.history()  # попытка записать json в БД
        return cdt_dict

    def history(self):
        """ запись результатов поиска в бд """
        DB.insert_inf(self.user_id)

    def show_photo(self, photos):
        for i, y in photos.items():
            server1.send_msg(self.user_id, f'Возможная пара: {i}')
            for photo in y:
                server1.send_photo(self.user_id, photo)


def creating_json(pages):
    """ создание json-файла с кандитатми """
    with open('canditat.json', 'w') as f:
        json.dump(pages, f, indent=1)


if __name__ == '__main__':
    pass
