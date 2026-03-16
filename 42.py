from flask import Flask, session, request, flash, redirect, url_for, render_template
import os

app = Flask(__name__)
app.secret_key = "arbuz52"

# Данные для авторизации
VALID_USER = 'student'
VALID_PASS = 'cerber666'

# База данных книг
books = [
    {
        "id": 1,
        "title": "Flask для начинающих",
        "category": "Книга",
        "author": "Иванов И.И.",
        "description": "Введение во Flask. Основы создания веб-приложений."
    },
    {
        "id": 2,
        "title": "Python мастерство",
        "category": "Книга",
        "author": "Петров П.П.",
        "description": "Продвинутые техники программирования на Python."
    },
    {
        "id": 3,
        "title": "Веб-разработка",
        "category": "Учебник",
        "author": "Сидоров С.С.",
        "description": "Полный курс по современной веб-разработке."
    }
]


def get_next_id():
    """Получить следующий ID для новой книги"""
    return max(book["id"] for book in books) + 1 if books else 1


@app.route('/base')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/books')
def books_list():
    """Список всех книг"""
    return render_template('books.html', books=books)


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    """Детальная страница книги"""
    book = None
    for b in books:
        if b["id"] == book_id:
            book = b
            break

    if book:
        return render_template('books_detail.html', book=book)
    else:
        flash('Книга не найдена', 'danger')
        return redirect(url_for('books_list'))


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    """Добавление новой книги"""
    if 'username' not in session:
        flash('Необходимо войти в систему', 'warning')
        return redirect(url_for('login'))

    if request.method == "POST":
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        author = request.form.get('author', '').strip()
        description = request.form.get('description', '').strip()

        if not title or not author:
            flash('Название и автор обязательны', 'danger')
            return redirect(request.url)

        new_book = {
            "id": get_next_id(),
            "title": title,
            "category": category if category else "Книга",
            "author": author,
            "description": description if description else "Описание отсутствует"
        }

        books.append(new_book)
        flash(f'Книга "{title}" добавлена!', 'success')
        return redirect(url_for('books_list'))

    return render_template('add_book.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Авторизация"""
    if request.method == "POST":
        user = request.form.get('username')
        password = request.form.get('password')

        if user == VALID_USER and password == VALID_PASS:
            session['username'] = user
            flash(f"Добро пожаловать, {user}!", 'success')
            return redirect(url_for('add_book'))  # Редирект на добавление
        else:
            flash('Неверный логин или пароль', 'danger')

    return render_template("login.html")


@app.route('/stats')
def stats():
    """Статистика"""
    if 'username' not in session:
        flash('Сначала войдите в систему!', 'warning')
        return redirect(url_for('login'))

    # Подсчет статистики
    total_books = len(books)
    categories = len(set(book['category'] for book in books))
    authors = len(set(book['author'] for book in books))

    # Книги по категориям
    books_by_category = {}
    for book in books:
        cat = book['category']
        books_by_category[cat] = books_by_category.get(cat, 0) + 1

    stats_data = {
        'total_books': total_books,
        'categories': categories,
        'authors': authors,
        'books_by_category': books_by_category,
        'username': session['username']
    }

    return render_template("stats.html", stats=stats_data)


@app.route('/logout')
def logout():
    """Выход"""
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)