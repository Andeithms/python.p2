import hashlib


def generate_file_md5(file_path):

    with open(file_path, "rb") as f:
        while chunk := f.readline():
            file_hash = hashlib.md5(chunk)
            yield file_hash.digest()


if __name__ == '__main__':
    for i in generate_file_md5('country_list.txt'):
        print(i)
