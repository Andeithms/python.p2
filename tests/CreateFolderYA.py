import requests


def creating_folder():
    TOKEN = 'OAuth токен'
    HEADERS = {'Accept': 'application/json', 'Authorization': TOKEN}
    # input_folder = 'aaaa'
    # requests.put('https://cloud-api.yandex.net/v1/disk/resources',
    #              params={'path': "/" + str(input_folder)},
    #              headers=HEADERS,
    #              )
    checking_folders = requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                                    params={'path': "/"},
                                    headers=HEADERS,
                                    ).status_code
    return checking_folders


if __name__ == '__main__':
    print(creating_folder())


