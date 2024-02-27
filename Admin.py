from tkinter import *
from PIL import Image, ImageTk


class Admin:
    def __init__(self, master):
        self.root = master
        self.f_admin = Frame(self.root, width=200, height=500)
        self.f_admin.grid(row=0, column=0)
        self.f_admin.grid_propagate(False)
        for i in range(2):
            self.f_admin.rowconfigure(i, weight=1)
            self.f_admin.columnconfigure(i, weight=1)
        # TOP PANEL OF ADMIN WITH NAME, LOGOUT AND SEARCH ENTRY-----------------------------------------------------
        self.f_a_top = Frame(self.f_admin, height=75, width=200, bg='#5e7a6d')
        self.f_a_top.grid(row=0, column=0)
        self.f_a_top.grid_propagate(False)

        self.l_a_name = Label(self.f_a_top, text='Edmond C', font=('Arial', 16), bg='#5e7a6d')
        self.l_a_name.grid(row=0, column=0, padx=15, pady=5)

        logout_img = ImageTk.PhotoImage(Image.open('icons/tools/logout.png').resize((20, 20)))
        self.bt_a_logout = Button(self.f_a_top, image=logout_img, cursor="hand2", bg='#5e7a6d', bd=0)
        self.bt_a_logout.image = logout_img
        self.bt_a_logout.grid(row=0, column=1)

        self.e_a_search = Entry(self.f_a_top, bg='#80a594', font=('Arial', 14), width=12)
        self.e_a_search.grid(row=1, column=0, columnspan=2, padx=32)

        # BOT PANEL OF ADMIN THAT SHOWS ALL THE USERS, WITH ADMINS ON TOP-------------------------------------------
        self.f_a_bot = Frame(self.f_admin, height=425, width=200, bg='#80a594')
        self.f_a_bot.grid(row=1, column=0)
