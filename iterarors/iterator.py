import requests
import json
from tqdm import tqdm


class MyIterator:

    def __init__(self, file_path):
        self.file_path = file_path
        self.country_list = []
        self.i = -1
        with open(self.file_path) as f:
            self.file = json.load(f)

    def __iter__(self):
        return self

    def __next__(self):
        string = self.file
        self.i += 1
        if string[self.i] is None:
            raise StopIteration
        return string[self.i]

    def writer(self):
        for country in tqdm(self.file):
            country_url = {}
            response = requests.get('https://en.wikipedia.org/wiki/' + country['name']['common']).url
            country_url[country['name']['common']] = response
            self.country_list.append(country_url)
        with open('country_list.json', 'w', ) as cl:
            json.dump(self.country_list, cl, indent=1)
        return self.country_list


if __name__ == '__main__':
    test = MyIterator('countries.json').writer()



