import tkinter as tk

import requests

from Book import Book
from RecommendedBooks import agent

books = []


def rec_books():
    # Creates a new window
    window = tk.Toplevel(root)

    # Creates a label for the window
    label = tk.Label(window, text='Recommended Books')
    label.pack()

    # Creates a frame to hold the book details
    frame = tk.Frame(window)
    frame.pack()

    recommended = agent(books)

    # Loop through each book and display its details
    for book in recommended:
        author_title_label = tk.Label(frame, text=f"{book.title} by {book.author}", font='bold', wraplength=800)
        author_title_label.pack()

        # Create a label for the book's description
        description_label = tk.Label(frame, text=f"Average Rating: {book.rating}")
        description_label.pack()


def book_search(title):
    url = "http://openlibrary.org/search.json"  # base url

    # Create the query string and make the API call
    query = {
        "q": title,
        "limit": 1
    }

    response = requests.get(url, params=query)  # get info from website

    book = response.json()['docs'][0]  # takes in the first book from search

    return book


# Create a function to add a book to the list
def add_book():
    # Get the title entered by the user
    title = title_entry.get()
    book_d = book_search(title)
    title = book_d.get("title")  # finds the title from site
    author = ", ".join(book_d.get("author_name", ["Unknown"]))  # finds the author from site
    rating = book_d.get("ratings_average", "Not rated")  # finds the rating from site
    genre = ", ".join(book_d.get("subject", ["Unknown"]))  # finds the genre from site

    # Create a Book to store all the variables of the book found
    book = Book(title, author, rating, genre, book_d, 1)

    # Add the book to the end of the list
    books.append(book)

    # Clears the input fields
    title_entry.delete(0, tk.END)

    # Display the list of books
    display_books()


# Create a function to display the list of books
def display_books():
    # Clear the existing list of books
    for child in book_frame.winfo_children():
        child.destroy()

    # Loop through each book and display its details
    for book in books:
        # Create a label for the book's author and title
        author_title_label = tk.Label(book_frame, text=f"{book.title} by {book.author}", font='bold', wraplength=800)
        author_title_label.pack()

        # Create a label for the book's description
        description_label = tk.Label(book_frame, text=f"Average Rating: {book.rating}")
        description_label.pack()


# Creates the main window
root = tk.Tk()

# Creates labels and entry fields for the user to put in the title
title_label = tk.Label(root, text='Title:')
title_label.pack()
title_entry = tk.Entry(root)
title_entry.pack()

# Create a button to add a book to the list
add_button = tk.Button(root, text='Add Book', command=add_book)
add_button.pack()

# Create a button to get the recommended list
add_button = tk.Button(root, text='Recommend Books', command=rec_books)
add_button.pack()

# Create a frame to hold the list of books
book_frame = tk.Frame(root)
book_frame.pack()

# Run the main loop
root.mainloop()
