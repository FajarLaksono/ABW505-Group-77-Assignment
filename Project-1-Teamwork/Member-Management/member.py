import csv
import os
import re
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

MEMBERS_FILE = os.path.join(DATASETS_DIR, "members.csv")
print(f"Members will be saved to: {MEMBERS_FILE}")

# -------------------------------
# Creating File
# -------------------------------
def initialize_members_file():
    if not os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["member_id", "name", "email"])   # header row


# -------------------------------------
# LOAD members.csv → to DATAFRAME (list of dicts)
# -------------------------------------
def load_members():
    initialize_members_file()
    members = []

    with open(MEMBERS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            members.append(row)

    return members


# -------------------------------------
# SAVE DATAFRAME → members.csv
# -------------------------------------
def save_members(data):
    with open(MEMBERS_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["member_id", "name", "email"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)


# -------------------------------------
# CHECK EMAIL FORMAT
# -------------------------------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


# -------------------------------------
# CHECK DUPLICATE MEMBER ID
# -------------------------------------
def does_member_id_exist(data, member_id):
    return any(m["member_id"] == member_id for m in data)


# -------------------------------------
# REGISTER MEMBER
# -------------------------------------
def register_member(data, member_id, name, email):

    # Blank checks
    if not member_id or not name or not email:
        print("❌ member_id, name, and email cannot be blank.")
        return False

    # Duplicate ID check
    if does_member_id_exist(data, member_id):
        print("❌ Member ID already exists!")
        return False

    # Email format validation
    if not is_valid_email(email):
        print("❌ Invalid email format.")
        return False

    # Add to dataframe
    new_member = {
        "member_id": member_id,
        "name": name,
        "email": email
    }

    data.append(new_member)
    print("✅ Member registered successfully!")
    return True


# -------------------------------------
# LIST MEMBERS
# -------------------------------------
def list_members(data):
    if not data:
        print("No members found.")
        return

    print("\n--- Member List ---")
    for m in data:
        print(f"ID: {m['member_id']} | Name: {m['name']} | Email: {m['email']}")


# -------------------------------------
# SEARCH MEMBERS
# -------------------------------------
def search_members(data, keyword):
    print("\n--- Search Results ---")
    keyword = keyword.lower()
    results = []

    for m in data:
        if keyword in m["member_id"].lower() or \
           keyword in m["name"].lower() or \
           keyword in m["email"].lower():
            results.append(m)

    return results
