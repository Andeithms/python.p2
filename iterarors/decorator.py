from datetime import datetime
from generator import generate_file_md5


def log_decorator(file_path):

    def decorator(old_function):

        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            log = (f"Время вызова функции: {datetime.now()}, имя функции: {old_function.__name__}," 
                   f"параметры функции: {args}, {kwargs}, возвращаемое значение: {result}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(log + "\n")
            return result

        return new_function

    return decorator


if __name__ == '__main__':

    @log_decorator('log.txt')
    def function(file_path):
        return generate_file_md5(file_path)


    for i in function('countries.json'):
        pass
