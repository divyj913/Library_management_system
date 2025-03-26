# library_management_system/database.py
import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        # Create books table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                publication_year TEXT,
                is_available BOOLEAN DEFAULT TRUE,
                current_user_email TEXT
            )
        ''')

        # Create users table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT
            )
        ''')

        # Create book transactions table
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
            (isbn, title, author, genre, publication_year, is_available) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            book_data['isbn'], 
            book_data['title'], 
            book_data['author'], 
            book_data['genre'], 
            book_data['publication_year'], 
            book_data['is_available']
        ))
        self.conn.commit()

    def insert_user(self, user_data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users 
            (email, name, phone, address) 
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
        cursor.execute('SELECT * FROM books WHERE isbn = ?', (isbn,))
        result = cursor.fetchone()
        
        if result:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, result))
        return None

    def find_user_by_email(self, email):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()
        
        if result:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, result))
        return None

    def issue_book(self, book_isbn, user_email):
        cursor = self.conn.cursor()
        
        # Update book availability
        cursor.execute('''
            UPDATE books 
            SET is_available = FALSE, current_user_email = ? 
            WHERE isbn = ?
        ''', (user_email, book_isbn))

        # Record transaction
        cursor.execute('''
            INSERT INTO book_transactions 
            (book_isbn, user_email) 
            VALUES (?, ?)
        ''', (book_isbn, user_email))

        self.conn.commit()

    def return_book(self, book_isbn):
        cursor = self.conn.cursor()
        
        # Update book availability
        cursor.execute('''
            UPDATE books 
            SET is_available = TRUE, current_user_email = NULL 
            WHERE isbn = ?
        ''', (book_isbn,))

        # Update transaction return date
        cursor.execute('''
            UPDATE book_transactions 
            SET return_date = CURRENT_TIMESTAMP 
            WHERE book_isbn = ? AND return_date IS NULL
        ''', (book_isbn,))

        self.conn.commit()

    def __del__(self):
        self.conn.close()