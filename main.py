from pprint import pprint
import csv
import re
from logging import logger

@logger(path='fix_name.log')
def fix_name(list_contact):
    """
    Функция записывает Фамили, Имя и Отчетсво в соотв. поля/столбцы
    :param list_contact: Список с контактами
    :return: Отформатированный список с контактами
    """
    pattern = ' +'
    n= 0
    for contact in list_contact:
        emploee_lastname = re.findall(pattern, contact[0])
        if len(emploee_lastname) != 0:
            emploee_sep = contact[0].split(' ')
            list_contact[n][0] = emploee_sep[0]
            list_contact[n][1] = emploee_sep[1]
            if len(emploee_sep) == 3:
                list_contact[n][2] = emploee_sep[2]
        emploee_firstname = re.findall(pattern, contact[1])
        if len(emploee_firstname) != 0:
            emploee_firstname_sep = contact[1].split(' ')
            list_contact[n][1] = emploee_firstname_sep[0]
            list_contact[n][2] = emploee_firstname_sep[1]
        n += 1
    return list_contact

@logger(path='fix_tel.log')
def fix_tel(list_tel):
    """
    Функция заменяет телефонные номера на требуемый формат +7(999)999-99-99 доб.9999
    :param list_tel: Список для сиправления номеров телефонов
    :return: Исправленный список
    """
    pattern_tel = '(\+7|8) *\(*(\d{3})\)* *-*(\d{3})-*(\d{2})-*(\d{2}) *\(*д*о*б*\.* *(\d*)\)*'
    pattern = 'д'
    substitution_add = r'+7(\2)\3-\4-\5 доб.\6'
    substitution = r'+7(\2)\3-\4-\5'
    n = 0
    for tel in list_tel:
        emploee_tel = re.findall(pattern, tel[5])
        if len(emploee_tel) == 0:
            telephone = re.sub(pattern_tel, substitution, tel[5])
            list_tel[n][5] = telephone
        else:
            telephone = re.sub(pattern_tel, substitution_add, tel[5])
            list_tel[n][5] = telephone
        n += 1
    return list_tel


@logger(path='fix_data.log')
def fix_data(list_to_fix):
    """
    Функция объеденяет все дублирующие записи и удаляет лишние
    :param list_to_fix: Список для исправления
    :return: Исправленный список
    """
    fixed_list = []
    for contact_list in list_to_fix:
        n = len(list_to_fix)
        m = 0
        while n != 0:
            if (contact_list[0] == list_to_fix[-n][0]) and (contact_list[1] == list_to_fix[-n][1]):
                m += 1
                if m >= 2:
                    k = n
                    l = len(list_to_fix[0])
                    b = len(list_to_fix[0])
                    while l != 0:
                        if len(contact_list[b-l]) < len(list_to_fix[-k][b-l]):
                            contact_list[b-l] = list_to_fix[-k][b-l]
                        l -= 1
            n -= 1
        fixed_list.append(contact_list)

    fixed_list.sort()
    fix_list = []
    n = len(fixed_list)

    while n != 0:
        if (fixed_list[-n][0] in fixed_list[-n+1][0]) and (fixed_list[-n][1] in fixed_list[-n+1][1]):
            fix_list.append(fixed_list[-n+1])
            n -= 2
        else:
            fix_list.append(fixed_list[-n])
            n -= 1
    return fix_list

if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    fix_contacts_list = fix_name(contacts_list)
    fix_contacts_list = fix_tel(fix_contacts_list)
    fix_contacts_list = fix_data(fix_contacts_list)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(fix_contacts_list)