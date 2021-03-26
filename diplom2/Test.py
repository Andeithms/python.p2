import unittest
import Database as DB
from vk_bot import MyBot
import vk_api
from data.config import login, password


class MyTest(unittest.TestCase):

    def setUp(self):
        self.user_id = 'windgood'
        self.login, self.password = login, password
        self.vk_session = vk_api.VkApi(self.login, self.password)
        try:
            self.vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)

        self.doc = [362185124, 350195378, 272507299, 174682711, 9950888,
                    133290766, 205399292, 176711574, 156384242, 327596850]
        self.dict = {'https://vk.com/id362185124': [
            'https://sun9-68.userapi.com/impf/c639319/v639319124/22c8/KkZAhg4wkL4.jpg?size=720x720&quality=96&sign=d1e'
            '95d43ef9ca8fb4fab826c6869d369&c_uniq_tag=moYGfZxkr6bueG_kldXPkrU3hBIohCALVawEBeCpJ-s&type=album',
            'https://sun9-37.userapi.com/impf/c841237/v841237744/2b681/HM9yIcR1UlM.jpg?size=1080x802&quality=96&sign'
            '=6b6c4075dda471bd2e1567ae98674f88&c_uniq_tag=Z6DHyGxYsueobpy7abUgKR4D1Or_95mF7BqDvXScIWA&type=album',
            'https://sun9-38.userapi.com/impf/c837225/v837225124/2602/YxVLHWBpg28.jpg?size=617x617&quality=96&sign='
            '8e7ce974c4b07e6c54ccba2c87d362f9&c_uniq_tag=6wAjT-PiKbkDHK_nyv4PwWLm-r7LtkszRd_4U4D8K2o&type=album']}

    def test_collect_info(self):
        vk = self.vk_session.get_api()
        response = vk.users.get(user_ids=self.user_id, fields='sex, bdate, city')
        self.assertEqual(MyBot.get_sex(self, response), 2)
        self.assertEqual(MyBot.get_age(self, response), '1998')
        self.assertEqual(MyBot.get_town(self, response), 56)

    def test_get_data(self):
        self.assertEqual(DB.get_data(self.user_id), self.doc)

    def test_get_photo(self):
        self.assertEqual(MyBot.get_photo(self, [362185124]), self.dict)

    def history(self):  # чтобы избежать ошибки при вызове записи в БД в test_get_photo
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
