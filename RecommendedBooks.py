from collections import Counter

import requests
from Book import Book

books = []


def agent(books_g):
    books.clear()  # resets books
    top_genres = find_genres(books_g)  # finds the state
    # cycles through each genre
    for genre in top_genres:
        books_by_genre(genre, top_genres)  # does the search for each book
    no_repeats(books)
    return books


def find_genres(books_g):
    genres = set()
    # cycles through all the books and adds the genres to the list of genres
    for book in books_g:
        genres.update(book.data.get("subject", ["Unknown"]))
    genres = list(genres)
    genre_counts = Counter(genres)  # counts the genres
    return [genre for genre, count in genre_counts.most_common(7)]  # returns the top seven most frequent genres


def no_repeats(book):
    all_books = book.copy()
    books.clear()
    # makes sure multiple copies of each book aren't added
    for i, book1 in enumerate(all_books):
        same = False  # resets same
        for j, book2 in enumerate(all_books[i + 1:], i + 1):
            if book1.title == book2.title:  # checks if there are 2 books with the same title
                same = True  # sets same to true
        if not same:  # if 2 books don't have the same title add book to books
            books.append(book1)
    books.sort(key=lambda x: x.similar_genres, reverse=True)  # sorts books by number of popular genres
    return books


def books_by_genre(genre, top):
    all_books = []
    url = f"http://openlibrary.org/search.json"  # base url
    query = {
        "q": "subject:{}".format(genre),  # sets subject
        "limit": 50  # sets limit of books
    }
    response = requests.get(url, params=query)  # gets info from website

    # Extract the book titles from the response
    book = response.json()["docs"]

    # checks if the books have more than 1 of the popular genres
    for b in book:
        many = 0  # sets how many popular genres the book has
        genres = b.get("subject", "")  # retrieves the genre from the b
        for g in top:  # cycles through each popular genre
            if genres.count(g) > 0:  # checks if the b contains the popular genre
                many = many + 1  # increase many by 1
        if many >= 2:  # if book has more than 1 genre adds the b to the list of all_books
            title = b["title"]  # finds title
            author = ", ".join(b.get("author_name", ["Unknown"]))  # finds author
            rating = b.get("ratings_average", "Not rated")  # finds rating
            all_books.append(Book(title, author, rating, genres, b, many))  # adds b to all_books

    # makes sure multiple copies of each book aren't added
    for i, book1 in enumerate(all_books):
        same = False  # resets same
        for j, book2 in enumerate(all_books[i + 1:], i + 1):
            if book1.title == book2.title:  # checks if there are 2 books with the same title
                same = True  # sets same to true
        if not same:  # if 2 books don't have the same title add book to books
            books.append(book1)
