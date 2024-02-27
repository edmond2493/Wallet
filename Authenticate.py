import sqlite3
import bcrypt


def validate_login(username, password):
    conn = sqlite3.connect("Wallet.db")
    cur = conn.cursor()
    cur.execute("SELECT password, role FROM account WHERE username=?", (username,))
    user_data = cur.fetchone()

    if user_data:
        hashed_password, role = user_data
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            conn.close()
            return role
        else:
            conn.close()
            return 'invalid password'
    else:
        return 'user not found'
