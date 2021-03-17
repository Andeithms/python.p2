from tqdm import tqdm
import Database as DB
import vk_api
import time


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

        print('Приветсвую!')
        user_id = input('Введите id vk(например: 133423499 или NickCoen) ')  # для сбора инфы пользователя возьмем id
        vk = self.vk_session.get_api()
        response = vk.users.get(user_ids=user_id, fields='sex, bdate, city')  # инфа о юзере
        time.sleep(1)

        print('Собираю информацию...')
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
            user_city = response[0]['city']['title']
            city_id = response[0]['city']['id']
        except KeyError:
            user_city = input('Введите свой город, пожалуйста не вводите города не из России ').capitalize()
            resp = vk.database.getCities(country_id=1, q=user_city)  # id города понадобится при поиске
            time.sleep(1)

            for i in resp['items']:
                if user_city == i['title']:
                    city_id = i['id']
                    break

        user_info = []
        user_info.append(city_id)
        user_info.append(user_year)
        user_info.append(user_sex)
        print(f'Ваш год рождения {user_year}, ваш город {user_city}\n'
              f'Если есть не совпадения, попробуйте обновить информацию на своей страничке в ВК\n'
              f'Приступаем к подборке пары? ')

        while True:
            user_input = input(' да / нет ')
            if user_input.lower() == ('да'):      # антикапс
                break
            elif user_input.lower() == ('нет'):
                exit()
            else:
                print('Пожалуйста либо русскими буквами да, либо нет')
        return user_id, user_info

    def selection(self, name, info):

        """ выборка подходящих людей """

        print('Начинаю поиск пары')
        vk = self.vk_session.get_api()
        bdate = range(int(info[1]) - 5, int(info[1]) + 5)

        if info[2] == 1:  # противоположный пол
            unsex = 2
        else:
            unsex = 1

        city_id = info[0]
        response = vk.users.search(sex=unsex,
                                   birth_year=bdate,
                                   city=city_id,
                                   status=6,
                                   has_photo=1,
                                   count=1000,)

        time.sleep(1)
        candidat_list = []
        tup = DB.get_data(name)  # получение истории поиска по имени пользователя
        history_list = []
        for i in tup:
            history_list.append(i[0])
        for i in response['items']:
            if i["can_access_closed"] and (len(candidat_list) < 10) and (i['id'] not in history_list):
                candidat_list.append(i['id'])

        return candidat_list

    def get_photo(self, list_):

        """ сбор самых популярных фото """

        vk = self.vk_session.get_api()
        canditat_dict = {}

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

    def history(self, name):

        """ запись результатов поиска в бд """

        DB.insert_inf(name)
