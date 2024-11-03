from pathlib import Path
import json
import random
import time
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

# # Общее количество итераций
# total_iterations = 264 // 8
#
# # Замените на нужный диапазон
# for i in range(0, 128, 8):
#     # Текущая итерация
#     current_iteration = i // 8 + 1
#     # Осталось итераций
#     remaining_iterations = total_iterations - current_iteration
#
#     print(f'Идет парсинг... Итерация: {current_iteration}/{total_iterations}, Осталось: {remaining_iterations}')
#
#     url = (f'https://www.skiddle.com/api/v1/events/search/?limit=8&offset={i}&radius=10&minDate=2024-11-02T00%3A00%3A00&h'
#            f'idecancelled=1&order=trending&showVirtualEvents=0&artistmeta=1&artistmetalimit=3&aggs=genreids%2Ceventcode&'
#            f'pub_key=42f25&platform=web&collapse=uniquelistingidentifier')
#
#     request = requests.get(url=url, headers=headers)
#     json_data = json.loads(request.text)
#
#
#     for j in json_data['results']:
#         link = j['link']
#         link_req = requests.get(link, headers=headers)
#
#         with open('event_links.txt', 'a', encoding='utf-8') as file:
#             file.write(f"{link}\n")
#
#         with open(f'data/index_{j["id"]}.html', 'w', encoding='utf-8') as file:
#                 file.write(link_req.text)
#
#         time.sleep(random.randint(2, 4))

import json
from pathlib import Path
from bs4 import BeautifulSoup

# Укажите путь к папке с HTML-файлами
folder_path = Path('data')
fest_list_result = []

# Проходим по всем HTML-файлам в папке
for file_path in folder_path.glob('*.html'):
    print(f"Обрабатываем файл: {file_path}")

    # Инициализация переменных
    page_title = fest_location = fest_date = None

    # Открываем файл и читаем его содержимое
    with file_path.open('r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')

        # Ищем элемент с классом 'MuiBox-root'
        mui_box = soup.find(class_='MuiBox-root')
        if mui_box:
            page_title = mui_box.find('h1').text.strip()
            print(f"Заголовок страницы: {page_title}")
        else:
            print("Элемент с классом 'MuiBox-root' не найден")

        # Ищем элемент с классом 'MuiPaper-elevation1'
        info_block = soup.find(class_='MuiPaper-elevation1')
        if info_block:
            try:
                fest_location = info_block.find('a').get('href')
                dates = info_block.find_all('span')
                if len(dates) >= 2:
                    fest_date = f'{dates[0].text.strip()}, {dates[1].text.strip()}'
                else:
                    print("Недостаточно элементов span для формирования fest_date")
            except Exception:
                print("Событие уже произошло")
                continue
        else:
            print("Элемент с классом 'MuiPaper-elevation1' не найден")

        # Добавляем данные в fest_list_result только если все необходимые элементы найдены
        if page_title and fest_location and fest_date:
            fest_list_result.append({
                'page_title': page_title,
                'festival_location': fest_location,
                'date': fest_date
            })

# Сохраняем результат в JSON файл
with open('fest_list_result.json', 'w', encoding='utf-8') as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)