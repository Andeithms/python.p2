from data import libr


def main():
    while True:
        user_input = input('Введите команду' '\n' 'r - справка ')
        if user_input == 'p':
            input_number_doc = input('Введите номер документа ')
            print(people(input_number_doc))
        elif user_input == 's':
            input_number_doc = input('Введите номер документа ')
            print(shelf(input_number_doc))
        elif user_input == 'l':
            list_1()
        elif user_input == 'r':
            reference()
        elif user_input == 'as':
            input_number_shelf = input('Введите номер новой полки ')
            print(add_shelf(input_number_shelf))
        elif user_input == 'a':
            input_directory = input('Введите номер полки ')
            print(add(input_directory))
        elif user_input == 'd':
            input_number_doc = input('Введите номер документа, который хотите удалить ')
            print(delete(input_number_doc))
        elif user_input == 'm':
            input_number_doc = input('Введите номер документа ')
            print(move(input_number_doc))
        elif user_input == 'q':
            break


def people(user_input):
    for numb in libr.documents:
        if user_input == numb['number']:
            return numb['name']
    return 'Такого документа нет'


def list_1():
    for x in libr.documents:
        print(f'{x["type"]} "{x["number"]}" "{x["name"]}"')


def shelf(user_input):
    for numb in libr.directories:
        if user_input in libr.directories[numb]:
            return f'Номер полки {numb}'
    return 'Такого документа нет'


def add_shelf(user_input):
    if user_input in libr.directories.keys():
        return 'Такая полка уже существует'
    else:
        libr.directories[user_input] = []
        return 'Полка добавлена'


def add(user_input):
    if user_input not in libr.directories.keys():
        return 'Такой полки не существует'
    else:
        input_type = input('Введите тип документа ')
        input_number = input('Введите номер документа ')
        input_name = input('Введите имя владельца ')
        new_doc = dict(type=input_type, number=input_number, name=input_name)
        libr.documents.append(new_doc)
        libr.directories[user_input] += [input_number]
        return 'Данные успешно внесены'


def delete(user_input):
    initial_lent = len(libr.documents)
    for i, numb in enumerate(libr.documents):
        if user_input == numb['number']:
            libr.documents.pop(i)
    if initial_lent == len(libr.documents):
        return 'Такого документа нет'
    for key, value in libr.directories.items():
        if user_input in value:
            value.remove(user_input)
    return 'Документ удален'


def move(user_input):
    for numb in libr.directories.values():
        if user_input in numb:
            input_directory = input('Введите номер полки, на которую хотите поместить документ ')
            if input_directory not in libr.directories.keys():
                return 'Такой полки не существует'
            else:
                libr.directories[input_directory] += [user_input]
                numb.remove(user_input)
                return 'Документ перемещен'
    return 'Такого документа нет'


def reference():
    print('p - имя владельца документа''\n'
          's - номер полки с документом''\n'
          'l - список всех документов''\n'
          'as - добавление нового документа''\n'
          'd - удаление документа по его номеру''\n'
          'm -  перемещение документа на другую полку''\n'
          'q - выход из программы')


if __name__ == '__main__':
    main()
