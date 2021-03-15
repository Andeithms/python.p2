import time
import json
import vk_api
from pprint import pprint
from tqdm import tqdm


def main():
    login, password = 'логин', 'пароль'
    bot = MyBot(login, password)
    user_info = bot.collect_info()
    candidat_list = bot.selection(user_info)
    pages = bot.get_photo(candidat_list)
    creating_json(pages)
    # pprint(pages)


def creating_json(pages):

    """ создание json-файла с кандитатми """

    with open('canditat.json', 'w') as f:
        json.dump(pages, f, indent=1)


class MyBot:

    def __init__(self, login, password):
        self.password = password
        self.login = login
        self.vk_session = vk_api.VkApi(self.login, self.password)
        try:
            self.vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

    def collect_info(self):

        """ сбор информации о пользователе """

        user_id = input('Введите id vk(например: 133423499 или NickCoen) ')  # для сбора инфы пользователя возьмем id
        vk = self.vk_session.get_api()
        response = vk.users.get(user_ids=user_id, fields='sex, bdate, city')  # инфа о юзере
        time.sleep(1)

        if response[0]['sex'] != 0:  # определение пола
            user_sex = response[0]['sex']
        else:
            while True:  # если пол не указан, потребуем его написать
                user_sex = input('Укажите пол( м/ж ) ')
                if user_sex == ('м'):
                    user_sex = 2
                    break
                elif user_sex == ('ж'):
                    user_sex = 1
                    break
                else:
                    print('Неверный ввод')

        try:
            user_year = response[0]['bdate'].split('.')[2]
        except (KeyError, IndexError):
            user_year = int(input('Введите год рождения (1990) '))
            while True:
                if 1900 < user_year < 2100:
                    break
                else:
                    print('Неправильный ввод')

        try:
            city_id = response[0]['city']['id']
        except KeyError:
            user_city = input('Введите свой город (Москва) ')
            resp = vk.database.getCities(country_id=1, q=user_city)  # id города понадобится при поиске
            time.sleep(1)

            '''country_id=1 - Россия,с городами в других странах работать не будет'''

            for i in resp['items']:
                if user_city == i['title']:
                    city_id = i['id']
                    break

        user_info = []
        user_info.append(city_id)
        user_info.append(user_year)
        user_info.append(user_sex)
        return user_info

    def selection(self, attribute):

        """ выборка подходящих людей """

        vk = self.vk_session.get_api()
        bdate = range(int(attribute[1]) - 5, int(attribute[1]) + 5)

        if attribute[2] == 1:  # противоположный пол
            unsex = 2
        else:
            unsex = 1

        city_id = attribute[0]
        response = vk.users.search(is_closed=0,  # не работает
                                   sex=unsex,
                                   birth_year=bdate,
                                   city=city_id,
                                   status=6,
                                   has_photo=1,
                                   count=1000)

        time.sleep(1)
        candidat_list = []
        for i in response['items']:
            if i["can_access_closed"] and len(candidat_list) < 10:
                '''i["can_access_closed"] - нужно чтоб отсеять скрытые страницы, т.к. is_closed не работает'''

                ''' проверка с бд на наличие повторов'''

                candidat_list.append(i['id'])
        return candidat_list

    def get_photo(self, candidat_list):

        """ сбор самых популярных фото """

        vk = self.vk_session.get_api()
        canditat_dict = {}

        for i in tqdm(candidat_list):  # разбираем профили
            photo_dict = {}  # фото : сумма лайков и комментов, понадобится чтобы не потерять ссылку
            response = vk.photos.get(owner_id=i, album_id='profile', extended=1, count=1000)
            time.sleep(1)  # чтобы не получить бан за частые запросы
            photo_list = []  # для самых популярных фото

            for photo in response['items']:  # в этом цикле заполняем словарь фото : популярность
                count_like = photo['likes']['count']
                count_comments = photo['comments']['count']
                popularity = count_like + count_comments  # считаем общее кол-во лайков и комментов у фото
                photo_dict[photo['sizes'][-1]['url']] = popularity

            for x in range(1, 4):  # отбор 3 фото
                max_count = 0

                for y in photo_dict.values():  # определяем наибольшее кол-во лайков
                    if max_count < y:
                        max_count = y

                for y in photo_dict.keys():  # выбираем самые популярные
                    if photo_dict[y] == max_count:
                        photo_list.append(y)
                        photo_dict.pop(y)
                        break

            canditat_dict['https://vk.com/id' + str(i)] = photo_list  # финальный список профиль - фото
        return canditat_dict

    def history(self):

        """ записываем все результаты поиска в бд """

        pass


if __name__ == '__main__':
    main()
