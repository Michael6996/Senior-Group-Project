import re

users = {}  # Stores accounts as {username: password}

def valid_password(password):
    # At least 8 characters
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False

    # At least one digit
    if not re.search(r"\d", password):
        print("Password must contain at least one digit.")
        return False

    # At least one lowercase letter
    if not re.search(r"[a-z]", password):
        print("Password must contain at least one lowercase letter.")
        return False

    # At least one uppercase letter
    if not re.search(r"[A-Z]", password):
        print("Password must contain at least one uppercase letter.")
        return False

    # At least one symbol
    if not re.search(r"[!@#$%^&*()\-_+=\[\]{};:,.<>/?]", password):
        print("Password must contain at least one symbol.")
        return False

    return True


def sign_up():
    print("\n--- Sign Up ---")
    username = input("Create a username: ")

    if username in users:
        print("Username already exists. Try logging in.")
        return

    while True:
        password = input("Create a password: ")
        if valid_password(password):
            break
        print("Please try again.\n")

    users[username] = password
    print("Account created successfully!")


def login():
    print("\n--- Login ---")
    username = input("Enter username: ")

    if username not in users:
        print("No such user. Please sign up first.")
        return

    password = input("Enter password: ")

    if users[username] == password:
        print("Login successful! Welcome,", username)
    else:
        print("Incorrect password.")


def main():
    while True:
        print("\n=== Menu ===")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

main()
