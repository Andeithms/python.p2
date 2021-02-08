import requests
from tqdm import tqdm
import time


class YaUploader:
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN
        self.HEADERS = {'Accept': 'application/json', 'Authorization': self.TOKEN}

    def checking_my_yandex_disc(self):
        checking_folders = requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                                        params={'path': "/"},
                                        headers=self.HEADERS,
                                        )
        checking_folders.raise_for_status()
        data = checking_folders.json()
        return data

    def creating_folder(self):
        data = self.checking_my_yandex_disc()
        input_folder = input('Введите имя папки, в которую хотите загрузить фото ')

        for file in data['_embedded']['items']:
            if input_folder == file['name']:
                print('Такая папка уже существует, хотите загрузить в нее?')
                user_answer = input('yes/no ')
                if user_answer == 'yes':
                    break
                else:
                    return self.creating_folder()

        requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                     params={'path': "/" + str(input_folder)},
                     headers=self.HEADERS,
                     )
        return input_folder

    def upload(self, user):
        folder_name = self.creating_folder()
        photo_list = user.photo_for_upload()
        for photo in tqdm(photo_list):
            requests.post(
                'https://cloud-api.yandex.net/v1/disk/resources/upload',
                params={'path': "/" + folder_name + "/" + str(photo['file_name']),
                        'url': photo['url'],
                        'overwrite': 'true'},
                headers=self.HEADERS,
            )
            time.sleep(1)
        return 'Фото загружены'
