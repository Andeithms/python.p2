import diplom

if __name__ == '__main__':
    user_input_id = 'aksiev_ma'
    album_id = 'profile'
    token_input_vk = '10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c'
    version = '5.126'
    user_2 = diplom.VK.UserVK(user_input_id, token_input_vk, version, album_id)