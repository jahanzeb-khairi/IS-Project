import os
import time
from datetime import datetime
import sys
import getpass
import msvcrt

OTP = "cat"

def masked_input(prompt=""):
    print(prompt, end='', flush=True)
    input_chars = []
    while True:
        char = msvcrt.getch()  
        if char in {b'\r', b'\n'}:
            print() 
            break
        elif char == b'\x08':
            if input_chars: 
                input_chars.pop()
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            input_chars.append(char.decode('utf-8'))
            sys.stdout.write('*')
            sys.stdout.flush()
    return ''.join(input_chars)

def add_spaces(input_str: str, total_length: int) -> str:
    if len(input_str) >= total_length:
        return input_str
    spaces_to_add = total_length - len(input_str)
    spaces_at_start = spaces_to_add // 2
    spaces_at_end = spaces_to_add - spaces_at_start
    result = '_' * spaces_at_start + input_str + '_' * spaces_at_end
    return result

def clear():
    input("Press Enter...")
    os.system('cls' if os.name == 'nt' else 'clear')

def hash_string(string: str) -> int:
    hash_value = 0
    for c in string:
        hash_value = ((hash_value << 5) + hash_value + ord(c)) & 0xFFFFFFFF
    return hash_value

def get_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def log_consent(username: str, action: str):
    try:
        with open("consent.txt", "a") as consent_file:
            current_date = get_current_date()
            consent_file.write(f"User: {username} Action: {action} Date: {current_date}\n")
    except IOError:
        print("Error: Could not open consent log file.")

def log_audit(username: str, action: str, details: str):
    try:
        with open("audit.txt", "a") as audit_file:
            current_date = get_current_date()
            audit_file.write(f"User: {username} Action: {action} Details: {details} Date: {current_date}\n")
    except IOError:
        print("Error: Could not open audit log file.")

def read_file_lines(filename: str, max_lines: int = 10) -> list:
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()[:max_lines]]
    except IOError:
        print(f"Error: Could not open file {filename}")
        return []

def read_file_hashes(filename: str, max_lines: int = 10) -> list:
    try:
        with open(filename, 'r') as file:
            return [int(line.strip()) for line in file.readlines()[:max_lines]]
    except IOError:
        print(f"Error: Could not open file {filename}")
        return []

def append_to_file(word: str, filename: str):
    try:
        with open(filename, "a") as file:
            file.write(f"{word}\n")
    except IOError:
        print(f"Error: Could not open file {filename} for writing.")

def append_hash(hash_value: int, filename: str):
    try:
        with open(filename, "a") as file:
            file.write(f"{hash_value}\n")
    except IOError:
        print(f"Error: Could not open file {filename} for writing.")

def create_files(username: str):
    filenames = ["product.txt", "quantity.txt", "buy.txt", "sell.txt", "time.txt"]
    for filename in filenames:
        full_filename = f"{username}_{filename}"
        try:
            with open(full_filename, 'w') as file:
                print(f"Created file: {full_filename}")
        except IOError:
            print(f"Error creating file: {full_filename}")

