# ============================================
# Part 2 – Loan Management Module
# ============================================

import csv
import os
import sys
import ipynbname
from datetime import datetime

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

LOANS_FILE = os.path.join(DATASETS_DIR, "loans.csv")
print(f"Loans will be saved to: {LOANS_FILE}")
loans = []   # global list to store loan records

# -------------------------------------------------
# Load loans from CSV
# -------------------------------------------------
def load_loans():
    global loans
    loans = []

    if not os.path.exists(LOANS_FILE):
        print(f"File '{LOANS_FILE}' not found. Starting with empty list.")
        return

    with open(LOANS_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            loans.append(row)

    print(f"Loaded {len(loans)} loan(s) from '{LOANS_FILE}'.")


# -------------------------------------------------
# Save loans to CSV
# -------------------------------------------------
def save_loans():
    fieldnames = ["loan_id", "book_id", "member_id", "borrow_date", "due_date", "return_date", "fine"]

    with open(LOANS_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for loan in loans:
            writer.writerow(loan)

    print(f"Saved {len(loans)} loan(s) to '{LOANS_FILE}'.")


# -------------------------------------------------
# Helper: Check if loan_id already exists
# -------------------------------------------------
def is_loan_id_exist(loan_id):
    for loan in loans:
        if loan["loan_id"] == loan_id:
            return True
    return False


# -------------------------------------------------
# Borrow a book
# -------------------------------------------------
def borrow_book():
    print("\n=== Borrow Book ===")

    # Validate loan_id
    while True:
        loan_id = input("Enter Loan ID (e.g. L001): ").strip()
        if loan_id == "":
            print("Loan ID cannot be empty.")
        elif is_loan_id_exist(loan_id):
            print("This Loan ID already exists.")
        else:
            break

    # Validate book_id
    while True:
        book_id = input("Enter Book ID: ").strip()
        if book_id == "":
            print("Book ID cannot be empty.")
        else:
            break

    # Validate member_id
    while True:
        member_id = input("Enter Member ID: ").strip()
        if member_id == "":
            print("Member ID cannot be empty.")
        else:
            break

    # Validate borrow_date
    while True:
        borrow_date = input("Enter Borrow Date (YYYY-MM-DD): ").strip()
        if borrow_date == "":
            print("Borrow Date cannot be empty.")
        else:
            try:
                datetime.strptime(borrow_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    # Validate due_date
    while True:
        due_date = input("Enter Due Date (YYYY-MM-DD): ").strip()
        if due_date == "":
            print("Due Date cannot be empty.")
        else:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    new_loan = {
        "loan_id": loan_id,
        "book_id": book_id,
        "member_id": member_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": "",
        "fine": "0"
    }

    loans.append(new_loan)
    print(f"\nLoan '{loan_id}' has been created successfully!")


# -------------------------------------------------
# Return a book
# -------------------------------------------------
def return_book():
    print("\n=== Return Book ===")

    loan_id = input("Enter Loan ID to return: ").strip()

    # Find the loan
    loan_found = None
    for loan in loans:
        if loan["loan_id"] == loan_id:
            loan_found = loan
            break

    if loan_found is None:
        print(f"Loan ID '{loan_id}' not found.")
        return

    if loan_found["return_date"] != "":
        print(f"This book has already been returned on {loan_found['return_date']}.")
        return

    # Validate return_date
    while True:
        return_date = input("Enter Return Date (YYYY-MM-DD): ").strip()
        if return_date == "":
            print("Return Date cannot be empty.")
        else:
            try:
                datetime.strptime(return_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    # Calculate fine if return date is after due date
    due_date_obj = datetime.strptime(loan_found["due_date"], "%Y-%m-%d")
    return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")

    fine = 0
    if return_date_obj > due_date_obj:
        days_late = (return_date_obj - due_date_obj).days
        fine = days_late * 0.5
        print(f"\nBook is {days_late} day(s) late. Fine: MYR {fine:.2f}")
    else:
        print("\nBook returned on time. No fine.")

    # Update the loan
    loan_found["return_date"] = return_date
    loan_found["fine"] = str(fine)

    print(f"Loan '{loan_id}' has been updated successfully!")


# -------------------------------------------------
# List all loans
# -------------------------------------------------
def list_loans():
    print("\n=== List of Loans ===")

    if len(loans) == 0:
        print("No loans available.")
        return

    print(f"{'Loan ID':<10} {'Book ID':<10} {'Member ID':<12} {'Borrow':<12} {'Due':<12} {'Return':<12} {'Fine':<8}")
    print("-" * 90)

    for loan in loans:
        return_date = loan["return_date"] if loan["return_date"] else "Not returned"
        fine = f"MYR {loan['fine']}" if loan["fine"] else "MYR 0"
        print(f"{loan['loan_id']:<10} {loan['book_id']:<10} {loan['member_id']:<12} "
              f"{loan['borrow_date']:<12} {loan['due_date']:<12} {return_date:<12} {fine:<8}")
