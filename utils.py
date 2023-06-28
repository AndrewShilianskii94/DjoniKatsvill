import json
import logging
import codecs
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Пути к файлам
DATA_FOLDER = 'C:/Users/Андрей/PycharmProjects/DjoniKatsvill/data/'
POSTS_FILE = DATA_FOLDER + 'posts.json'
COMMENTS_FILE = DATA_FOLDER + 'comments.json'
BOOKMARKS_FILE = DATA_FOLDER + 'bookmarks.json'
LOG_FILE = DATA_FOLDER + 'api.log'


def load_json_file(file_path):
    """Загружает JSON-файл и возвращает его содержимое."""
    with codecs.open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def save_json_file(file_path, data):
    """Сохраняет данные в JSON-файл."""
    with codecs.open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_posts_all():
    """Возвращает все посты из файла."""
    return load_json_file(POSTS_FILE)


def get_comments_all():
    """Возвращает все комментарии из файла."""
    return load_json_file(COMMENTS_FILE)


def get_bookmarks_all():
    """Возвращает все закладки из файла."""
    return load_json_file(BOOKMARKS_FILE)


def add_post(post_data):
    """Добавляет новый пост в файл."""
    posts = get_posts_all()
    posts.append(post_data)
    save_json_file(POSTS_FILE, posts)


def add_comment(comment_data):
    """Добавляет новый комментарий в файл."""
    comments = get_comments_all()
    comments.append(comment_data)
    save_json_file(COMMENTS_FILE, comments)


def add_bookmark(bookmark_data):
    """Добавляет новую закладку в файл."""
    bookmarks = get_bookmarks_all()
    bookmarks.append(bookmark_data)
    save_json_file(BOOKMARKS_FILE, bookmarks)


def delete_post(post_id):
    """Удаляет пост по указанному идентификатору."""
    posts = get_posts_all()
    for post in posts:
        if post['pk'] == post_id:
            posts.remove(post)
            save_json_file(POSTS_FILE, posts)
            return True
    return False


def delete_comment(comment_id):
    """Удаляет комментарий по указанному идентификатору."""
    comments = get_comments_all()
    for comment in comments:
        if comment['pk'] == comment_id:
            comments.remove(comment)
            save_json_file(COMMENTS_FILE, comments)
            return True
    return False


def delete_bookmark(bookmark_id):
    """Удаляет закладку по указанному идентификатору."""
    bookmarks = get_bookmarks_all()
    for bookmark in bookmarks:
        if bookmark['pk'] == bookmark_id:
            bookmarks.remove(bookmark)
            save_json_file(BOOKMARKS_FILE, bookmarks)
            return True
    return False


def configure_api_logger():
    """Настройка логгера API."""
    logger = logging.getLogger('api')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


# Отключение кэширования
@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response


def get_post_by_pk(pk):
    """Возвращает пост по указанному идентификатору."""
    posts = get_posts_all()
    for post in posts:
        if post['pk'] == pk:
            return post
    raise ValueError("Post with specified PK does not exist.")


def get_comments_by_post_id(post_id):
    """Возвращает комментарии для поста с указанным идентификатором."""
    comments = get_comments_all()
    post_comments = [comment for comment in comments if comment['post_id'] == post_id]
    if not post_comments:
        raise ValueError("Post does not exist or has no comments.")
    return post_comments


def search_for_posts(query):
    """Выполняет поиск постов по указанному запросу."""
    posts = get_posts_all()
    search_results = [post for post in posts if query in post['content']]
    return search_results


def get_posts_by_user(user_name):
    """Возвращает посты для указанного пользователя."""
    posts = get_posts_all()
    user_posts_data = [post for post in posts if post['poster_name'] == user_name]
    if not user_posts_data:
        raise ValueError("User does not exist or has no posts.")
    return user_posts_data


@app.route('/')
def home():
    """Обработчик маршрута главной страницы."""
    posts = get_posts_all()
    return render_template('index.html', posts=posts)


@app.route('/posts/<postid>')
def view_post(postid):
    """Обработчик маршрута просмотра отдельного поста."""
    try:
        post = get_post_by_pk(postid)
        comments = get_comments_by_post_id(postid)
        return render_template('post.html', post=post, comments=comments)
    except ValueError as e:
        return str(e), 404


@app.route('/search/')
def search():
    """Обработчик маршрута поиска постов."""
    query = request.args.get('s', '')
    results = search_for_posts(query)
    return render_template('search.html', query=query, results=results)


@app.route('/users/<username>')
def user_feed(username):
    """Обработчик маршрута просмотра постов пользователя."""
    try:
        user_posts_data = get_posts_by_user(username)
        return render_template('user-feed.html', username=username, posts=user_posts_data)
    except ValueError as e:
        return str(e), 404


# API endpoints
@app.route('/api/posts')
def api_get_posts():
    """API-метод для получения всех постов."""
    posts = get_posts_all()
    return jsonify(posts)


@app.route('/api/posts/<post_id>')
def api_get_post(post_id):
    """API-метод для получения поста по идентификатору."""
    try:
        post = get_post_by_pk(post_id)
        return jsonify(post)
    except ValueError as e:
        return str(e), 404


# Error handlers
@app.errorhandler(404)
def page_not_found():
    """Обработчик ошибки 404."""
    return "Page not found", 404


@app.errorhandler(500)
def internal_server_error():
    """Обработчик внутренней серверной ошибки."""
    return "Internal Server Error", 500


if __name__ == '__main__':
    api_logger = configure_api_logger()
    app.run(debug=True)
