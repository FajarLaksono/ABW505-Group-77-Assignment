# ============================================
# Part 1 – Book Management Module
# ============================================

import csv
import os
import sys
import ipynbname

# Check if DATASETS_DIR is set by main script (via environment variable)
if 'LMS_DATASETS_DIR' in os.environ:
    # Running from main script - use the pre-set directory
    DATASETS_DIR = os.environ['LMS_DATASETS_DIR']
    print("Using Datasets directory from main script")
else:
    # Running standalone - calculate the directory
    notebook_path = ipynbname.path()
    print("Current path: ", notebook_path.parent)
    sys.path.insert(0, notebook_path.parent.as_posix())

    # Find Project-1 directory by walking up the path
    def find_project_dir(path):
        current = path.parent
        while current.name != "":
            if current.name == "Project-1":
                return str(current)
            current = current.parent
        return str(path.parent.parent) if "Management" in str(path.parent) else str(path.parent)

    PROJECT_DIR = find_project_dir(notebook_path)
    DATASETS_DIR = os.path.join(PROJECT_DIR, "Datasets")
    os.makedirs(DATASETS_DIR, exist_ok=True)

BOOKS_FILE = os.path.join(DATASETS_DIR, "books.csv")
print(f"Books will be saved to: {BOOKS_FILE}")
books = []   # global list to store book records

# -------------------------------------------------
# Load books from CSV
# -------------------------------------------------
def load_books():
    global books
    books = []

    if not os.path.exists(BOOKS_FILE):
        print(f"File '{BOOKS_FILE}' not found. Starting with empty list.")
        return

    with open(BOOKS_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(row)

    print(f"Loaded {len(books)} book(s) from '{BOOKS_FILE}'.")


# -------------------------------------------------
# Save books to CSV
# -------------------------------------------------
def save_books():
    fieldnames = ["book_id", "title", "author", "year", "available"]

    with open(BOOKS_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book)

    print(f"Saved {len(books)} book(s) to '{BOOKS_FILE}'.")


# -------------------------------------------------
# Helper: Check if book_id already exists
# -------------------------------------------------
def does_book_id_exist(book_id):
    for book in books:
        if book["book_id"] == book_id:
            return True
    return False


# -------------------------------------------------
# Add a new book (with validation)
# -------------------------------------------------
def add_book():
    print("\n=== Add New Book ===")

    while True:
        book_id = input("Enter Book ID (e.g. B001): ").strip()
        if book_id == "":
            print("Book ID cannot be empty.")
        elif does_book_id_exist(book_id):
            print("This Book ID already exists.")
        else:
            break

    while True:
        title = input("Enter Book Title: ").strip()
        if title == "":
            print("Title cannot be empty.")
        else:
            break

    while True:
        author = input("Enter Author Name: ").strip()
        if author == "":
            print("Author cannot be empty.")
        else:
            break

    while True:
        year = input("Enter Publication Year: ").strip()
        if not year.isdigit():
            print("Year must be digits.")
        else:
            break

    new_book = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "year": year,
        "available": "yes"
    }

    books.append(new_book)
    print(f"\nBook '{title}' has been added successfully!")


# -------------------------------------------------
# List all books
# -------------------------------------------------
def list_books():
    print("\n=== List of Books ===")

    if len(books) == 0:
        print("No books available.")
        return

    print(f"{'ID':<10} {'Title':<30} {'Author':<20} {'Year':<6} {'Available':<9}")
    print("-" * 80)

    for book in books:
        print(f"{book['book_id']:<10} {book['title']:<30} {book['author']:<20} "
              f"{book['year']:<6} {book['available']:<9}")


# -------------------------------------------------
# Search books (by title or author)
# -------------------------------------------------
def search_books():
    print("\n=== Search Books ===")
    keyword = input("Enter keyword: ").strip().lower()

    if keyword == "":
        print("Keyword cannot be empty.")
        return

    results = []
    for book in books:
        if keyword in book["title"].lower() or keyword in book["author"].lower():
            results.append(book)

    if len(results) == 0:
        print("No matching books found.")
        return

    print(f"\nFound {len(results)} result(s):\n")
    print(f"{'ID':<10} {'Title':<30} {'Author':<20} {'Year':<6} {'Available':<9}")
    print("-" * 80)

    for book in results:
        print(f"{book['book_id']:<10} {book['title']:<30} {book['author']:<20} "
              f"{book['year']:<6} {book['available']:<9}")
