import tkinter as tk
from tkinter import ttk
import json

# Define the Book class to represent individual books
class Book:
    def __init__(self, title, author, genre, pages, read_status=False):
        self.title = title
        self.author = author
        self.genre = genre
        self.pages = pages
        self.read_status = read_status

# Define the Library class to manage the collection of books
class Library:
    def __init__(self):
        self.books = []
        self.load_data()

    def add_book(self, book):
        self.books.append(book)

    def search_books(self, keyword):
        matching_books = [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
        return matching_books

    def display_books(self, book_list=None):
        books_to_display = book_list or self.books
        if not books_to_display:
            return "No books found."
        else:
            result = ""
            for i, book in enumerate(books_to_display, start=1):
                result += f"{i}. Title: {book.title}, Author: {book.author}, Genre: {book.genre}, Pages: {book.pages}, Read: {book.read_status}.\n"
            return result


    def update_read_status(self, book_title):
        found_book = next((book for book in self.books if book.title.lower() == book_title.lower()), None)
        if found_book:
            found_book.read_status = not found_book.read_status
            status = "read" if found_book.read_status else "unread"
            return f"Read status for '{found_book.title}' has been updated to {status}."
        else:
            return f"Book with title '{book_title}' not found in the library."

    def get_reading_statistics(self):
        total_books = len(self.books)
        read_books = sum(book.read_status for book in self.books)
        unread_books = total_books - read_books
        return f"Reading statistics \nTotal books: {total_books}\nRead books: {read_books}\nUnread books: {unread_books}"

    def delete_book(self, book_title):
        found_book = next((book for book in self.books if book.title.lower() == book_title.lower()), None)
        if found_book:
            self.books.remove(found_book)
            return f"Book '{book_title}' deleted from the library."
        else:
            return f"Book with title '{book_title}' not found in the library."

    def load_data(self):
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)
                for book_data in data:
                    book = Book(book_data["title"], book_data["author"], book_data["genre"], book_data["pages"], book_data["read_status"])
                    self.books.append(book)
        except FileNotFoundError:
            pass

    def save_data(self):
        data = []
        for book in self.books:
            data.append({"title": book.title, "author": book.author, "genre": book.genre, "pages": book.pages, "read_status": book.read_status})
        with open("library_data.json", "w") as file:
            json.dump(data, file)

