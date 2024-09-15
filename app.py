from flask import Flask, render_template, request
import requests
import re
import base64
import webbrowser
import threading

app = Flask(__name__)

# Конфигурация
KODIK_TOKEN = "4492ae176f94d3103750b9443139fdc5"
KODIK_API_URL = "https://kodikapi.com"  # Замените на правильный URL

# Функции для работы с Kodik
def extract_domain(url):
    start = url.find("//")
    if start != -1:
        start += 2
    else:
        start = 0
    end = url.find('/', start)
    if end == -1:
        end = len(url)
    return url[start:end]

def decode_base64(encoded):
    return base64.b64decode(encoded).decode('utf-8')

def decode_url(encoded):
    rot13_encoded = ''.join(
        chr((ord(c) - 65 + 13) % 26 + 65) if 'A' <= c <= 'Z' else
        chr((ord(c) - 97 + 13) % 26 + 97) if 'a' <= c <= 'z' else c for c in encoded
    )
    return decode_base64(rot13_encoded)

def get_videos_map(base_url):
    video_links_map = {}
    url_pattern = r'"([0-9]+)p?":\[\{"src":"([^\"]+)"'
    
    response = requests.get(base_url)
    if response.status_code == 200:
        html = response.text
        matches = re.findall(url_pattern, html)
        for match in matches:
            quality, link = match
            decoded_link = decode_url(link)
            video_links_map[quality] = decoded_link
    return video_links_map

# Поиск контента по запросу
def search_content(query, search_type='title'):
    try:
        url = f"{KODIK_API_URL}/search"
        params = {
            'token': KODIK_TOKEN,
            search_type: query
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            return data['results']
        else:
            print(f"Непредвиденный формат ответа: {data}")
            return None
    except requests.RequestException as e:
        print(f"Ошибка при поиске: {e}")
        return None

# Получение ссылок на видео
def get_kodik_links(video_link):
    try:
        video_links = get_videos_map(video_link)  # Используем декодирование для ссылок
        return video_links
    except Exception as e:
        print(f"Ошибка получения видео: {e}")
        return None

# Маршруты
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    if not query:
        return render_template('index.html', error="Введите запрос!")
    
    results = search_content(query)
    if not results:
        return render_template('index.html', error="Ничего не найдено!")
    
    return render_template('index.html', results=results)

@app.route('/play/<path:video_link>')
def play(video_link):
    kodik_links = get_kodik_links(video_link)
    if kodik_links:
        return render_template('player.html', kodik_links=kodik_links)
    return "Ошибка получения видео!"

# Открытие браузера
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
