import json


class MyIterator:

    def __init__(self, file_path):
        self.file_path = file_path
        self.i = -1

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file_path) as f:
            self.string = json.load(f)
        self.i += 1
        if self.string[self.i] is None:
            raise StopIteration
        country_name = self.string[self.i]['name']['common']
        country_link = ('https://en.wikipedia.org/wiki/' + country_name.replace(' ', '_'))
        with open('country_list.txt', 'a', encoding="utf-8") as cl:
            cl.write(f"{country_name}: {country_link}" '\n')
        return self.string[self.i]


if __name__ == '__main__':
    test = MyIterator('countries.json')
    for i in test:
        test.__next__()



