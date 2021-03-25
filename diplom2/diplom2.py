from vk_bot import MyBot
from group import server1


def main():
    while True:
        if server1.listen():
            user_id, message = server1.listen()
            server1.send_msg(user_id, 'Приветсвую!')
            user_info = bot.collect_info(user_id)
            working(user_id, user_info)


def working(user_id, user_info):
    candidat_list = bot.selection(user_id, user_info)
    pages = bot.get_photo(candidat_list)
    bot.show_photo(pages)
    server1.send_msg(user_id, 'Выполнить поиск еще раз?( да/нет )')
    while True:
        user_input = server1.listen()[1]
        if user_input.lower() == ('да'):
            working(user_id, user_info)
        else:
            main()


if __name__ == '__main__':
    bot = MyBot()
    main()
