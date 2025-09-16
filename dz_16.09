import sqlite3
from datetime import date, timedelta

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

print("1. Создание таблиц...")

cursor.execute("PRAGMA foreign_keys = ON")

create_tables_queries = [
    """
    CREATE TABLE IF NOT EXISTS Authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER NOT NULL CHECK (year <= strftime('%Y', 'now')),
        author_id INTEGER NOT NULL,
        genre_id INTEGER NOT NULL,
        FOREIGN KEY (author_id) REFERENCES Authors (id) ON DELETE CASCADE,
        FOREIGN KEY (genre_id) REFERENCES Genres (id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Readers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Book_Issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        reader_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES Books (id) ON DELETE CASCADE,
        FOREIGN KEY (reader_id) REFERENCES Readers (id) ON DELETE CASCADE
    )
    """
]

for query in create_tables_queries:
    cursor.execute(query)
print("   Таблицы успешно созданы.")

print("\n2. Добавление тестовых данных...")

authors_data = [
    ('Айзек Азимов',),
    ('Джордж Оруэлл',),
    ('Энди Хант',)
]
cursor.executemany("INSERT INTO Authors (full_name) VALUES (?)", authors_data)

genres_data = [
    ('Научная фантастика',),
    ('Антиутопия',),
    ('Программирование',)
]
cursor.executemany("INSERT INTO Genres (name) VALUES (?)", genres_data)

conn.commit()

cursor.execute("SELECT id, full_name FROM Authors")
authors = cursor.fetchall()
print("Авторы в базе:", authors)

cursor.execute("SELECT id, name FROM Genres")
genres = cursor.fetchall()
print("Жанры в базе:", genres)

books_data = [
    ('Основание', 1951, 1, 1),
    ('1984', 1949, 2, 2),
    ('Программист-прагматик', 1999, 3, 3)
]

try:
    cursor.executemany("""
        INSERT INTO Books (title, year, author_id, genre_id)
        VALUES (?, ?, ?, ?)
    """, books_data)
    print("   Книги успешно добавлены!")
except sqlite3.IntegrityError as e:
    print(f"   Ошибка целостности данных: {e}")
    print("   Проверьте соответствие author_id и genre_id")

readers_data = [
    ('Иван Петров', 'ivan.petrov@mail.com'),
    ('Мария Сидорова', 'maria.sid@example.com'),
    ('Алексей IT', 'alex.it@dev.com')
]
cursor.executemany("INSERT INTO Readers (full_name, email) VALUES (?, ?)", readers_data)

conn.commit()

cursor.execute("SELECT id, title FROM Books")
books = cursor.fetchall()
print("Книги в базе:", books)

today = date.today().isoformat()
two_weeks_ago = (date.today() - timedelta(days=14)).isoformat()
one_week_ago = (date.today() - timedelta(days=7)).isoformat()

book_issues_data = [
    (1, 1, two_weeks_ago, today),
    (2, 2, one_week_ago, None),
    (3, 3, one_week_ago, None),
    (1, 2, two_weeks_ago, one_week_ago)
]

try:
    cursor.executemany("""
        INSERT INTO Book_Issues (book_id, reader_id, issue_date, return_date)
        VALUES (?, ?, ?, ?)
    """, book_issues_data)
    print("   Выдачи книг успешно добавлены!")
except sqlite3.IntegrityError as e:
    print(f"   Ошибка при добавлении выдач: {e}")

conn.commit()

print("\n3. Выполнение запросов на выборку:")

print("\nа) Список всех книг:")
query_a = """
SELECT
    b.title as 'Название',
    a.full_name as 'Автор',
    g.name as 'Жанр',
    b.year as 'Год'
FROM Books b
JOIN Authors a ON b.author_id = a.id
JOIN Genres g ON b.genre_id = g.id
ORDER BY b.title
"""
cursor.execute(query_a)
for row in cursor.fetchall():
    print(f" - {row[0]} | {row[1]} | {row[2]} | {row[3]}")

print("\nб) Читатели с невозвращенными книгами:")
query_b = """
SELECT DISTINCT
    r.full_name as 'Читатель',
    r.email as 'Email'
FROM Readers r
JOIN Book_Issues bi ON r.id = bi.reader_id
WHERE bi.return_date IS NULL
ORDER BY r.full_name
"""
cursor.execute(query_b)
for row in cursor.fetchall():
    print(f" - {row[0]} ({row[1]})")

print("\nв) Количество книг по авторам:")
query_c = """
SELECT
    a.full_name as 'Автор',
    COUNT(b.id) as 'Количество книг'
FROM Authors a
LEFT JOIN Books b ON a.id = b.author_id
GROUP BY a.id
ORDER BY COUNT(b.id) DESC, a.full_name
"""
cursor.execute(query_c)
for row in cursor.fetchall():
    print(f" - {row[0]}: {row[1]}")

print("\nГотово! База данных создана, наполнена и проанализирована.")
conn.close()
