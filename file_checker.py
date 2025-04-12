import hashlib
import os
import json

HASH_FILE = "hashes.json"

def generate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def save_hash(file_path):
    hash_value = generate_hash(file_path)
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            hashes = json.load(f)
    else:
        hashes = {}

    hashes[file_path] = hash_value
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=4)
    print("Hash saved.")

def check_file(file_path):
    if not os.path.exists(HASH_FILE):
        print("No saved hashes found.")
        return

    with open(HASH_FILE, "r") as f:
        hashes = json.load(f)

    if file_path not in hashes:
        print("File not found in saved hash list.")
        return

    current_hash = generate_hash(file_path)
    if current_hash == hashes[file_path]:
        print("File is unchanged.")
    else:
        print("WARNING: File has been modified!")

if __name__ == "__main__":
    print("1. Save file hash")
    print("2. Check file integrity")
    choice = input("Enter your choice: ")
    path = input("Enter file path (e.g., files/test.txt): ")

    if choice == "1":
        save_hash(path)
    elif choice == "2":
        check_file(path)
    else:
        print("Invalid choice.")
