import csv
import re
from pprint import pprint


def reading():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    # pprint(contacts_list)

    my_list = []
    for i in contacts_list:
        name_list = []
        for string in i[:3]:    # первые три слова это ФИО
            if string != "":
                for word in string.split(" "):
                    name_list.append(word)  # записываем ФИО в новый список
        if len(name_list) < 3:  # заполняем ячейку, где отсутствовало отчество
            name_list.append("")
        name_list.extend(i[3:7])    # возвращаем остальные данные к ФИО
        my_list.append(name_list)

    for i in my_list:
        pattern = re.compile(r"(\+*7|8)[\s-]*\(*(\d{3})\)*[\s-]*(\d{3})\-*(\d{2})\-*(\d{2})\s*\(*(доб.)*\s*(\d+)*\)*")
        # print(i[5])
        i[5] = pattern.sub(r'+7(\2)\3-\4-\5 \6\7', i[5])
        # print(i[5])

    person_info = []
    while len(my_list) != 0:    # создание нового списка путем удаления старого
        first_string = my_list.pop(0)
        if first_string is not None:
            for i in my_list:
                if first_string[0:2] == i[0:2]:     # сравнение удаленных элементов(ФИО) с оставшимися в списке
                    new_first_string = []
                    while len(first_string) != 0 and len(i) != 0:
                        var_1 = first_string.pop(0)     # сохраняем по элементу пока строка не опустеет
                        var_2 = i.pop(0)
                        if var_1 == var_2:
                            new_first_string.append(var_1)   # записываем только 1 ФИО если есть копия
                        else:
                            new_first_string.append(var_1 + var_2)
                    first_string = new_first_string     # новая строка с удаленными дублями

            person_info.append(first_string)    # отредактированный список

    return person_info


def writing(contacts_list):
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    writing(reading())



