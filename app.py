from flask import Flask, render_template, request
from downloader import search_content, get_kodik_links
import webbrowser
import threading

app = Flask(__name__)

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
    
# Функция для автоматического открытия браузера
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    # Создаём поток для открытия браузера после запуска приложения
    threading.Timer(1, open_browser).start()
    app.run()
