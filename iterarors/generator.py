import hashlib


def generate_file_md5(file_path):

    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            yield chunk
            file_hash.update(chunk)
            print(file_hash.digest())
            print(file_hash.hexdigest())


if __name__ == '__main__':
    for item in generate_file_md5('countries.json'):
        pass
