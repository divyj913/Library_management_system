import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from book_management import BookManager
from user_management import UserManager
from database import Database

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1960x1080")

        # Initialize database and managers
        self.db = Database("library.db")
        self.book_manager = BookManager(self.db)
        self.user_manager = UserManager(self.db)

        # Create main menu
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.root,
            text="Library management system for gsv",
            font=("Blanka", 24, "bold"),
            fg="black",
        )
        title_label.pack(pady=20)

        menu_frame = tk.Frame(self.root, padx=20, pady=20)
        menu_frame.pack(expand=True)

        buttons = [
            ("Add Book", self.open_add_book_window),
            ("View Books", self.open_book_list_window),
            ("Add User", self.open_add_user_window),
            ("View Users", self.open_user_list_window),
            ("Issue Book", self.issue_book),
            ("Return Book", self.return_book),
        ]

        for text, command in buttons:
            btn = tk.Button(menu_frame, text=text, command=command,
                            width=20, height=2, font=("Arial", 12))
            btn.pack(pady=10)

    def open_add_book_window(self):
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("Add Book")
        add_book_window.geometry("400x500")

        labels = ["Title", "Author", "ISBN", "Genre", "Publication Year", "Total Copies"]
        entries = {}

        for label in labels:
            tk.Label(add_book_window, text=label).pack(pady=(10, 0))
            entry = tk.Entry(add_book_window, width=40)
            entry.pack()
            entries[label.lower().replace(" ", "_")] = entry

        def save_book():
            book_data = {key: entry.get() for key, entry in entries.items()}
            try:
                book_data['available_copies'] = int(book_data['total_copies'])  # Set available_copies = total_copies initially
                book_data['total_copies'] = int(book_data['total_copies'])
                self.book_manager.add_book(book_data)
                messagebox.showinfo("Success", "Book added successfully!")
                add_book_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(add_book_window, text="Save Book", command=save_book).pack(pady=20)

    def open_book_list_window(self):
        book_list_window = tk.Toplevel(self.root)
        book_list_window.title("Book List")
        book_list_window.geometry("900x500")

        books = self.book_manager.get_all_books()

        columns = ("Title", "Author", "ISBN", "Genre", "Publication Year", "Total Copies", "Available Copies")
        tree = ttk.Treeview(book_list_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for book in books:
            tree.insert("", "end", values=(
                book['title'], book['author'], book['isbn'],
                book['genre'], book['publication_year'],
                book['total_copies'], book['available_copies'],
            ))

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def open_add_user_window(self):
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Add User")
        add_user_window.geometry("400x500")

        labels = ["Name", "Email", "Phone", "Address"]
        entries = {}

        for label in labels:
            tk.Label(add_user_window, text=label).pack(pady=(10, 0))
            entry = tk.Entry(add_user_window, width=40)
            entry.pack()
            entries[label.lower()] = entry

        def save_user():
            user_data = {key: entry.get() for key, entry in entries.items()}
            try:
                self.user_manager.add_user(user_data)
                messagebox.showinfo("Success", "User added successfully!")
                add_user_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(add_user_window, text="Save User", command=save_user).pack(pady=20)

    def open_user_list_window(self):
        user_list_window = tk.Toplevel(self.root)
        user_list_window.title("User List")
        user_list_window.geometry("800x500")

        users = self.user_manager.get_all_users()

        columns = ("Name", "Email", "Phone", "Address")
        tree = ttk.Treeview(user_list_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        for user in users:
            tree.insert("", "end", values=(
                user['name'], user['email'], user['phone'], user['address']
            ))

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def issue_book(self):
        book_isbn = simpledialog.askstring("Issue Book", "Enter Book ISBN:")
        user_email = simpledialog.askstring("Issue Book", "Enter User Email:")

        if book_isbn and user_email:
            try:
                result = self.book_manager.issue_book(book_isbn, user_email)
                messagebox.showinfo("Success", result)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def return_book(self):
        book_isbn = simpledialog.askstring("Return Book", "Enter Book ISBN:")

        if book_isbn:
            try:
                result = self.book_manager.return_book(book_isbn)
                messagebox.showinfo("Success", result)
            except Exception as e:
                messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
