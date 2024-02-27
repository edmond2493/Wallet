from tkinter import *
from Admin import Admin
from Widgets import Widgets
from PIL import Image, ImageTk
from tkinter import messagebox


class User:
    def __init__(self, role, username, master):

        def logout():
            ask = messagebox.askokcancel("Logout", "Are you sure you want to logout?")
            if ask:
                from Login import Login
                from Static import Static
                from Functions import Functions
                Functions.remember(username)
                Static.garbage_collect(self.f_main)
                self.f_main.grid_remove()
                Login(master)

        self.root = master
        self.root.title('Wallet')
        self.root.resizable(False, False)
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        app_w = 800
        app_h = 500
        self.root.geometry(f'{app_w}x{app_h}+{(screen_w // 2) - (app_w // 2)}+{(screen_h // 2) - (app_h // 2)}')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.iconbitmap('icons/tools/wallet.ico')

        # CHECK IF THE USER IS ADMIN OR NOT, THEN CHANGES THE SIZE OF THE APP ADDING A SIDE PANEL FOR THE ADMIN---------
        if role == 'admin':
            app_w = 1000
            Admin(self.root)

        for i in range(2):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)
        self.root.geometry(f'{app_w}x{app_h}+{(screen_w // 2) - (app_w // 2)}+{(screen_h // 2) - (app_h // 2)}')

        self.bg = '#404040'
        self.bg2 = '#606060'
        self.bg3 = '#40464D'
        self.fg = '#ffffff'
        # MAIN FRAME FOR THE USER WINDOW--------------------------------------------------------------------------------
        self.f_main = Frame(self.root, width=800, height=app_h)
        self.f_main.grid(row=0, column=1)

        # TOP FRAME FOR NAME AND THE WALLETS AND FRAME SEPARATOR WITH THE BOT FRAMES------------------------------------
        self.f_1 = Frame(self.f_main, width=800, height=75, bg=self.bg)  # frame for name and wallets
        self.f_1.grid(row=0, column=0, columnspan=3)
        self.f_1.rowconfigure(index=1, weight=1)
        self.f_1.grid_propagate(False)

        self.f_1A = Frame(self.f_1, bg=self.bg)  # frame for name
        self.f_1A.grid(row=0, column=0)
        self.f_1A.rowconfigure(index=1, weight=1)

        img_logout = ImageTk.PhotoImage(Image.open('icons/tools/logout.png').resize((20, 20)))
        btn_logout = Button(self.f_1A, image=img_logout, bg=self.bg, bd=0, command=logout, activebackground=self.bg,
                            cursor='hand2')
        btn_logout.grid(row=0, column=1, padx=10, pady=10)
        btn_logout.image = img_logout

        self.f_1B = Frame(self.f_1, bg=self.bg)  # frame for wallets
        self.f_1B.grid(row=0, column=1)
        self.f_1B.rowconfigure(index=1, weight=1)

        Frame(self.f_main, width=800, height=2, bd=10, relief='sunken').grid(row=1, column=0, columnspan=3)

        # BOT LEFT AND RIGHT FRAME THAT CONTAINS THE BALANCE AND EXCHANGE FRAMES, AND THE MOVEMENTS FRAME---------------
        self.f_2A = Frame(self.f_main, width=500, height=423)  # frame of the left bottom side
        self.f_2A.grid(row=2, column=0)
        self.f_2A.grid_propagate(False)
        Frame(self.f_main, height=423, width=2, bd=10, relief='sunken').grid(row=2, column=1)
        self.f_2B = Frame(self.f_main, height=423, width=298)  # frame for the right bottom side
        self.f_2B.grid(row=2, column=2)
        self.f_2B.grid_propagate(False)

        self.f_2C = Frame(self.f_main, width=500, height=423)  # frame for the chart pie view
        self.f_2C.grid(row=2, column=0)
        self.f_2C.grid_propagate(False)

        # BOT LEFT FRAME WHICH CONTAINS THE BALANCE FRAME---------------------------------------------------------------
        self.f_2A1 = Frame(self.f_2A, width=500, height=225)  # this is the balance frame
        self.f_2A1.grid(row=0, column=0)
        self.f_left = Frame(self.f_2A1, height=225, width=138, bg=self.bg2)  # this is the left side of balance
        self.f_left.grid_propagate(False)
        self.f_left.grid(row=0, column=0)
        Frame(self.f_2A1, width=2, bd=10, relief='sunken').grid(row=0, column=1)
        self.f_right = Frame(self.f_2A1, height=225, width=360, bg=self.bg2)  # this is the right side of balance
        self.f_right.grid_propagate(False)
        self.f_right.grid(row=0, column=2)

        Frame(self.f_2A, width=500, height=2, bd=10, relief='sunken').grid(row=1, column=0)

        # BOT LEFT FRAME WHICH CONTAINS THE EXCHANGE FRAME AND THE MOVEMENTS FRAME--------------------------------------
        self.f_2A2 = Frame(self.f_2A, width=500, height=196, bg=self.bg3)  # this is the exchange frame
        self.f_2A2.grid(row=2, column=0)
        self.f_2A2.grid_propagate(False)
        self.f_2A3 = Frame(self.f_2A, width=500, height=196, bg=self.bg2)  # this is the add, edit movements frame
        self.f_2A3.grid(row=2, column=0)
        self.f_2A3.grid_propagate(False)
        self.f_2A4 = Frame(self.f_2A, width=500, height=196, bg=self.bg)  # this is the select icon for movement frame
        self.f_2A4.grid(row=2, column=0)
        self.f_2A4.grid_propagate(False)
        self.f_2A5 = Frame(self.f_2A, width=500, height=196, bg=self.bg2)  # this is the create new category frame
        self.f_2A5.grid(row=2, column=0)
        self.f_2A5.grid_propagate(False)
        self.f_2A6 = Frame(self.f_2A, width=500, height=196, bg=self.bg2)  # this is the show all category frame
        self.f_2A6.grid(row=2, column=0)
        self.f_2A6.grid_propagate(False)
        self.f_2A7 = Frame(self.f_2A, width=500, height=196, bg=self.bg2)  # this is the add and edit wallet frame
        self.f_2A7.grid(row=2, column=0)
        self.f_2A7.grid_propagate(False)
        self.f_2A8 = Frame(self.f_2A, width=500, height=196, bg=self.bg2)  # this is the transfer between wallets frame
        self.f_2A8.grid(row=2, column=0)
        self.f_2A8.grid_propagate(False)
        for i in range(6):
            self.f_2A8.rowconfigure(i, weight=1)
            self.f_2A8.columnconfigure(i, weight=1)

        # BOT RIGHT FRAME WHICH CONTAINS THE MOVEMENTS AND CATEGORY FRAME-----------------------------------------------
        self.f_2B1 = Frame(self.f_2B, width=298, height=55, bg=self.bg)  # this is the five widgets frame
        self.f_2B1.grid(row=0, column=0)
        self.f_2B1.grid_propagate(False)
        self.f_2B2 = Frame(self.f_2B, width=298, height=55, bg=self.bg)  # this is the search movements frame
        self.f_2B2.grid(row=0, column=0)
        self.f_2B2.grid_propagate(False)
        Frame(self.f_2B, width=298, height=2, bd=10, relief='sunken').grid(row=1, column=0)
        self.f_2B3 = Frame(self.f_2B, width=298, height=366, bg=self.bg)  # this is the category treeview
        self.f_2B3.grid(row=2, column=0)
        self.f_2B3.grid_propagate(False)
        self.f_2B4 = Frame(self.f_2B, width=298, height=366, bg=self.bg)  # this is the date treeview
        self.f_2B4.grid(row=2, column=0)
        self.f_2B4.grid_propagate(False)
        self.f_2B5 = Frame(self.f_2B, width=298, height=366, bg=self.bg)  # this is the search treeview
        self.f_2B5.grid(row=2, column=0)
        self.f_2B5.grid_propagate(False)

        # CHART FRAMES THAT CONTAINS THE MENU AND THE DONUT CHART-------------------------------------------------------
        self.f_2C1 = Frame(self.f_2C, width=500, height=57, bg=self.bg)  # this is the menu frame on the donut chart
        self.f_2C1.grid(row=0, column=0)
        self.f_2C1.grid_propagate(False)
        self.f_2C2 = Frame(self.f_2C, width=500, height=366, bg=self.bg)  # this is the donut chart frame
        self.f_2C2.grid(row=1, column=0)
        self.f_2C2.grid_propagate(False)
        for i in range(2):
            self.f_2C2.columnconfigure(i, weight=1)

        frames = [self.f_1, self.f_1A, self.f_1B, self.f_2A, self.f_2A1, self.f_left, self.f_right, self.f_2A2,
                  self.f_2A3, self.f_2A4, self.f_2A5, self.f_2A6, self.f_2A7, self.f_2A8, self.f_2B1, self.f_2B2,
                  self.f_2B3, self.f_2B4, self.f_2B5, self.f_2C, self.f_2C1, self.f_2C2]

        self.widgets = Widgets(role, username, frames)
        self.widgets.wallets_frame()