class Database:
    def __init__(self):
        self.product_name = [""] * 10
        self.quantity = [""] * 10
        self.buy_price = [""] * 10
        self.sell_price = [""] * 10
        self.last_updated = [""] * 10

    def view(self, name: str):
        clear()
        self.product_name = read_file_lines(f"{name}_product.txt")
        self.quantity = read_file_lines(f"{name}_quantity.txt")
        self.buy_price = read_file_lines(f"{name}_buy.txt")
        self.sell_price = read_file_lines(f"{name}_sell.txt")
        self.last_updated = read_file_lines(f"{name}_time.txt")

        print("_" * 90)
        print("|__No__|_____Product Name_____|__Quantity__|__Buy Price__|__Sell Price__|__Last Updated__|")
        
        for i in range(len(self.product_name)):
            if not self.product_name[i]:
                break
                
            if i < 9:
                print(f"|__{i+1}___|_____{add_spaces(self.product_name[i], 12)}_____|__{add_spaces(self.quantity[i], 8)}__|__{add_spaces(self.buy_price[i], 9)}__|__{add_spaces(self.sell_price[i], 10)}__|__{add_spaces(self.last_updated[i], 12)}__|")
            else:
                print(f"|__{i+1}__|_____{add_spaces(self.product_name[i], 12)}_____|__{add_spaces(self.quantity[i], 8)}__|__{add_spaces(self.buy_price[i], 9)}__|__{add_spaces(self.sell_price[i], 10)}__|__{add_spaces(self.last_updated[i], 12)}__|")

    def insert(self, username: str):
        clear()
        print("-----Enter Product Details-----")
        prod = input("Enter product name: \n")
        qty = input("Enter quantity of product: \n")
        buy = input("Enter buying price of product: \n")
        sell = input("Enter selling price of product: \n")
        time = get_current_date()

        consent = input("Do you consent to this action? (Yes/No): \n")
        if consent.lower() == "yes":
            log_consent(username, "Insert product")
            append_to_file(prod, f"{username}_product.txt")
            append_to_file(qty, f"{username}_quantity.txt")
            append_to_file(buy, f"{username}_buy.txt")
            append_to_file(sell, f"{username}_sell.txt")
            append_to_file(time, f"{username}_time.txt")
            print("-----Insertion Successful-----")
            log_audit(username, "Insert product", f"Product: {prod}")
        else:
            print("Action aborted.")

    def update(self, username: str):
        clear()
        self.product_name = read_file_lines(f"{username}_product.txt")
        self.quantity = read_file_lines(f"{username}_quantity.txt")
        self.buy_price = read_file_lines(f"{username}_buy.txt")
        self.sell_price = read_file_lines(f"{username}_sell.txt")
        self.last_updated = read_file_lines(f"{username}_time.txt")

        prod_u = input("Enter the product name to update: \n")
        consent = input("Do you consent to this update? (Yes/No): \n")

        if consent.lower() == "yes":
            log_consent(username, "Update product")
            found = False
            for i in range(len(self.product_name)):
                if self.product_name[i] == prod_u:
                    found = True
                    self.product_name[i] = input("Enter new product name: ")
                    self.quantity[i] = input("Enter new quantity: ")
                    self.buy_price[i] = input("Enter new buying price: ")
                    self.sell_price[i] = input("Enter new selling price: ")
                    self.last_updated[i] = get_current_date()

                    # Update all files
                    for filename, data in [
                        (f"{username}_product.txt", self.product_name),
                        (f"{username}_quantity.txt", self.quantity),
                        (f"{username}_buy.txt", self.buy_price),
                        (f"{username}_sell.txt", self.sell_price),
                        (f"{username}_time.txt", self.last_updated)
                    ]:
                        with open(filename, 'w') as f:
                            for item in data:
                                if item:
                                    f.write(f"{item}\n")

                    log_audit(username, "Update product", f"Product: {prod_u}")
                    print("-----Update Successful-----")
                    break

            if not found:
                print("Product not found!")

    def delete_db(self, username: str):
        clear()
        self.product_name = read_file_lines(f"{username}_product.txt")
        self.quantity = read_file_lines(f"{username}_quantity.txt")
        self.buy_price = read_file_lines(f"{username}_buy.txt")
        self.sell_price = read_file_lines(f"{username}_sell.txt")
        self.last_updated = read_file_lines(f"{username}_time.txt")

        prod_d = input("Enter the product name to delete: \n")
        consent = input("Do you consent to this deletion? (Yes/No): \n")

        if consent.lower() == "yes":
            log_consent(username, "Delete product")
            found = False
            for i in range(len(self.product_name)):
                if self.product_name[i] == prod_d:
                    found = True
                    # Shift all items up
                    for j in range(i, len(self.product_name)-1):
                        self.product_name[j] = self.product_name[j+1]
                        self.quantity[j] = self.quantity[j+1]
                        self.buy_price[j] = self.buy_price[j+1]
                        self.sell_price[j] = self.sell_price[j+1]
                        self.last_updated[j] = self.last_updated[j+1]

                    # Clear last item
                    self.product_name[-1] = ""
                    self.quantity[-1] = ""
                    self.buy_price[-1] = ""
                    self.sell_price[-1] = ""
                    self.last_updated[-1] = ""

                    # Update all files
                    for filename, data in [
                        (f"{username}_product.txt", self.product_name),
                        (f"{username}_quantity.txt", self.quantity),
                        (f"{username}_buy.txt", self.buy_price),
                        (f"{username}_sell.txt", self.sell_price),
                        (f"{username}_time.txt", self.last_updated)
                    ]:
                        with open(filename, 'w') as f:
                            for item in data:
                                if item:
                                    f.write(f"{item}\n")

                    log_audit(username, "Delete product", f"Product: {prod_d}")
                    print("-----Deletion Successful-----")
                    break

            if not found:
                print("Product not found!")

