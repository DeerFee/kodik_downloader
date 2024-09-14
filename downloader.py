import requests
from bs4 import BeautifulSoup
import json
import requests

def search_content(query):
    try:
        # Формируем URL для поиска на Kodik
        search_url = f"https://kodik.cc/search?q={query}"
        response = requests.get(search_url)
        response.raise_for_status()  # Проверка на успешность запроса

        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Здесь мы ожидаем список результатов поиска
        results = []
        search_results = soup.find_all('a', class_='film-list-item')  # Заменить на актуальный селектор

        for result in search_results:
            title = result.find('div', class_='film-list-item-title').text  # Определить точный селектор
            link = result['href']
            results.append({"title": title, "link": link})

        return results
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        return []

def get_kodik_links(share_kodik_link):
    try:
        # Формируем URL для запроса
        url = f"https:{share_kodik_link}"

        # Шаг 1: Получаем HTML страницы
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешность запроса
        page_content = response.text

        # Шаг 2: Разбор HTML и извлечение данных
        soup = BeautifulSoup(page_content, 'html.parser')
        page_text = soup.get_text().split()

        # Извлекаем параметры видео
        video_type = page_text[page_text.index('videoInfo.type') + 2].strip('"', ';', '\'')
        video_hash = page_text[page_text.index('videoInfo.hash') + 2].strip('"', ';', '\'')
        video_id = page_text[page_text.index('videoInfo.id') + 2].strip('"', ';', '\'')
        info = '{"advImps":{}}'
        bad_user = 'true'

        # Извлекаем urlParams
        url_params_string = page_text[page_text.index('urlParams') + 2].strip('\'', ';', '\'')
        url_params = json.loads(url_params_string)

        # Шаг 3: Отправляем POST-запрос на Kodik API для получения ссылки на видео
        api_url = "https://kodik.info/gvi"
        headers = {'x-requested-with': 'XMLHttpRequest'}
        form_data = {
            'd': url_params.get('d'),
            'd_sign': url_params.get('d_sign'),
            'pd': url_params.get('pd'),
            'pd_sign': url_params.get('pd_sign'),
            'ref': url_params.get('ref'),
            'ref_sign': url_params.get('ref_sign'),
            'bad_user': bad_user,
            'type': video_type,
            'hash': video_hash,
            'id': video_id,
            'info': info
        }

        response_dvi = requests.post(api_url, headers=headers, data=form_data)
        response_dvi.raise_for_status()  # Проверка на успешность запроса

        # Шаг 4: Получаем JSON с ссылками на видео
        kodik_links = response_dvi.json()

        return kodik_links  # Возвращаем результат
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
