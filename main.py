import sqlite3
from tkinter import *


def main():
    conn = sqlite3.connect('Wallet.db')
    cursor = conn.cursor()

    # Create the 'account' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS account (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                name TEXT,
                surname TEXT,
                role TEXT,
                remember TEXT)''')

    # Create the 'categories' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                user TEXT NOT NULL,
                category TEXT NOT NULL,
                type TEXT,
                icon TEXT,
                FOREIGN KEY(user) REFERENCES account(username))''')

    # Create the 'wallet' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallet (
                user TEXT NOT NULL,
                wallet_name TEXT NOT NULL,
                sum REAL,
                coin TEXT,
                start_sum REAL,
                start_date TEXT,
                icon TEXT,
                FOREIGN KEY(user) REFERENCES account(username))''')

    # Create the 'movements' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS movements (
                user TEXT NOT NULL,
                wallet TEXT NOT NULL,
                category TEXT NOT NULL,
                sum REAL NOT NULL,
                date TEXT NOT NULL,
                note TEXT,
                type TEXT NOT NULL,
                FOREIGN KEY(user) REFERENCES account(username),
                FOREIGN KEY(wallet) REFERENCES wallet(wallet_name),
                FOREIGN KEY(category) REFERENCES categories(category))''')

    root = Tk()
    from Login import Login
    from User import User
    remember = cursor.execute("SELECT username, role FROM account WHERE remember = 1").fetchone()
    if remember:
        User(role=remember[1], username=remember[0], master=root)
    else:
        Login(master=root)
    conn.commit()
    conn.close()
    root.mainloop()


if __name__ == "__main__":
    main()