class Privacy:
    def register_user(self):
        clear()
        print("-----Enter User Details-----")
        username = input("Enter your username: \n")
        password = masked_input("Enter your password: \n")
        role = input("Enter your purpose on the application (Admin, Special, User): \n")

        if role.lower() == "admin":
            while True:
                admin_key = input("Enter the administration key: \n")
                append_hash(hash_string(admin_key), "admin_key.txt")
                print("-----Admin Registration Successful-----")
                create_files(username)
                append_to_file(username, "admin.txt")
                append_hash(hash_string(password), "password1.txt")
                break

        elif role.lower() == "special":
            while True:
                special_otp = input("Enter the special user's OTP: \n")
                if OTP == special_otp:
                    print("-----Special User Registration Successful-----")
                    append_to_file(username, "special.txt")
                    append_hash(hash_string(password), "password2.txt")
                    break
                else:
                    print("Incorrect Password")
                    ans = input("Would you like to retry entering (Yes or No): \n")
                    if ans.lower() != "yes":
                        return

        elif role.lower() == "user":
            print("-----User Registration Successful-----")
            append_to_file(username, "user.txt")
            append_hash(hash_string(password), "password3.txt")

    def admin(self, name: str):
        db = Database()
        while True:
            clear()
            print(f"-----Welcome back {name} !-----\n")
            print("1) View data on system.")
            print("2) Insert data on system.")
            print("3) Update data on system.")
            print("4) Delete data on system.")
            print("5) Exit the system.\n")

            choice = input("Enter option number: \n")
            
            if choice == "1":
                db.view(name)
            elif choice == "2":
                db.insert(name)
            elif choice == "3":
                db.update(name)
            elif choice == "4":
                db.delete_db(name)
            elif choice == "5":
                print("Exiting........")
                clear()
                exit(0)
            else:
                print("Incorrect Input! Try Again")

    def special(self, name: str, admin: str):
        db = Database()
        while True:
            clear()
            print(f"-----Welcome back {name} !-----\n")
            print("1) View data on system.")
            print("2) Insert data on system.")
            print("3) Exit the system.\n")

            choice = input("Enter option number: \n")
            
            if choice == "1":
                db.view(admin)
            elif choice == "2":
                db.insert(admin)
            elif choice == "3":
                print("Exiting........")
                clear()
                exit(0)
            else:
                print("Incorrect Input! Try Again")

    def user(self, name: str, admin: str):
        db = Database()
        while True:
            clear()
            print(f"-----Welcome back {name} !-----\n")
            print("1) View data on system.")
            print("2) Exit the system.\n")

            choice = input("Enter option number: \n")
            
            if choice == "1":
                db.view(admin)
            elif choice == "2":
                print("Exiting........")
                clear()
                exit(0)
            else:
                print("Incorrect Input! Try Again")

def main_ui():
    while True:
        clear()
        print("     Welcome To Digital Database     ")
        print("   Your solution to day to day problems   \n\n\n")
        print("1) Register New User.")
        print("2) Login.\n\n")
        
        ans = input("Enter option number: \n")
        privacy = Privacy()

        if ans == "1":
            privacy.register_user()
        elif ans == "2":
            clear()
            name = input("Enter username: \n")
            password = masked_input("Enter password: \n")

            names1 = read_file_lines("admin.txt")
            passes1 = read_file_hashes("password1.txt")
            
            if name in names1 and hash_string(password) in passes1:
                print("-----Authentication Complete-----")
                privacy.admin(name)
                continue

            names2 = read_file_lines("special.txt")
            passes2 = read_file_hashes("password2.txt")
            
            if name in names2 and hash_string(password) in passes2:
                print("-----Authentication Complete-----")
                admin = input("Enter name of admin to log into admin's database: \n")
                admin_key = masked_input("Enter admin key to log into admin's database: \n")
                keys = read_file_hashes("admin_key.txt")
                
                if hash_string(admin_key) in keys:
                    privacy.special(name, admin)
                continue

            names3 = read_file_lines("user.txt")
            passes3 = read_file_hashes("password3.txt")
            
            if name in names3 and hash_string(password) in passes3:
                print("-----Authentication Complete-----")
                admin = input("Enter name of admin to log into admin's database: \n")
                admin_key = masked_input("Enter admin key to log into admin's database: \n")
                keys = read_file_hashes("admin_key.txt")
                
                if hash_string(admin_key) in keys:
                    privacy.user(name, admin)
                else:
                    print("Incorrect Password or Admin Key")
                continue
            
            print("-----User Not Found-----")
        else:
            print("Incorrect Input! Try Again")

if __name__ == "__main__":
    print("Group Members:--")
    print("1) jahanzeb Khairi (22K-4746)")
    print("2) Syed Murtaza Rizvi (22K-4754)")
    print("3) M. Yahya Khan (22K-4690)")
    main_ui()