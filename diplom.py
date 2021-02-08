from datetime import datetime
from data import VK, Yandex


def user_inp():
    # user_input_vk = input('Введите токен vk ')
    user_input_id = input('Введите id vk(например: 133423499 или NickCoen) ')
    while True:
        inp_alb = input('Выберите откуда скачать фото,\n'
                        'profile(личные) - P \n'
                        'wall(со стены - w \n'
                        'saved(сохранённые - s ')
        if inp_alb == 'p':
            album_id = 'profile'
            break
        elif inp_alb == 'w':
            album_id = 'wall'
            break
        elif inp_alb == 's':
            album_id = 'saved'
            break
        else:
            print('Неверный ввод')

    token_input_ya = input('Введите токен Яндекса ')
    token_input_vk = '10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c'
    version = '5.126'
    user_1 = VK.UserVK(user_input_id, token_input_vk, version, album_id)
    uploader = Yandex.YaUploader("OAuth " + token_input_ya)
    print(uploader.upload(user_1))
    user_1.creating_json()


if __name__ == '__main__':
    print(datetime.now())
    user_inp()
