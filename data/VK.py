from pprint import pprint
import requests
import json


class UserVK:
    url = 'https://api.vk.com/method/'

    def __init__(self, user_id, token, version, album):
        self.version = version
        self.token = token
        self.owner_id = user_id
        self.album = album

        if user_id.isdigit() is False:
            resp = requests.get(self.url + "utils.resolveScreenName", {'access_token': self.token,
                                                                       'v': self.version,
                                                                       'screen_name': user_id}).json()
            self.owner_id = resp['response']['object_id']

        self.params = {
            'owner_id': self.owner_id,
            'access_token': self.token,
            'v': self.version,
            'album_id': self.album,
            'extended': 1,
        }
        self.photos = requests.get(self.url + "photos.get", self.params).json()
        pprint(self.photos)

    def creating_json(self):
        photo_list = []
        for i in self.photos["response"]["items"]:  # создаем список всех фото пользователя
            photo = {}
            count_like = i['likes']['count']
            photo['file_name'] = count_like
            for x in photo_list:  # проверка фото на одинаковое кол-во лайков
                if x['file_name'] == count_like:
                    photo['file_name'] = str(count_like) + '.' + str(i['date'])  # '.' - разделитель лайков и даты
            photo['size'] = i['sizes'][-1]['type']  # -1 это последнее фото с максимальным разрешением
            photo_list.append(photo)
        with open('photo.json', 'w') as file_work:
            json.dump(photo_list, file_work)
        return photo_list

    def photo_for_upload(self):
        photo_list = []
        for i in self.photos["response"]["items"]:
            photo = {}
            count_like = i['likes']['count']
            photo['file_name'] = count_like
            for x in photo_list:
                if x['file_name'] == count_like:
                    photo['file_name'] = str(count_like) + '.' + str(i['date'])
            photo['url'] = i['sizes'][-1]['url']
            photo_list.append(photo)
        return photo_list
