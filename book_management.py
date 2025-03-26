# library_management_system/book_management.py
class BookManager:
    def __init__(self, database):
        self.db = database

    def add_book(self, book_data):
        # Validate book data
        required_fields = ['title', 'author', 'isbn', 'genre', 'publication_year']
        for field in required_fields:
            if not book_data.get(field):
                raise ValueError(f"{field.capitalize()} is required")

        # Additional validation
        if not book_data['isbn'].isdigit():
            raise ValueError("ISBN must be a number")
        
        book_data['is_available'] = True
        self.db.insert_book(book_data)
        return "Book added successfully"

    def get_all_books(self):
        return self.db.fetch_all_books()

    def issue_book(self, book_isbn, user_email):
        # Check book availability
        book = self.db.find_book_by_isbn(book_isbn)
        user = self.db.find_user_by_email(user_email)

        if not book:
            raise ValueError("Book not found")
        if not user:
            raise ValueError("User not found")
        if not book['is_available']:
            raise ValueError("Book is already issued")

        # Update book status and record transaction
        self.db.issue_book(book_isbn, user_email)
        return "Book issued successfully"

    def return_book(self, book_isbn):
        # Validate book return
        book = self.db.find_book_by_isbn(book_isbn)

        if not book:
            raise ValueError("Book not found")
        if book['is_available']:
            raise ValueError("Book was not issued")

        # Process book return
        self.db.return_book(book_isbn)
        return "Book returned successfully"