# Tkinter GUI Application
class LibraryGUI:
    def __init__(self, root, library):
        self.root = root
        self.root.title("Personal Library")
        self.library = library
        self.create_menu_frame()

    def create_menu_frame(self):
        # Main menu frame
        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.grid(row=0, column=0, padx=175)
        self.menu_frame.columnconfigure(0, weight=1)
        title_label = ttk.Label(self.menu_frame, text='Personal Library', font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(20, 10) , sticky='n')

        # Buttons for different actions
        ttk.Button(self.menu_frame, text="1. Add a Book", width=35, command=self.show_add_book_frame).grid(row=1, column=0, pady=(20,5))
        ttk.Button(self.menu_frame, text="2. Search for Books", width=35, command=self.show_search_books_frame).grid(row=2, column=0, pady=5)
        ttk.Button(self.menu_frame, text="3. Display All Books", width=35, command=self.show_display_books_frame).grid(row=3, column=0, pady=5)
        ttk.Button(self.menu_frame, text="4. Update Read Status", width=35, command=self.show_update_read_status_frame).grid(row=4, column=0, pady=5)
        ttk.Button(self.menu_frame, text="5. Reading Statistics", width=35, command=self.show_reading_statistics_frame).grid(row=5, column=0, pady=5)
        ttk.Button(self.menu_frame, text="6. Delete a Book", width=35, command=self.show_delete_book_frame).grid(row=6, column=0, pady=5)
        ttk.Button(self.menu_frame, text="7. Exit", width=35, command=self.root.destroy).grid(row=7, column=0, pady=(5,20))

    def show_add_book_frame(self):
        # Frame to add a book
        self.clear_frames()
        self.add_book_frame = ttk.Frame(self.root)
        self.add_book_frame.grid(row=0, column=1, padx=150)

        title_label = ttk.Label(self.add_book_frame, text='Personal Library', font=('Arial', 14, 'bold'), padding=20)
        title_label.grid(row=0, column=0, columnspan=2, pady=(20,10), sticky='n')

        ttk.Label(self.add_book_frame, text="Title:", padding=5).grid(row=1, column=0, sticky=tk.E)
        self.title_entry = ttk.Entry(self.add_book_frame, width=40)
        self.title_entry.grid(row=1, column=1)

        ttk.Label(self.add_book_frame, text="Author:", padding=5).grid(row=2, column=0, sticky=tk.E)
        self.author_entry = ttk.Entry(self.add_book_frame, width=40)
        self.author_entry.grid(row=2, column=1)

        ttk.Label(self.add_book_frame, text="Genre:", padding=5).grid(row=3, column=0, sticky=tk.E)
        self.genre_entry = ttk.Entry(self.add_book_frame, width=40)
        self.genre_entry.grid(row=3, column=1)

        ttk.Label(self.add_book_frame, text="Pages:", padding=5).grid(row=4, column=0, sticky=tk.E)
        self.pages_entry = ttk.Entry(self.add_book_frame, width=40)
        self.pages_entry.grid(row=4, column=1)

        ttk.Button(self.add_book_frame, text="Add Book", command=self.add_book).grid(row=5, column=0, columnspan=2, pady=5)

    def show_search_books_frame(self):
        # Frame to search for books
        self.clear_frames()
        self.search_books_frame = ttk.Frame(self.root)
        self.search_books_frame.grid(row=0, column=1, padx=100)

        title_label = ttk.Label(self.search_books_frame, text='Personal Library', font=('Arial', 14, 'bold'), padding=20)
        title_label.grid(row=0, column=0, columnspan=2, pady=(20,10), sticky='n')

        ttk.Label(self.search_books_frame, text="Title or Author of the Book:").grid(row=1, column=0, sticky=tk.E)
        self.search_entry = ttk.Entry(self.search_books_frame, width=40)
        self.search_entry.grid(row=1, column=1)

        ttk.Button(self.search_books_frame, text="Search", command=self.search_books).grid(row=2, column=0, columnspan=2, pady=5)

    def show_display_books_frame(self):
        # Frame to display all books
        self.clear_frames()
        result = self.library.display_books()
        self.display_result_frame("Display Books", result)

    def show_update_read_status_frame(self):
        # Frame to update read status
        self.clear_frames()
        self.update_read_status_frame = ttk.Frame(self.root)
        self.update_read_status_frame.grid(row=0, column=1, padx=150)
        title_label = ttk.Label(self.update_read_status_frame, text='Personal Library', font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky='n') 


        ttk.Label(self.update_read_status_frame, text="Title of The Book:", padding=10).grid(row=1, column=0, sticky=tk.E)
        self.update_status_entry = ttk.Entry(self.update_read_status_frame, width=30)
        self.update_status_entry.grid(row=1, column=1)

        ttk.Button(self.update_read_status_frame, text="Update Status", command=self.update_read_status).grid(row=2, column=0, columnspan=2, pady=5)

    def show_reading_statistics_frame(self):
        # Frame to display reading statistics
        self.clear_frames()
        self.reading_statistics_frame = ttk.Frame(self.root)
        self.reading_statistics_frame.grid(row=0, column=1, padx=220)
        
        result = self.library.get_reading_statistics()
        self.display_result_frame("Reading Statistics", result)

    def show_delete_book_frame(self):
        # Frame to delete a book
        self.clear_frames()
        self.delete_book_frame = ttk.Frame(self.root)
        self.delete_book_frame.grid(row=0, column=1, padx=150)

        title_label = ttk.Label(self.delete_book_frame, text='Personal Library', font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky='n') 

        ttk.Label(self.delete_book_frame, text="Title of The Book:", padding=10).grid(row=1, column=0, sticky=tk.E)
        self.delete_entry = ttk.Entry(self.delete_book_frame, width=35)
        self.delete_entry.grid(row=1, column=1)

        ttk.Button(self.delete_book_frame, text="Delete Book", command=self.delete_book).grid(row=2, column=0, columnspan=2, pady=5)

    def add_book(self):
        # Add a book to the library
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        try:
            pages = int(self.pages_entry.get())
        except ValueError:
            pages = int(input("Please enter a correct number: "))
        book = Book(title, author, genre, pages)
        self.library.add_book(book)
        self.clear_frames()
        self.display_result_frame("Book added", "Book added to the library.")

    def search_books(self):
        # Search for books based on title or author
        keyword = self.search_entry.get()
        matching_books = self.library.search_books(keyword)
        if matching_books:
            result = self.library.display_books(matching_books)
            self.clear_frames()
            self.display_result_frame("Matching Books", result)
        else:
            self.clear_frames()
            self.display_result_frame("No Matching Books", "No matching books found.")

    def update_read_status(self):
        # Update read status of a book
        book_title = self.update_status_entry.get()
        result = self.library.update_read_status(book_title)
        self.clear_frames()
        self.display_result_frame("Update Read Status", result)

    def delete_book(self):
        # Delete a book
        book_title = self.delete_entry.get()
        result = self.library.delete_book(book_title)
        self.clear_frames()
        self.display_result_frame("Delete Book", result)

    def clear_frames(self):
        # Clear all frames on the root window
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()

    def display_result_frame(self, title, result):
        # Create a frame for displaying results
        result_frame = ttk.Frame(self.root)
        result_frame.grid(row=1, column=1, padx=40)

        title_label = ttk.Label(result_frame, text='Personal Library', font=('Arial', 14, 'bold'), padding=5)
        title_label.grid(row=0, column=0, columnspan=2, pady=(20,10), sticky='n')

        # Display the result and add button to go back to the main menu
        ttk.Label(result_frame, text=title).grid(row=1, column=0, columnspan=2, pady=(20,5))
        result_text = tk.Text(result_frame, height=10, width=65)
        result_text.grid(row=2, column=0, columnspan=2, pady=5)
        result_text.insert(tk.END, result)
        ttk.Button(result_frame, text="Back to Menu", command=self.create_menu_frame).grid(row=3, column=0, columnspan=2, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    library = Library()
    app = LibraryGUI(root, library)
    root.geometry("600x375")
    
    root.mainloop()

    library.save_data()
