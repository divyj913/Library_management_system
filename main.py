import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from book_management import BookManager
from user_management import UserManager
from database import Database
from PIL import Image, ImageTk  # You'll need to install pillow: pip install pillow

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1200x800")
        
        # Set background color
        self.root.configure(bg="#f0f4f8")
        
        # Initialize database and managers
        self.db = Database("library.db")
        self.book_manager = BookManager(self.db)
        self.user_manager = UserManager(self.db)

        # Create main menu
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a header frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=100)
        header_frame.pack(fill=tk.X)
        
        # Title with improved styling
        title_label = tk.Label(
            header_frame,
            text="GSV LIBRARY MANAGEMENT SYSTEM",
            font=("Helvetica", 28, "bold"),
            fg="white",
            bg="#2c3e50",
            pady=25
        )
        title_label.pack()
        
        # Main content area
        content_frame = tk.Frame(self.root, bg="#f0f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # Left side for buttons
        button_frame = tk.Frame(content_frame, bg="#f0f4f8")
        button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        # Right side for decorative elements
        info_frame = tk.Frame(content_frame, bg="#f0f4f8")
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)
        
        # Welcome message
        welcome_label = tk.Label(
            info_frame,
            text="Welcome to GSV Library",
            font=("Helvetica", 22, "bold"),
            fg="#2c3e50",
            bg="#f0f4f8",
            justify=tk.LEFT
        )
        welcome_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Information text
        info_text = """
        This system helps you manage your library efficiently.
        You can add books and users, issue and return books,
        and keep track of all library resources.
        
        Start by selecting an option from the menu.
        """
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Helvetica", 14),
            fg="#34495e",
            bg="#f0f4f8",
            justify=tk.LEFT,
            wraplength=400
        )
        info_label.pack(anchor=tk.W)
        
        # Section title for buttons
        section_label = tk.Label(
            button_frame,
            text="Main Menu",
            font=("Helvetica", 18, "bold"),
            fg="#2c3e50",
            bg="#f0f4f8"
        )
        section_label.pack(anchor=tk.W, pady=(0, 20))

        # Button definitions with icons and colors
        buttons = [
            ("Add Book", self.open_add_book_window, "#3498db", "#2980b9"),
            ("View Books", self.open_book_list_window, "#2ecc71", "#27ae60"),
            ("Add User", self.open_add_user_window, "#9b59b6", "#8e44ad"),
            ("View Users", self.open_user_list_window, "#e74c3c", "#c0392b"),
            ("Issue Book", self.issue_book, "#f39c12", "#d35400"),
            ("Return Book", self.return_book, "#1abc9c", "#16a085"),
        ]

        # Create styled buttons
        for text, command, bg_color, active_bg in buttons:
            btn_frame = tk.Frame(button_frame, bg="#f0f4f8")
            btn_frame.pack(fill=tk.X, pady=8)
            
            btn = tk.Button(
                btn_frame, 
                text=text,
                command=command,
                font=("Helvetica", 14, "bold"),
                bg=bg_color,
                fg="white",
                activebackground=active_bg,
                activeforeground="white",
                bd=0,
                padx=20,
                pady=12,
                width=20,
                cursor="hand2",
                relief=tk.FLAT
            )
            btn.pack(fill=tk.X)

        # Footer
        footer_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2025 GSV Library Management System | All Rights Reserved",
            font=("Helvetica", 10),
            fg="white",
            bg="#2c3e50",
            pady=15
        )
        footer_text.pack()

    # Your existing methods remain unchanged
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
