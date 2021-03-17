from vk_bot import MyBot
import json
from pprint import pprint


def main():
    login, password = '', ''
    bot = MyBot(login, password)
    user_id, user_info = bot.collect_info()

    while True:
        candidat_list = bot.selection(user_id, user_info)
        pages = bot.get_photo(candidat_list)
        creating_json(pages)
        bot.history(user_id)
        print(' Возможные пары: ')
        pprint(pages)

        print('Желаете повторно вы полнить поиск?')
        user_input = input(' да / нет ')
        if user_input.lower() == ('да'):  # антикапс
            pass
        elif user_input.lower() == ('нет'):
            break
        else:
            print('Пожалуйста либо русскими буквами да, либо нет')


def creating_json(pages):

    """ создание json-файла с кандитатми """

    with open('canditat.json', 'w') as f:
        json.dump(pages, f, indent=1)


if __name__ == '__main__':
    main()
