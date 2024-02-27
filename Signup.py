from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import bcrypt
import re
from Static import Static


class Signup:
    def __init__(self, master, role):

        self.root = master
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        app_w = 350
        app_h = 250
        self.root.title('Signup')
        self.root.geometry(f'{app_w}x{app_h}+{(screen_w // 2) - (app_w // 2)}+{(screen_h // 2) - (app_h // 2)}')
        self.static = Static
        for i in range(6):
            self.root.rowconfigure(index=i, weight=1)
            self.root.columnconfigure(index=i, weight=1)
        self.bg = '#404040'
        self.bg2 = '#606060'
        self.fg = '#ffffff'
        self.font1 = ('Arial', 16, 'italic')
        self.font2 = ('Arial', 14)
        self.role = role

        self.f_signup = Frame(self.root, width=app_w, height=app_h, bg=self.bg)
        self.f_signup.grid(row=0, column=0)
        self.f_signup.grid_propagate(False)

        # NAME LABELFRAME AND ENTRY-------------------------------------------------------------------------------------
        self.lf_name = LabelFrame(self.f_signup, text='Name', font=self.font1, bg=self.bg, fg=self.fg)
        self.lf_name.grid(row=0, column=0, columnspan=3, padx=5, pady=10, sticky='ew')
        self.e_name = Entry(self.lf_name, font=self.font2, bg=self.bg2, fg=self.fg, width=12)
        self.e_name.pack(padx=5, pady=5)

        # SURNAME LABELFRAME AND ENTRY----------------------------------------------------------------------------------
        self.lf_surname = LabelFrame(self.f_signup, text='Surname', font=self.font1, bg=self.bg, fg=self.fg)
        self.lf_surname.grid(row=0, column=3, columnspan=3, padx=5, pady=10, sticky='ew')
        self.e_surname = Entry(self.lf_surname, font=self.font2, bg=self.bg2, fg=self.fg, width=12)
        self.e_surname.pack(padx=5, pady=5)

        # USERNAME LABELFRAME AND ENTRY---------------------------------------------------------------------------------
        self.lf_username = LabelFrame(self.f_signup, text='Username', font=self.font1, bg=self.bg, fg=self.fg)
        self.lf_username.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky='ew')
        self.e_username = Entry(self.lf_username, font=self.font2, bg=self.bg2, fg=self.fg, width=12)
        self.e_username.pack(padx=5, pady=5)

        # PASSWORD LABELFRAME AND ENTRY--------------------------------------------------------------------------------
        self.lf_password = LabelFrame(self.f_signup, text='Password', font=self.font1, bg=self.bg, fg=self.fg)
        self.lf_password.grid(row=1, column=3, columnspan=3, padx=5, pady=10, sticky='ew')
        self.e_password = Entry(self.lf_password, font=self.font2, bg=self.bg2, fg=self.fg, width=12, show='*')
        self.e_password.pack(padx=5, pady=5, side='left')

        # SHOW AND HIDE PASSWORD BUTTON AND IMAGES----------------------------------------------------------------------
        self.show_pass = ImageTk.PhotoImage(Image.open('icons/tools/pass_shown.png').resize((20, 20)))
        self.hide_pass = ImageTk.PhotoImage(Image.open('icons/tools/pass_hidden.png').resize((20, 20)))
        self.show_hide = Button(self.lf_password, image=self.hide_pass, bg=self.bg, bd=0, cursor='hand2')
        self.show_hide.config(command=self.password_view, activebackground=self.bg)
        self.show_hide.pack(side='right')

        # CONFIRM AND CANCEL BUTTONS WITH IMAGES FOR THE NEW SIGNUP-----------------------------------------------------
        self.confirm_img = ImageTk.PhotoImage(Image.open('icons/tools/signup_confirm.png').resize((100, 45)))
        self.bt_confirm = Button(self.f_signup, image=self.confirm_img, cursor="hand2", bg=self.bg, bd=0)
        self.bt_confirm.config(command=self.confirm, activebackground=self.bg)
        self.bt_confirm.grid(row=2, column=0, columnspan=3, sticky='ew')

        self.cancel_img = ImageTk.PhotoImage(Image.open('icons/tools/signup_cancel.png').resize((100, 45)))
        self.bt_cancel = Button(self.f_signup, image=self.cancel_img, cursor="hand2", bg=self.bg, bd=0)
        self.bt_cancel.config(command=self.cancel, activebackground=self.bg)
        self.bt_cancel.grid(row=2, column=3, columnspan=3, sticky='ew')
        self.remember_var = IntVar()
        self.remember = Checkbutton(self.f_signup, text='Remember me', font=('Arial', 12), bg=self.bg, onvalue=1,
                                    variable=self.remember_var, cursor='hand2', activebackground=self.bg)
        self.remember.grid(row=3, column=0, columnspan=2, padx=5, sticky='w')

    def password_view(self):
        if self.e_password.cget('show') == '*':
            self.e_password.configure(show='')
            self.show_hide.configure(image=self.show_pass)
        else:
            self.e_password.configure(show='*')
            self.show_hide.configure(image=self.hide_pass)

    def cancel(self):
        Static.garbage_collect(self.f_signup)
        self.f_signup.grid_remove()
        from Login import Login
        Login(self.root)

    def confirm(self):
        conn = sqlite3.connect("Wallet.db")
        cur = conn.cursor()
        name = self.e_name.get()
        surname = self.e_surname.get()
        username = self.e_username.get()
        password = self.e_password.get()

        # CHECK IF NAME AND SURNAME ARE NOT EMPTY-----------------------------------------------------------------------
        if not name or not surname:
            messagebox.showwarning("Warning", "Name and surname cannot be empty")
            return

        # CHECK USERNAME LENGTH-----------------------------------------------------------------------------------------
        if not (4 <= len(username) <= 30):
            messagebox.showwarning("Warning", "Username must be between 4 and 30 characters")
            return

        # CHECK PASSWORD REQUIREMENTS-----------------------------------------------------------------------------------
        if not (6 <= len(password) <= 20) or not re.search("[a-zA-Z]", password) or \
           not re.search("[A-Z]", password) or not re.search("[0-9]", password):
            messagebox.showwarning("Warning", "Password must be between 6 and 20 characters and include at least one "
                                              "letter, one capital letter, and a number")
            return

        # CHECK IF USERNAME ALREADY EXISTS------------------------------------------------------------------------------
        cur.execute("SELECT * FROM account WHERE username=?", (username,))
        if cur.fetchone():
            messagebox.showwarning("Warning", "Username already taken")
            return

        # HASH THE PASSWORD---------------------------------------------------------------------------------------------
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # INSERT THE NEW USER-------------------------------------------------------------------------------------------
        try:
            cur.execute("INSERT INTO account (name, surname, username, password, role, remember) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (name, surname, username, hashed_password.decode('utf-8'), self.role, self.remember_var.get()))
            conn.commit()
            Static.garbage_collect(self.f_signup)
            self.f_signup.grid_remove()
            from User import User
            User('user', username, self.root)
        except Exception as e:
            messagebox.showwarning("Warning", f"Error: {e}")
        finally:
            conn.close()
