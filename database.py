import sqlite3
import os

class Database:
    def __init__(self, db_name):
        db_exists = os.path.exists(db_name)
        self.conn = sqlite3.connect(db_name)
        if not db_exists:
            self.create_tables()

    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                publication_year TEXT,
                total_copies INTEGER,
                available_copies INTEGER,
                is_available BOOLEAN DEFAULT TRUE
            )
        ''')

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT
            )
        ''')

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS book_transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_isbn TEXT,
                user_email TEXT,
                issue_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                return_date DATETIME,
                FOREIGN KEY(book_isbn) REFERENCES books(isbn),
                FOREIGN KEY(user_email) REFERENCES users(email)
            )
        ''')

        self.conn.commit()

    def insert_book(self, book_data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO books 
            (isbn, title, author, genre, publication_year, total_copies, available_copies, is_available) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            book_data['isbn'], 
            book_data['title'], 
            book_data['author'], 
            book_data['genre'], 
            book_data['publication_year'], 
            book_data['total_copies'],
            book_data['available_copies'],
            book_data.get('is_available', True)  # Default to True if not provided
        ))
        self.conn.commit()

    def insert_user(self, user_data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (email, name, phone, address) 
            VALUES (?, ?, ?, ?)
        ''', (
            user_data['email'],
            user_data['name'],
            user_data['phone'],
            user_data['address']
        ))
        self.conn.commit()

    def fetch_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books')
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def fetch_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def find_book_by_isbn(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute('SELECT *, available_copies > 0 as is_available FROM books WHERE isbn = ?', (isbn,))
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None


    def find_user_by_email(self, email):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None

    def issue_book(self, isbn, email):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE books 
            SET available_copies = available_copies - 1,
                is_available = CASE WHEN available_copies - 1 > 0 THEN 1 ELSE 0 END
            WHERE isbn = ?
        ''', (isbn,))
        cursor.execute('''
            INSERT INTO book_transactions (book_isbn, user_email)
            VALUES (?, ?)
        ''', (isbn, email))
        self.conn.commit()

    def return_book(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE books 
            SET available_copies = available_copies + 1,
                is_available = CASE WHEN available_copies + 1 > 0 THEN 1 ELSE 0 END
            WHERE isbn = ?
        ''', (isbn,))
        cursor.execute('''
            UPDATE book_transactions SET return_date = CURRENT_TIMESTAMP 
            WHERE book_isbn = ? AND return_date IS NULL
        ''', (isbn,))
        self.conn.commit()


    def count_books(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM books')
        return cursor.fetchone()[0]
