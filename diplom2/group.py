import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from data.config import token, group_id


class MyGroup:

    def __init__(self, api_token, g_id, group_name: str = "Empty"):
        self.group_name = group_name
        self.g_id = g_id
        self.api_token = api_token
        self.vk = vk_api.VkApi(token=self.api_token)
        self.long_poll = VkLongPoll(self.vk)
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, msg):
        self.vk_api.messages.send(peer_id=send_id,
                                  message=msg,
                                  random_id=randrange(10 ** 7))

    def send_photo(self, send_id, photo):
        self.vk_api.messages.send(peer_id=send_id,
                                  attachment=photo,
                                  random_id=randrange(10 ** 7))

    def listen(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    return int(event.user_id), event.text


server1 = MyGroup(token, group_id, "server")
