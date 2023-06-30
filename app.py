import json
import logging
import os
from flask import Flask, render_template

app = Flask(__name__)

# Путь к папке с данными
DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')
POSTS_FILE = os.path.join(DATA_FOLDER, 'posts.json')
COMMENTS_FILE = os.path.join(DATA_FOLDER, 'comments.json')
BOOKMARKS_FILE = os.path.join(DATA_FOLDER, 'bookmarks.json')
LOG_FILE = os.path.join(DATA_FOLDER, 'api.log')

# Настройка логгера
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR)


def load_json_file(file_path):
    """Загружает данные из JSON-файла."""
    try:
        with open(file_path, encoding='utf-8') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading JSON file '{file_path}': {e}")
        return None


def save_json_file(file_path, data):
    """Сохраняет данные в JSON-файл."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error saving JSON file '{file_path}': {e}")


def get_posts_all():
    """Возвращает все посты."""
    return load_json_file(POSTS_FILE)


def get_post_by_id(post_id):
    """Возвращает пост по его идентификатору."""
    posts = get_posts_all()
    if posts:
        for post in posts:
            if post['id'] == post_id:
                return post
    return None


def get_comments_by_post_id(post_id):
    """Возвращает комментарии для определенного поста."""
    comments = load_json_file(COMMENTS_FILE)
    if comments:
        post_comments = [comment for comment in comments if comment['post_id'] == post_id]
        return post_comments
    return []


@app.route('/')
def home():
    """Обработчик корневого маршрута."""
    posts = get_posts_all()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """Обработчик маршрута для просмотра отдельного поста."""
    post = get_post_by_id(post_id)
    if post:
        comments = get_comments_by_post_id(post_id)
        return render_template('post.html', post=post, comments=comments)
    else:
        return 'Post not found'


if __name__ == '__main__':
    app.run(debug=True)
