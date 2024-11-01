import random
import time

from bs4 import BeautifulSoup
import lxml
import json
import requests

# persons_url_list = []
#
# for i in range(0, 756, 12):
#     url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}'
#     print(url)
#
#     request  = requests.get(url)
#     result = request.content
#
#     soup = BeautifulSoup(result, 'lxml')
#     persons = soup.find_all(class_='bt-slide-content')
#
#     for person in persons:
#         person_page_url = person.find('a').get('href')
#         persons_url_list.append(person_page_url)
#
# with open('persons_url_list.txt', 'a') as file:
#     for line in persons_url_list:
#         file.write(f'{line}\n')


data_list = []

# Открываем файл с URL-адресами
with open('persons_url_list.txt') as file:
    lines = [line.strip() for line in file.readlines()]

    count = 0

    for line in lines:
        print(f'Идет парсинг...Итерация: {count + 1}')
        try:
            # Отправляем GET-запрос
            request = requests.get(line)
            result = request.content

            # Создаем объект BeautifulSoup для парсинга HTML с использованием lxml
            soup = BeautifulSoup(result, 'lxml')

            # Извлекаем информацию о человеке
            person_info = soup.find(class_='bt-biografie-name').find('h2').text.strip().split(',')
            person_name = person_info[0]
            person_company = person_info[1]

            # Извлекаем ссылки
            person_links_list = []
            person_links = soup.find(class_="bt-linkliste").find_all(class_='bt-link-extern')
            for person_link in person_links:
                person_links_list.append(person_link.get('href'))

            # Создаем словарь с данными
            data = {
                'person_name': person_name,
                'person_company': person_company,
                'person_links': person_links_list
            }

            # Добавляем данные в список
            data_list.append(data)

            count += 1

            # Задержка для имитации человеческого поведения
            time.sleep(random.randint(2, 4))

        except Exception as e:
            print(f"Ошибка при обработке URL {line}: {e}")

# Записываем данные в файл JSON
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, indent=4, ensure_ascii=False)


