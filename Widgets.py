from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import date, datetime
from Functions import Functions
from Static import Static
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import threading
import numpy as np
import uuid

coins = ["ALL", "EUR", "USD", "GBP", "CHF", "AUD", "BRL", "CAD", "CNY", "INR", "JPY", "KRW", "MXN", "NOK", "NZD",
         "RUB", "SEK", "SGD", "ZAR"]


class Widgets:
    def __init__(self, role, username, frames):
        self.bg = '#404040'
        self.bg2 = '#606060'
        self.bg3 = '#40464D'
        self.fg = '#ffffff'
        self.status = {'admin': 'disabled', 'user': 'active'}  # disables buttons if the user is admin
        self.exp_type = {'income': '+', 'expense': '-'}
        self.exp_type2 = {'+': 'income', '-': 'expense'}
        # list of frames
        self.f_1 = frames[0]
        self.f_1A = frames[1]
        self.f_1B = frames[2]
        self.f_2A = frames[3]
        self.f_2A1 = frames[4]
        self.f_left = frames[5]
        self.f_right = frames[6]
        self.f_2A2 = frames[7]
        self.f_2A3 = frames[8]
        self.f_2A4 = frames[9]
        self.f_2A5 = frames[10]
        self.f_2A6 = frames[11]
        self.f_2A7 = frames[12]
        self.f_2A8 = frames[13]
        self.f_2B1 = frames[14]
        self.f_2B2 = frames[15]
        self.f_2B3 = frames[16]
        self.f_2B4 = frames[17]
        self.f_2B5 = frames[18]
        self.f_2C = frames[19]
        self.f_2C1 = frames[20]
        self.f_2C2 = frames[21]
        # current username and the role of the user
        self.username = username
        self.role = role

        self.settings_toggle = True  # toggle for the settings in the balance frame
        self.c_toggle = True  # toggle to switch between the category and date treeview
        self.pie_toggle = False  # toggle to switch between the wallet charts

        self.wallet = ''  # current wallet name
        self.walled_oid = None  # current wallet oid

        self.update_list = []  # list that stores the widgets to be updated from balance and transfer frame
        self.settings_list = []  # list that stores the widgets for the settings to toggle off and on

        self.functions = Functions(self.username)  # call the functions that handle the SQL queries
        self.static = Static()  # static functions
        self.name_surname_frame()
        self.tree_menu_frame()

    # FUNCTION THAT CREATES THE NAME AND SURNAME LABEL OF THE USER self.f_1A--------------------------------------------
    def name_surname_frame(self):
        user = self.functions.name_surname()
        l_name = Label(self.f_1A, text=f'{user[0]} {user[1]}', font=('Arial', 20), bg=self.bg, fg=self.fg)
        l_name.grid(row=0, column=0, rowspan=2, padx=10, pady=20)

        # ADD NEW WALLET BUTTON, IS DISABLED IF THE WALLET NUMBER IS 10 OR THE USER IS ADMIN----------------------------
        im_wallet = ImageTk.PhotoImage(Image.open('icons/tools/add_new.png').resize((40, 40)))
        bt_wallet = Button(self.f_1, image=im_wallet, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
        bt_wallet.config(command=lambda: self.add_edit_wallet('INSERT'), state=self.status[self.role])
        bt_wallet.image = im_wallet
        bt_wallet.grid(row=0, column=2, rowspan=2)
        if len(self.functions.retrieve_wallets()) >= 10:
            bt_wallet.config(state='disabled')

    # FUNCTION THAT CREATES THE WALLETS BUTTONS WITH THE COMMANDS TO SWITCH BETWEEN self.f_1B---------------------------
    def wallets_frame(self):

        self.static.garbage_collect(self.f_1B)
        self.f_2A.lift()
        column = 0
        wallets = self.functions.retrieve_wallets()
        for wallet in wallets:
            font = self.static.calculate_font_size(wallet[1], base_size=14, min_size=8)
            photo = ImageTk.PhotoImage(Image.open(wallet[6]).resize((38, 38)))
            btn = Button(self.f_1B, image=photo, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2', fg=self.fg,
                         text=wallet[1], compound='top', font=('arial', font), activeforeground=self.fg)
            btn.image = photo
            btn.grid(row=0, column=column, padx=7, pady=(6, 0))
            btn.config(command=lambda n=wallet[1], p=wallet[7]: self.call_wallet(n, p))
            column += 1
        wallets = self.functions.retrieve_wallets()
        if wallets:
            self.wallet = wallets[0][1]
            self.update_list.clear()
            self.settings_list.clear()
            self.right_balance_frame()
            self.left_balance_frame()
            self.exchange_frame()
            self.call_wallet(self.wallet, wallets[0][7])

    # FUNCTION TO SWITCH TO THE SELECTED WALLET-------------------------------------------------------------------------
    def call_wallet(self, w_name, w_oid):
        self.wallet = w_name
        self.walled_oid = w_oid
        self.tree_toggle()  # function to show the treeview that is already in view
        self.left_balance_update()  # function to update the wallet icon and name in the transfer frame
        self.right_balance_update()  # function to update the wallet total in the balance frame
        self.update_exchange()  # function to update the exchange frame
        self.settings_toggle = False  # disable the settings toggle and then calls the wallet settings
        self.wallet_settings()  # it serves to close the wallet setting when switching between wallets
        self.f_2A2.lift()  # lifts the exchange frame
        self.f_2A.lift()  # lifts the main self.f_2A frame

    # FUNCTION TO CREATE AND EDIT WALLETS FOR THE USER self.f_2A7-------------------------------------------------------
    def add_edit_wallet(self, action, edit=None):

        def collect_data():
            name = e_name.get().capitalize()
            start_sum = e_start_sum.get().replace(',', '.').strip()
            if not start_sum:  # Check if start_sum is empty
                start_sum = '0'
            coin = sv_coin.get()
            date_str = bt_calendar.cget('text')
            date_ob = datetime.strptime(date_str, "%d-%m-%Y")
            f_date = date_ob.strftime("%Y-%m-%d")
            icon = btn.cget('text')
            if name == '':
                messagebox.showerror("Error", "Please enter a name", parent=self.f_2A2)
                return

            elif len(name) < 3 or len(name) > 12:
                messagebox.showerror("Error", "Name must be between 3 and 12 characters", parent=self.f_2A2)
                return

            elif self.functions.wallet_exist(name) and (edit is None or edit[1].lower() != name.lower()):
                messagebox.showerror('Error', 'Name already exists', parent=self.f_2A5)
                return

            if ' ' in start_sum:
                messagebox.showerror("Error", "Input should not contain spaces.", parent=self.f_2A2)
                return
            try:
                start_sum = float(start_sum)
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a number.", parent=self.f_2A2)
                return

            if icon == '':
                messagebox.showerror("Error", "Select a category", parent=self.f_2A2)
                return

            p = f'icons/wallet/{icon}.png'
            if action == 'INSERT':
                self.functions.create_update_wallet(action, name, start_sum, coin, f_date, p)
            else:
                self.functions.create_update_wallet(action, name, start_sum, coin, f_date, p, edit[7], self.wallet)

            self.wallets_frame()
            self.settings_toggle = True

        self.static.garbage_collect(self.f_2A7)
        for i in range(6):
            self.f_2A7.grid_rowconfigure(i, weight=1)
            self.f_2A7.grid_columnconfigure(i, weight=1)
        lf_name = LabelFrame(self.f_2A7, text='Name', bg=self.bg2, fg=self.fg, font=('Arial', 18, 'italic'))
        lf_name.grid(row=0, column=0, columnspan=3, rowspan=3, sticky='nsew', pady=(10, 5))
        e_name = Entry(lf_name, bg=self.bg, fg=self.fg, font=('Arial', 17), width=12)
        e_name.pack(pady=10, padx=20)

        lf_start_sum = LabelFrame(self.f_2A7, text='Start sum', bg=self.bg2, fg=self.fg, font=('Arial', 18, 'italic'))
        lf_start_sum.grid(row=3, column=0, columnspan=3, rowspan=3, sticky='nsew', pady=10)
        e_start_sum = Entry(lf_start_sum, bg=self.bg, fg=self.fg, font=('Arial', 17), width=10)
        e_start_sum.grid(row=0, column=0, padx=10)

        style = ttk.Style()
        style.configure('OM.TButton')
        sv_coin = StringVar()
        om_coin = ttk.OptionMenu(lf_start_sum, sv_coin, 'ALL', *coins, style='OM.TButton')
        om_coin.config(width=7)
        om_coin.grid(row=0, column=1)
        # om_coin["menu"].configure(bg=self.bg, fg=self.fg)

        def on_enter(event):
            event.widget["cursor"] = "hand2"

        def on_leave(event):
            event.widget["cursor"] = ""

        om_coin.bind("<Enter>", on_enter)
        om_coin.bind("<Leave>", on_leave)

        current_date = date.today().strftime("%d-%m-%Y")
        img_calendar = ImageTk.PhotoImage(Image.open('icons/tools/calendar.png').resize((25, 25)))
        bt_calendar = Button(self.f_2A7, text=current_date, image=img_calendar, compound="right", bg=self.bg2,
                             command=lambda: self.static.grab_date(self.f_2A3, bt_calendar),
                             font=('Arial', 18), fg=self.fg, cursor='hand2', activebackground=self.bg2, border=0)
        bt_calendar.image = img_calendar
        bt_calendar.grid(row=0, column=3, columnspan=3, rowspan=1, padx=30)

        img = ImageTk.PhotoImage(Image.open('icons/tools/choose_category.png').resize((90, 90)))
        btn = Button(self.f_2A7, image=img, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        btn.config(command=lambda: self.category_icon('wallet', btn, self.f_2A7, 90, 90))
        btn.image = img
        btn.grid(row=1, column=3, columnspan=3, rowspan=4)

        img_confirm = ImageTk.PhotoImage(Image.open('icons/tools/action_confirm.png').resize((20, 20)))
        bt_confirm = Button(self.f_2A7, image=img_confirm, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        bt_confirm.config(command=collect_data, state=self.status[self.role])
        bt_confirm.image = img_confirm
        bt_confirm.grid(row=5, column=4, columnspan=1)

        img_cancel = ImageTk.PhotoImage(Image.open('icons/tools/action_cancel.png').resize((20, 20)))
        bt_cancel = Button(self.f_2A7, image=img_cancel, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        bt_cancel.config(command=self.f_2A2.lift)
        bt_cancel.image = img_cancel
        bt_cancel.grid(row=5, column=5, columnspan=1)

        if edit is not None:
            edit = self.functions.edit_wallet(self.wallet)
            path = edit[6].replace("icons/wallet/", "").rstrip(".png")
            e_name.insert(0, edit[1])
            e_start_sum.insert(0, edit[4])
            date_obj = datetime.strptime(edit[5], '%Y-%m-%d')
            new_date = date_obj.strftime('%d-%m-%Y')
            bt_calendar.config(text=new_date)
            img = ImageTk.PhotoImage(Image.open(edit[6]).resize((80, 80)))
            btn.config(text=path, image=img)
            btn.image = img
            # bt_cancel.config(command=lambda: self.f_2A2.lift())

        self.f_2A7.lift()
        self.f_2A.lift()

    # FUNCTIONS THAT CREATES THE WIDGETS IN THE TRANSFER FRAME self.f_left----------------------------------------------
    def left_balance_frame(self):
        self.static.garbage_collect(self.f_left)
        for i in range(3):
            self.f_left.rowconfigure(i, weight=1)
        data = self.functions.update_balance(self.wallet)
        img_wallet = ImageTk.PhotoImage(Image.open(data[6]).resize((80, 80)))
        bt_wallet = Button(self.f_left, image=img_wallet, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        bt_wallet.image = img_wallet
        bt_wallet.grid(row=0, column=0, padx=25, pady=(10, 5))

        font = self.static.calculate_font_size(data[1], base_size=16, min_size=12)
        l_wallet_name = Label(self.f_left, text=data[1], font=('Arial', font), bg=self.bg2, fg=self.fg)
        l_wallet_name.grid(row=1, column=0, pady=5)

        img_transfer = ImageTk.PhotoImage(Image.open('icons/tools/transfer.png').resize((50, 50)))
        bt_transfer = Button(self.f_left, image=img_transfer, bg=self.bg2, bd=0, activebackground=self.bg2,
                             cursor='hand2')
        bt_transfer.config(state=self.status[self.role], command=lambda: self.transfer_frame('INSERT'))
        bt_transfer.image = img_transfer
        bt_transfer.grid(row=3, column=0, pady=10)

        self.update_list.append(bt_wallet)
        self.update_list.append(l_wallet_name)

    # FUNCTION TO UPDATE THE LEFT BALANCE WIDGETS-----------------------------------------------------------------------
    def left_balance_update(self):
        data = self.functions.update_balance(self.wallet)
        new_img = ImageTk.PhotoImage(Image.open(data[6]).resize((80, 80)))
        self.update_list[1].config(image=new_img)  # wallet icon from the transfer_frame
        self.update_list[1].image = new_img
        font = self.static.calculate_font_size(data[1], base_size=16, min_size=12)
        self.update_list[2].config(text=data[1], font=('Arial', font))  # l_wallet_name from the transfer_frame

    # FUNCTION THAT CREATES THE BALANCE FRAME WIDGETS self.right--------------------------------------------------------
    def right_balance_frame(self):
        self.static.garbage_collect(self.f_right)
        for i in range(6):
            self.f_right.rowconfigure(i, weight=1)
            self.f_right.columnconfigure(i, weight=1)
        data = self.functions.update_balance(self.wallet)
        # SETTINGS BUTTON FOR CHART, EDIT AND DELETE WALLET-------------------------------------------------------------
        img_setting = ImageTk.PhotoImage(Image.open('icons/tools/settings.png').resize((30, 30)))
        bt_setting = Button(self.f_right, image=img_setting, bg=self.bg2, bd=0, activebackground=self.bg2,
                            cursor='hand2')
        bt_setting.config(command=self.wallet_settings)
        bt_setting.image = img_setting
        bt_setting.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='w', padx=5)

        img_chart = ImageTk.PhotoImage(Image.open('icons/tools/donut_chart.png').resize((20, 20)))
        bt_chart = Button(self.f_right, image=img_chart, bg=self.bg2, bd=0, activebackground=self.bg2,
                          cursor='hand2')
        bt_chart.config(command=self.chart_frame)
        bt_chart.image = img_chart

        img_edit = ImageTk.PhotoImage(Image.open('icons/tools/edit.png').resize((20, 20)))
        bt_edit = Button(self.f_right, image=img_edit, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        bt_edit.image = img_edit
        bt_edit.config(state=self.status[self.role], command=lambda: self.add_edit_wallet('UPDATE', True))

        img_delete = ImageTk.PhotoImage(Image.open('icons/tools/delete.png').resize((20, 20)))
        bt_delete = Button(self.f_right, image=img_delete, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        bt_delete.config(command=self.delete_wallet, state=self.status[self.role])
        bt_delete.image = img_delete
        self.settings_list.append(bt_chart)
        self.settings_list.append(bt_edit)
        self.settings_list.append(bt_delete)

        # BALANCE LABEL TO SHOW THE TOTAL OF THE WALLET-----------------------------------------------------------------
        l_balance = Label(self.f_right, text=f'Balance:', bg=self.bg2, fg=self.fg, font=('Arial', 22))
        l_balance.grid(row=2, column=0, columnspan=6)

        total = "{:.2f}".format(float(data[2]))
        l_total = Label(self.f_right, text=f'{total} {data[3]}', width=30, bg=self.bg2, fg=self.fg,
                        font=('Arial', 16))
        l_total.grid(row=3, column=0, columnspan=6)
        self.update_list.append(l_total)

        # ADD AND REMOVE BUTTONS FOR THE WALLET-------------------------------------------------------------------------
        img_add = ImageTk.PhotoImage(Image.open('icons/tools/add_income.png').resize((80, 80)))
        bt_add = Button(self.f_right, image=img_add, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        bt_add.config(state=self.status[self.role], command=lambda: (self.movement_frame('+', 'INSERT'),
                                                                     self.f_2A3.lift()))
        bt_add.image = img_add
        bt_add.grid(row=4, column=0, rowspan=2, columnspan=3)

        img_remove = ImageTk.PhotoImage(Image.open('icons/tools/add_expense.png').resize((80, 80)))
        bt_remove = Button(self.f_right, image=img_remove, bg=self.bg2, bd=0, activebackground=self.bg2,
                           cursor='hand2')
        bt_remove.config(state=self.status[self.role], command=lambda: (self.movement_frame('-', 'INSERT'),
                                                                        self.f_2A3.lift()))
        bt_remove.image = img_remove
        bt_remove.grid(row=4, column=3, rowspan=2, columnspan=3)

    # FUNCTION TO UPDATE THE RIGHT BALANCE LABEL------------------------------------------------------------------------
    def right_balance_update(self):
        data = self.functions.update_balance(self.wallet)
        total = "{:.2f}".format(float(data[2]))
        self.update_list[0].config(text=f'{total} {data[3]}')  # l_total from the balance_frame

    # FUNCTIONS THAT CREATES THE WIDGETS IN THE INSERT TRANSFER FRAME self.f_2A8----------------------------------------
    def transfer_frame(self, action, edit=None):

        def confirm_transfer():
            amount = self.static.validate_input_number(e_sum, self.f_2A2)
            if amount is None:
                return

            date_str = bt_calendar.cget('text')
            date_ob = datetime.strptime(date_str, "%d-%m-%Y")
            c_date = date_ob.strftime("%Y-%m-%d")
            wallet_1 = bt_1.cget('text')
            wallet_2 = bt_2.cget('text')
            if wallet_2 == 'Choose':
                messagebox.showerror("Error", "Select a wallet", parent=self.f_2A8)
                return
            transfer_id = str(f'UUID-{uuid.uuid4()}')
            oid1, oid2 = None, None
            if edit is not None:
                transfer_id = edit
                oid1, oid2 = bt_confirm.cget('text').split()
            data_1 = [self.username, wallet_1, f"TO-{wallet_2}", amount, c_date, transfer_id, "expense"]
            data_2 = [self.username, wallet_2, f"FROM-{wallet_1}", amount, c_date, transfer_id, "income"]
            self.functions.transfer(action, data_1, oid1)
            self.functions.transfer(action, data_2, oid2)

            self.right_balance_update()
            self.tree_toggle()
            self.update_exchange()
            self.f_2A2.lift()

        def delete_transfer():
            ask = messagebox.askyesno("Confirm", "Are you sure you want to delete this transfer?",
                                      parent=self.f_2A8)
            if ask:
                self.functions.delete_transfer(edit)
                self.right_balance_update()
                self.tree_toggle()
                self.update_exchange()
                self.f_2A2.lift()
            else:
                pass
            self.f_2A2.lift()

        self.static.garbage_collect(self.f_2A8)

        # THE CALENDAR WIDGET AND THE DELETE BUTTON THAT APPEARS WHEN EDITING AN EXISTING TRANSACTION-------------------
        current_date = date.today().strftime("%d-%m-%Y")
        img_calendar = ImageTk.PhotoImage(Image.open('icons/tools/calendar.png').resize((25, 25)))
        bt_calendar = Button(self.f_2A8, text=current_date, image=img_calendar, compound="right", bg=self.bg2,
                             command=lambda: self.static.grab_date(self.f_2A8, bt_calendar),
                             font=('Arial', 18), fg=self.fg, cursor='hand2', activebackground=self.bg2, border=0)
        bt_calendar.image = img_calendar
        bt_calendar.grid(row=0, column=0, columnspan=6, pady=(10, 0))

        img_delete = ImageTk.PhotoImage(Image.open('icons/tools/delete.png').resize((25, 25)))
        bt_delete = Button(self.f_2A8, image=img_delete, bg=self.bg2, bd=0, activebackground=self.bg2,
                           cursor='hand2')
        bt_delete.image = img_delete
        bt_delete.config(command=delete_transfer)

        # THE ARROW ICON THAT INDICATES THE TRANSFER BETWEEN THE TWO WALLETS--------------------------------------------
        img_arrow = ImageTk.PhotoImage(Image.open('icons/tools/transfer_arrow.png').resize((220, 25)))
        l_arrow = Label(self.f_2A8, image=img_arrow, bg=self.bg2)
        l_arrow.image = img_arrow
        l_arrow.grid(row=2, column=0, columnspan=6, padx=(10, 0))

        # LEFT BUTTON THAT SHOWS THE WALLET FROM WHICH THE TRANSFER WILL BE DONE----------------------------------------
        data = self.functions.update_balance(self.wallet)
        img_1 = ImageTk.PhotoImage(Image.open(data[6]).resize((90, 90)))
        bt_1 = Button(self.f_2A8, text=data[1], image=img_1, bg=self.bg2, bd=0, activebackground=self.bg2,
                      fg=self.fg,
                      cursor='hand2', compound='top', font=('Arial', 16))
        bt_1.image = img_1

        bt_1.grid(row=2, column=0, rowspan=4, columnspan=1, padx=(20, 0))

        # ENTRY TO INSERT THE SUM TO BE TRANSFERRED AND THE COIN USED --------------------------------------------------
        e_sum = Entry(self.f_2A8, font=('Arial', 20), bg=self.bg, fg=self.fg, width=9)
        e_sum.grid(row=3, column=0, rowspan=2, columnspan=6, padx=(0, 25))
        l_coin = Label(self.f_2A8, text=data[3], font=('Arial', 16, 'italic'), bg=self.bg, fg=self.fg)
        l_coin.grid(row=3, column=1, rowspan=2, columnspan=5, padx=(25, 0))

        # CONFIRM AND CANCEL BUTTON FOR THE TRANSACTION-----------------------------------------------------------------
        img_confirm = ImageTk.PhotoImage(Image.open('icons/tools/action_confirm.png').resize((25, 25)))
        bt_confirm = Button(self.f_2A8, image=img_confirm, bg=self.bg2, bd=0, activebackground=self.bg2,
                            cursor='hand2')
        bt_confirm.config(command=confirm_transfer)
        bt_confirm.image = img_confirm
        bt_confirm.grid(row=5, column=2, columnspan=1, padx=(0, 20))

        img_cancel = ImageTk.PhotoImage(Image.open('icons/tools/action_cancel.png').resize((25, 25)))
        bt_cancel = Button(self.f_2A8, image=img_cancel, bg=self.bg2, bd=0, activebackground=self.bg2,
                           cursor='hand2')
        bt_cancel.config(command=self.f_2A2.lift)
        bt_cancel.image = img_cancel
        bt_cancel.grid(row=5, column=3, columnspan=1, padx=(0, 20))

        # RIGHT BUTTON THAT SHOWS THE WALLET TO WHICH THE TRANSFER WILL BE DONE-----------------------------------------
        img_2 = ImageTk.PhotoImage(Image.open('icons/tools/choose_category.png').resize((90, 90)))
        bt_2 = Button(self.f_2A8, image=img_2, text='Choose', bg=self.bg2, bd=0, activebackground=self.bg2,
                      fg=self.fg,
                      cursor='hand2', compound='top', font=('Arial', 16))
        bt_2.image = img_2

        bt_2.grid(row=2, column=5, columnspan=1, rowspan=4, padx=(0, 20))
        bt_1.config(command=lambda: self.transfer_icon(bt_1, bt_2, data))
        bt_2.config(command=lambda: self.transfer_icon(bt_2, bt_1, data))
        # LOGIC TO CHECK IF THIS IS A NEW TRANSFER OR AN EDIT-----------------------------------------------------------
        if edit is not None:
            t_data = self.functions.get_transfer_data(edit)
            date_obj = datetime.strptime(t_data[0][4], '%Y-%m-%d')
            new_date = date_obj.strftime('%d-%m-%Y')
            bt_calendar.config(text=new_date)
            img_1 = ImageTk.PhotoImage(Image.open(t_data[0][8]).resize((90, 90)))
            bt_1.config(text=t_data[0][1], image=img_1)
            bt_1.image = img_1
            e_sum.insert(0, t_data[0][3])
            img_2 = ImageTk.PhotoImage(Image.open(t_data[1][8]).resize((90, 90)))
            bt_2.config(text=t_data[1][1], image=img_2)
            bt_2.image = img_2
            bt_confirm.config(text=f'{t_data[0][7]} {t_data[1][7]}')
            bt_delete.grid(row=0, column=5)

        self.f_2A8.lift()

    # FUNCTION TO OPEN OR CLOSE THE WALLET SETTINGS BUTTONS-------------------------------------------------------------
    def wallet_settings(self):
        if self.settings_toggle:
            self.settings_toggle = False
            self.settings_list[0].grid(row=0, column=1, rowspan=2, columnspan=2, sticky='w')
            self.settings_list[1].grid(row=0, column=2, rowspan=2, columnspan=2, sticky='w')
            self.settings_list[2].grid(row=0, column=3, rowspan=2, columnspan=2, sticky='w')
        else:
            self.settings_toggle = True
            self.settings_list[0].grid_remove()
            self.settings_list[1].grid_remove()
            self.settings_list[2].grid_remove()

    # FUNCTION TO DELETE THE CURRENT SELECTED WALLET--------------------------------------------------------------------
    def delete_wallet(self):
        ask = messagebox.askyesno("Confirm", "Are you sure you want to delete this wallet?")
        if ask:
            self.functions.delete_wallet(self.wallet, self.walled_oid)
            self.settings_toggle = True
            wallets = self.functions.retrieve_wallets()
            if wallets:
                self.wallets_frame()
            else:
                self.wallets_frame()
                self.static.garbage_collect(self.f_right)
                self.static.garbage_collect(self.f_left)
            self.update_exchange()

    # FUNCTION THAT CREATES THE EXCHANGE FRAME self.f_2A2---------------------------------------------------------------
    def exchange_frame(self):
        self.static.garbage_collect(self.f_2A2)

        f_left = Frame(self.f_2A2, bg=self.bg3, width=300, height=196)
        f_left.grid(row=0, column=0, sticky='nsew')
        f_left.grid_propagate(False)
        for i in range(6):
            f_left.rowconfigure(i, weight=1)
        style = ttk.Style()
        style.configure('OM.TButton')
        data_b = self.functions.update_balance(self.wallet)  # get the current coin
        font = ('Helvetica', 12)

        l_income = Label(f_left, text='Income:', bg=self.bg3, fg=self.fg, font=font)
        l_income.grid(row=0, rowspan=2, column=0, sticky='e')
        total_i = Label(f_left, bg=self.bg3, fg=self.fg, font=font)
        total_i.grid(row=0, rowspan=2, column=2, sticky='w')
        sv_income = StringVar()
        om_income = ttk.OptionMenu(f_left, sv_income, data_b[3], *coins, style='OM.TButton',
                                   command=lambda n=sv_income, m=0: self.update_exchange2(n, m))
        om_income.grid(row=0, rowspan=2, column=1, padx=3)

        l_expense = Label(f_left, text='Expense:', bg=self.bg3, fg=self.fg, font=font)
        l_expense.grid(row=2, rowspan=2, column=0, sticky='e')
        total_e = Label(f_left, bg=self.bg3, fg=self.fg, font=font)
        total_e.grid(row=2, rowspan=2, column=2, sticky='w')
        sv_expense = StringVar()
        om_expense = ttk.OptionMenu(f_left, sv_expense, data_b[3], *coins, style='OM.TButton',
                                    command=lambda n=sv_expense, m=1: self.update_exchange2(n, m))
        om_expense.grid(row=2, rowspan=2, column=1, columnspan=1, padx=3)

        l_balance = Label(f_left, text='Balance:', bg=self.bg3, fg=self.fg, font=font)
        l_balance.grid(row=4, rowspan=2, column=0, sticky='e')
        total_b = Label(f_left, bg=self.bg3, fg=self.fg, font=font)
        total_b.grid(row=4, rowspan=2, column=2, sticky='w')
        sv_balance = StringVar()
        om_balance = ttk.OptionMenu(f_left, sv_balance, data_b[3], *coins, style='OM.TButton',
                                    command=lambda n=sv_balance, m=2: self.update_exchange2(n, m))
        om_balance.grid(row=4, rowspan=2, column=1, padx=3)

        self.update_list.append([total_i, total_e, total_b])  # index 3
        self.update_list.append([om_income, om_expense, om_balance])  # index 4
        self.update_list.append([sv_income, sv_expense, sv_balance])  # index 5

        Frame(self.f_2A2, width=2, height=196, bd=10, relief='sunken').grid(row=0, column=1)

        def on_click_convert():
            sum_value = self.static.validate_input_number(e_coin1, self.f_2A2)
            if sum_value is None:
                return
            self.functions.exchange_rate(sv_coin1.get(), sv_coin2.get(), sum_value, l_coin2, l_reverse)

        f_right = Frame(self.f_2A2, bg=self.bg3, width=200, height=196)
        f_right.grid(row=0, column=2, sticky='nsew')
        f_right.grid_propagate(False)
        for i in range(6):
            f_right.rowconfigure(i, weight=1)
            f_right.columnconfigure(i, weight=1)

        l_convert = Label(f_right, text='Convert:', bg=self.bg3, fg=self.fg, font=('Arial', 15, 'italic'))
        l_convert.grid(row=0, column=0, columnspan=6)

        e_coin1 = Entry(f_right, bg=self.bg, fg=self.fg, font=('Times New Roman', 13), width=10)
        e_coin1.grid(row=1, column=0, rowspan=1, columnspan=3)
        sv_coin1 = StringVar()
        om_coin1 = ttk.OptionMenu(f_right, sv_coin1, data_b[3], *coins, style='OM.TButton')
        om_coin1.grid(row=1, column=3, rowspan=1, columnspan=2)

        img_convert = ImageTk.PhotoImage(Image.open('icons/tools/currency_convert.png').resize((50, 50)))
        bt_convert = Button(f_right, image=img_convert, bg=self.bg3, bd=0, activebackground=self.bg3, cursor='hand2')
        bt_convert.image = img_convert
        bt_convert.grid(row=2, column=0, rowspan=2, columnspan=3)

        l_rate = Label(f_right, text='Rate:', bg=self.bg3, fg=self.fg, font=('Times New Roman', 13))
        l_rate.grid(row=2, column=3, columnspan=3)
        l_reverse = Label(f_right, bg=self.bg3, fg=self.fg, font=('Times New Roman', 13))
        l_reverse.grid(row=3, column=3, columnspan=3)

        l_coin2 = Label(f_right,  bg=self.bg, fg=self.fg, font=('Times New Roman', 12), width=12)
        l_coin2.grid(row=4, column=0, rowspan=2, columnspan=3)
        sv_coin2 = StringVar()
        om_coin2 = ttk.OptionMenu(f_right, sv_coin2, data_b[3], *coins, style='OM.TButton')
        om_coin2.grid(row=4, column=3, rowspan=2, columnspan=2)
        bt_convert.config(command=on_click_convert)
        self.update_list.append([e_coin1, l_coin2])
        self.update_list.append([sv_coin1, sv_coin2])

        self.f_2A2.lift()

    # FUNCTION TO UPDATE THE EXCHANGE INFO IN THE EXCHANGE FRAME--------------------------------------------------------
    def update_exchange(self):
        total_income, total_expense = self.functions.wallet_total(self.wallet)  # get total income and expense
        total_income = 0 if total_income is None else total_income
        total_expense = 0 if total_expense is None else total_expense
        data_b = self.functions.update_balance(self.wallet)  # get the current balance
        if data_b is not None:
            if data_b[2].is_integer():
                balance = "{:.0f}".format(float(data_b[2]))  # convert the sum to a float with 2 decimals
            else:
                balance = "{:.2f}".format(float(data_b[2]))
        else:
            balance = 0

        self.update_list[3][0].config(text=f'{total_income} - 1.00')  # update the total income in the exchange
        self.update_list[3][1].config(text=f'{total_expense} - 1.00')  # update the total expense in the exchange
        self.update_list[3][2].config(text=f'{balance} - 1.00')  # update the current balance in the exchange

        if data_b is not None:
            for coin in self.update_list[5]:  # sets the coin for each stringvar in the exchange
                coin.set(data_b[3])
            self.update_list[7][0].set(data_b[3])
            self.update_list[7][1].set(data_b[3])
        else:
            pass

    def update_exchange2(self, var, index):
        total_income, total_expense = self.functions.wallet_total(self.wallet)  # get total income and expense
        total_income = 0 if total_income is None else total_income
        total_expense = 0 if total_expense is None else total_expense
        data_b = self.functions.update_balance(self.wallet)  # get the current balance
        balance = "{:.2f}".format(float(data_b[2]))  # convert the sum to a float with 2 decimals
        nums = [total_income, total_expense, balance]

        if var is not None:
            self.functions.exchange_rate(data_b[3], var, nums[index], self.update_list[3][index])
            self.update_list[5][index].set(var)
            
    # FUNCTION THAT CREATES THE MOVEMENTS FRAME WIDGETS self.f_2A3------------------------------------------------------
    def movement_frame(self, operation, action, edit=None, search=None, *_):
        def on_notes_click(*_):  # clear the 'Insert notes' when clicking inside the notes
            if notes.get(1.0, "end-1c") == 'Insert notes':
                notes.delete(1.0, "end-1c")

        def on_notes_focus_out(*_):  # insert 'Insert notes' when leaving the notes
            if not notes.get(1.0, "end-1c").strip():
                notes.insert(1.0, 'Insert notes')

        def collect_data():  # collect the data from the widgets and send it to the database
            sum_value = self.static.validate_input_number(e_sum, self.f_2A2)
            if sum_value is None:
                return
            notes_text = notes.get(1.0, "end-1c").strip()
            if notes_text == "Insert notes":
                notes_text = ""

            if bt_category.cget('text') == 'Category':
                messagebox.showerror("Error", "Select a category", parent=self.f_2A2)
                return

            date_str = bt_calendar.cget('text')
            date_ob = datetime.strptime(date_str, "%d-%m-%Y")
            formatted_date = date_ob.strftime("%Y-%m-%d")
            data = [bt_category.cget('text'), sum_value, formatted_date, notes_text, self.exp_type2[operation]]
            if action == 'INSERT':
                self.functions.create_update_movement(action, self.wallet, None, *data)
            else:
                self.functions.create_update_movement(action, self.wallet, v[7], *data)

            if search is not None:
                self.tree_search_frame(search)
            else:
                self.tree_menu_frame()
                self.tree_toggle()
            self.right_balance_update()
            self.update_exchange()
            self.f_2A2.lift()

        def delete_data(oid):  # delete the movement from the database
            ask = messagebox.askyesno("Confirm", "Are you sure you want to delete this movement?",
                                      parent=self.f_2A2)
            if ask:
                self.functions.delete_movement(oid)
                if search is not None:
                    self.tree_search_frame(search)
                else:
                    self.tree_toggle()
                    self.tree_menu_frame()
                self.update_exchange()
                self.right_balance_update()
                self.f_2A2.lift()

        self.static.garbage_collect(self.f_2A3)
        for i in range(6):
            self.f_2A3.rowconfigure(i, weight=1)
            self.f_2A3.columnconfigure(i, weight=1)
        current_date = date.today().strftime("%d-%m-%Y")
        img_calendar = ImageTk.PhotoImage(Image.open('icons/tools/calendar.png').resize((25, 25)))
        bt_calendar = Button(self.f_2A3, text=current_date, image=img_calendar, compound="right", bg=self.bg2,
                             command=lambda: self.static.grab_date(self.f_2A3, bt_calendar),
                             font=('Arial', 18), fg=self.fg, cursor='hand2', activebackground=self.bg2, border=0)
        bt_calendar.image = img_calendar
        bt_calendar.grid(row=0, column=0, rowspan=1, columnspan=3, sticky='w', padx=(29, 0))
        l_operation = Label(self.f_2A3, text=operation, bg=self.bg2, fg=self.fg, font=('Arial', 20), width=1)
        l_operation.grid(row=2, column=0, rowspan=1, columnspan=1, sticky='wn')
        e_sum = Entry(self.f_2A3, bg=self.bg, fg=self.fg, font=('Arial', 20), width=10)
        e_sum.bind('<Control-BackSpace>', self.static.entry_ctrl_delete)
        e_sum.grid(row=2, column=0, columnspan=3, rowspan=1, sticky='wn', padx=(30, 0))

        notes = Text(self.f_2A3, width=20, height=3, font=('Arial', 13), bg=self.bg, fg=self.fg)
        notes.insert(1.0, 'Insert notes')
        notes.bind("<Button-1>", on_notes_click)
        notes.bind("<FocusOut>", on_notes_focus_out)
        notes.bind('<Control-BackSpace>', self.static.entry_ctrl_delete)
        notes.grid(row=3, column=0, rowspan=3, columnspan=3, sticky='w', padx=(18, 0))

        img_category = ImageTk.PhotoImage(Image.open('icons/tools/choose_category.png').resize((100, 100)))
        bt_category = Button(self.f_2A3, text='Category', image=img_category, bg=self.bg2, bd=0, compound='top',
                             activebackground=self.bg2, cursor='hand2', font=('Arial', 15), fg=self.fg)
        bt_category.config(command=lambda: self.movement_icon(bt_category, self.f_2A3, operation))
        bt_category.image = img_category
        bt_category.grid(row=0, column=3, columnspan=3, rowspan=5, padx=(0, 40), pady=5)

        img_delete = ImageTk.PhotoImage(Image.open('icons/tools/delete.png').resize((25, 25)))
        bt_delete = Button(self.f_2A3, image=img_delete, bg=self.bg2, bd=0, activebackground=self.bg2,
                           cursor='hand2')
        bt_delete.image = img_delete
        bt_delete.config(state=self.status[self.role])

        img_confirm = ImageTk.PhotoImage(Image.open('icons/tools/action_confirm.png').resize((30, 30)))
        bt_confirm = Button(self.f_2A3, image=img_confirm, bg=self.bg2, bd=0, activebackground=self.bg2,
                            cursor='hand2')
        bt_confirm.config(command=collect_data, state=self.status[self.role])
        bt_confirm.image = img_confirm
        bt_confirm.grid(row=5, column=3, rowspan=1, columnspan=1, sticky='w', padx=(0, 40), pady=5)

        img_cancel = ImageTk.PhotoImage(Image.open('icons/tools/action_cancel.png').resize((30, 30)))
        bt_cancel = Button(self.f_2A3, image=img_cancel, bg=self.bg2, bd=0, activebackground=self.bg2,
                           cursor='hand2')
        bt_cancel.config(command=lambda: self.f_2A2.lift())
        bt_cancel.image = img_cancel
        bt_cancel.grid(row=5, column=5, rowspan=1, columnspan=1, sticky='w', pady=5)

        if edit is not None:
            selected = edit.focus()
            v = edit.item(selected, 'values')
            date_obj = datetime.strptime(v[4], '%Y-%m-%d')
            new_date = date_obj.strftime('%d-%m-%Y')
            bt_calendar.config(text=new_date)
            l_operation.config(text=self.exp_type[v[6]])
            e_sum.insert(0, v[3])
            notes.delete("1.0", "end")
            notes.insert("1.0", v[5])
            new_image = ImageTk.PhotoImage(Image.open(v[8]).resize((100, 100)))
            bt_category.config(image=new_image, text=v[2])
            bt_category.image = new_image
            bt_delete.config(command=lambda n=v[7]: delete_data(n))
            bt_delete.grid(row=0, column=5, rowspan=1, sticky='nsew')
        self.f_2A3.lift()
        self.f_2A.lift()

    # FUNCTION TO CREATE THE WIDGETS FOR THE TREE MENU FRAME self.f_2B1-------------------------------------------------
    def tree_menu_frame(self):
        self.static.garbage_collect(self.f_2B1)
        self.static.garbage_collect(self.f_2B2)
        for i in range(5):
            self.f_2B1.columnconfigure(i, weight=1)
        for j in range(3):
            self.f_2B2.rowconfigure(j, weight=1)

        # FIRST BUTTON THAT SERVES TO CALL THE ADD CATEGORY FRAME-------------------------------------------------------
        img1 = ImageTk.PhotoImage(Image.open('icons/tools/add_new.png').resize((30, 30)))
        btn1 = Button(self.f_2B1, image=img1, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
        btn1.config(command=self.add_category_frame)
        btn1.image = img1
        btn1.grid(row=0, column=0, pady=8, padx=(0, 5))

        # SECOND BUTTON THAT SERVES TO CALL THE CATEGORY LIST FRAME-----------------------------------------------------
        img2 = ImageTk.PhotoImage(Image.open('icons/tools/categories_list.png').resize((30, 30)))
        btn2 = Button(self.f_2B1, image=img2, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
        btn2.config(command=self.show_category_frame)
        btn2.image = img2
        btn2.grid(row=0, column=1, pady=8, padx=(0, 5))

        # THIRD WIDGET THAT SHOWS IF YOU ARE IN THE CATEGORY FRAME OR THE DATE FRAME------------------------------------
        lbl3 = Label(self.f_2B1, text='Category', bg=self.bg, fg=self.fg, font=('Arial', 18), width=8)
        lbl3.grid(row=0, column=2, pady=8, padx=(0, 5))

        # FOURTH BUTTON THAT SERVES TO CALL THE SEARCH FRAME------------------------------------------------------------
        img4 = ImageTk.PhotoImage(Image.open('icons/tools/search.png').resize((30, 30)))
        btn4 = Button(self.f_2B1, image=img4, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
        btn4.config(command=lambda: (self.f_2B2.lift(), self.f_2B5.lift()))
        btn4.image = img4
        btn4.grid(row=0, column=3, pady=8, padx=(0, 5))

        # FIFTH BUTTON THAT SERVES TO SWITCH BETWEEN THE CATEGORY AND DATE FRAME----------------------------------------
        img5 = ImageTk.PhotoImage(Image.open('icons/tools/sort_by_category.png').resize((35, 35)))
        btn5 = Button(self.f_2B1, image=img5, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
        btn5.config(command=lambda n=btn5, m=lbl3: self.switch_tree(n, m))
        btn5.image = img5
        btn5.grid(row=0, column=4, pady=8, padx=(0, 5))

        # SEARCH FRAME THAT CONTAINS THE SEARCH ENTRY AND THE CANCEL BUTTON---------------------------------------------
        e_search = Entry(self.f_2B2, bg=self.bg2, fg=self.fg, width=15, font=('Arial', 16))
        e_search.bind('<KeyRelease>', lambda e: self.tree_search_frame(e_search.get()))
        e_search.grid(row=0, column=0, rowspan=3, padx=30)

        img_cancel = ImageTk.PhotoImage(Image.open('icons/tools/action_cancel.png').resize((25, 25)))
        bt_cancel = Button(self.f_2B2, image=img_cancel, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
        bt_cancel.config(command=lambda:  (self.f_2B1.lift(), self.tree_toggle(), e_search.delete(0, 'end')))
        bt_cancel.image = img_cancel
        bt_cancel.grid(row=0, column=1, rowspan=3)
        self.f_2B1.lift()

    # FUNCTION TO CREATE THE WIDGETS FOR THE ADD CATEGORY FRAME self.f_2A5----------------------------------------------
    def add_category_frame(self, edit=None):

        # FUNCTION TO CONFIRM AND VALIDATE THE DATA FOR THE NEW CATEGORY------------------------------------------------
        def confirm_new():
            name = e_name.get()
            categories = self.functions.get_categories()
            count = sum(1 for cat in categories if not cat[1].startswith('TO-') and not cat[1].startswith('FROM-'))
            if name == '':
                messagebox.showerror('Error', 'Please enter a name', parent=self.f_2A5)
                return

            elif len(name) < 3 or len(name) > 12:
                messagebox.showerror("Error", "Name must be between 3 and 12 characters", parent=self.f_2A5)
                return

            elif name.startswith('TO-') or name.startswith('FROM-'):
                messagebox.showerror("Error", "Name cannot start with 'TO-' or 'FROM-'", parent=self.f_2A5)
                return

            elif count >= 30:
                messagebox.showerror("Error", "You can only have 30 categories", parent=self.f_2A5)
                return

            elif self.functions.category_exist(name.capitalize()) and (edit is None or edit[1].lower() != name.lower()):
                messagebox.showerror('Error', 'Name already exists', parent=self.f_2A5)
                return

            elif btn.cget('text') == '':
                messagebox.showerror('Error', 'Please select a type', parent=self.f_2A5)
                return

            else:
                path = f'icons/category/{btn.cget('text')}.png'
                if edit is not None:
                    self.functions.create_update_category(name.capitalize(), e_type.get(), path, 'UPDATE', edit)
                else:
                    self.functions.create_update_category(name.capitalize(), e_type.get(), path, 'INSERT')
                self.tree_toggle()
                self.f_2A2.lift()

        self.static.garbage_collect(self.f_2A5)
        for i in range(6):
            self.f_2A5.columnconfigure(i, weight=1)
            self.f_2A5.rowconfigure(i, weight=1)
        l_name = LabelFrame(self.f_2A5, text='Name', bg=self.bg2, fg=self.fg, font=('Arial', 18, 'italic'))
        l_name.grid(row=0, column=0, rowspan=3, columnspan=1, sticky='nsew')
        e_name = Entry(l_name, bg=self.bg, fg=self.fg, font=('Arial', 20), width=10)
        e_name.bind('<Control-BackSpace>', self.static.entry_ctrl_delete)
        e_name.pack(pady=20, padx=20, ipady=6)

        l_type = LabelFrame(self.f_2A5, text='Type', bg=self.bg2, fg=self.fg, font=('Arial', 18, 'italic'))
        l_type.grid(row=3, column=0, rowspan=3, columnspan=1, sticky='nsew', ipady=20)

        e_type = StringVar(value='income')
        income_radio = Radiobutton(l_type, text='income', variable=e_type, value='income', bg=self.bg2,
                                   font=('Arial', 15), activebackground=self.bg2)
        income_radio.pack(side='left', padx=(20, 0))
        expense_radio = Radiobutton(l_type, text='expense', variable=e_type, value='expense', bg=self.bg2,
                                    font=('Arial', 15), activeforeground=self.fg, activebackground=self.bg2)
        expense_radio.pack(side='right', padx=(0, 20))

        img = ImageTk.PhotoImage(Image.open('icons/tools/choose_category.png').resize((100, 100)))
        btn = Button(self.f_2A5, image=img, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        btn.config(command=lambda: self.category_icon('category', btn, self.f_2A5, 100, 100))
        btn.image = img
        btn.grid(row=0, column=3, columnspan=3, rowspan=4, sticky='nsew', padx=(0, 30))

        img_confirm = ImageTk.PhotoImage(Image.open('icons/tools/action_confirm.png').resize((30, 30)))
        bt_confirm = Button(self.f_2A5, image=img_confirm, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        bt_confirm.config(command=confirm_new)
        bt_confirm.image = img_confirm
        bt_confirm.grid(row=5, column=4, columnspan=1, rowspan=1, sticky='nsew')

        imc_cancel = ImageTk.PhotoImage(Image.open('icons/tools/action_cancel.png').resize((30, 30)))
        bt_cancel = Button(self.f_2A5, image=imc_cancel, bg=self.bg2, bd=0, activebackground=self.bg2, cursor='hand2')
        bt_cancel.config(command=self.f_2A2.lift)
        bt_cancel.image = imc_cancel
        bt_cancel.grid(row=5, column=5, columnspan=1, rowspan=1, sticky='nsew')

        if edit is not None:
            p = edit[3].replace("icons/category/", "").rstrip(".png")
            e_name.insert(0, edit[1])
            e_type.set(edit[2])
            img = ImageTk.PhotoImage(Image.open(edit[3]).resize((110, 100)))
            btn.config(text=p, image=img)
            btn.image = img
            bt_cancel.config(command=lambda: self.f_2A6.lift())
            income_radio.config(state='disabled')
            expense_radio.config(state='disabled')
        self.f_2A5.lift()
        self.f_2A.lift()

    # FUNCTION TO SHOW ALL THE CATEGORIES FRAME-------------------------------------------------------------------------
    def show_category_frame(self):

        def confirm_delete(name, oid):
            ask = messagebox.askquestion("Delete", "Are you sure you want to delete this category?")
            if ask == 'yes':
                self.functions.delete_category(name, oid)
                self.right_balance_update()
                self.show_category_frame()

        self.static.garbage_collect(self.f_2A3)
        frame = self.static.create_canvas(self.f_2A3)
        self.static.garbage_collect(frame)
        categories = self.functions.get_categories()
        data = self.functions.all_category_view()
        d1 = {item[0]: item[3] for item in data}
        d2 = {item[0]: item[4] for item in data}

        Frame(frame, width=500, bg=self.bg).grid(row=0, column=0, columnspan=10)
        check = True
        row = 1
        img_merge = ImageTk.PhotoImage(Image.open('icons/tools/merge_categories.png').resize((20, 20)))
        img_edit = ImageTk.PhotoImage(Image.open('icons/tools/edit.png').resize((20, 20)))
        img_delete = ImageTk.PhotoImage(Image.open('icons/tools/delete.png').resize((20, 20)))
        for c in categories:
            if c[2] == 'expense' and check:
                Frame(frame, width=500, height=2, bd=10, relief='sunken').grid(row=row, column=0, columnspan=10)
                check = False
                row += 1
            if c[1].startswith('TO-') or c[1].startswith('FROM-'):
                continue
            img_icon = ImageTk.PhotoImage(Image.open(c[3]).resize((50, 50)))
            bt_icon = Button(frame, image=img_icon, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
            bt_icon.image = img_icon
            bt_icon.grid(row=row, column=0, pady=5)

            font = self.static.calculate_font_size(c[1], base_size=14, min_size=10)
            l_name = Label(frame, text=c[1], bg=self.bg, fg=self.fg, font=('Arial', font))
            l_name.grid(row=row, column=1, sticky='w')

            l_type = Label(frame, text=self.exp_type[c[2]], bg=self.bg, font=('Arial', 25, 'italic'))
            l_type.grid(row=row, column=2)
            l_type.config(fg='green' if c[2] == 'income' else 'red')

            total = d1.get(c[1])
            num = d2.get(c[1])
            if total is not None:
                font = self.static.calculate_font_size(str(total), base_size=16, min_size=12)
                l_total = Label(frame, text=f'{total} ({num})', bg=self.bg, fg=self.fg, font=('Arial', font))
                l_total.grid(row=row, column=3, sticky='w')

            bt_edit = Button(frame, image=img_edit, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
            bt_edit.config(command=lambda n=c: self.add_category_frame(n), state=self.status[self.role])
            bt_edit.image = img_edit
            bt_edit.grid(row=row, column=4)

            bt_merge = Button(frame, image=img_merge, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
            bt_merge.config(state=self.status[self.role])
            bt_merge.bind("<Button-1>", lambda event, c_data=c: self.show_merge_options(event, c_data))
            bt_merge.image = img_merge
            bt_merge.grid(row=row, column=5)

            bt_delete = Button(frame, image=img_delete, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2')
            bt_delete.config(command=lambda n=c[1], m=c[4]: confirm_delete(n, m), state=self.status[self.role])
            bt_delete.image = img_delete
            bt_delete.grid(row=row, column=6)

            row += 1

        self.f_2A3.lift()
        self.f_2A.lift()

    # FUNCTION TO SHOW THE OPTIONS TO MERGE TWO CATEGORIES--------------------------------------------------------------
    def show_merge_options(self, event, c):
        def confirm_merge(c_data):
            ask = messagebox.askyesno("Confirm", f"Are you sure you want to merge {c[1]} with {c_data[1]}?")
            if ask:
                self.functions.merge_categories(c_data[1], c[1])
                self.show_category_frame()
                self.tree_toggle()
        merge_menu = Menu(None, tearoff=0, relief='sunken', bg=self.bg, fg=self.fg, activebackground=self.bg2)
        merge_menu.add_command(label=f"Merge {c[1]} with:")
        categories = self.functions.get_merge_categories(c[1], c[2])
        for i in categories:
            merge_menu.add_command(label=i[1], command=lambda n=i: confirm_merge(n))
        merge_menu.post(event.x_root, event.y_root)

    # FUNCTION TO CREATE A TREEVIEW OF THE WALLET MOVEMENTS-------------------------------------------------------------
    def tree_category_frame(self):
        def selected_treeview(*_):
            item = tree.selection()[0]
            item_type = tree.parent(item)
            if item_type != "":
                if tree.item(item)['values'][5].startswith('UUID-'):
                    self.transfer_frame('UPDATE', tree.item(item)['values'][5])
                else:
                    self.movement_frame(self.exp_type[tree.item(item)["values"][6]], 'UPDATE', tree)
                    self.f_2A3.lift()
            else:
                pass

        self.static.garbage_collect(self.f_2B3)
        data_c = self.functions.category_view(self.wallet)
        tree = ttk.Treeview(self.f_2B3, show='tree', selectmode='extended', height=10)
        tree.column('#0', width=280, minwidth=280)
        tree.images = {}
        for c1 in data_c:
            image_path = c1[2]
            if image_path not in tree.images:
                img = ImageTk.PhotoImage(Image.open(image_path).resize((33, 33)))
                tree.images[image_path] = img
            else:
                img = tree.images[image_path]
            parent_id = tree.insert('', 'end', text=f'{c1[0]}  ({c1[4]})  {self.exp_type[c1[1]]} {c1[3]}', image=img)
            data_d = self.functions.category_view2(self.wallet, c1[0])
            for c2 in data_d:
                date_obj = datetime.strptime(c2[4], '%Y-%m-%d')
                new_date = date_obj.strftime('%d-%m-%Y')
                if c2[5] != '':
                    text = f'{new_date}  {self.exp_type[c2[6]]}{c2[3]} \n# {c2[5]}'
                    if c2[5].startswith('UUID-'):
                        text = f'{c2[4]}  {self.exp_type[c2[6]]}{c2[3]}'
                    tree.insert(parent_id, 'end', text=text, values=c2 + (c1[2],))
                else:
                    text = f'{new_date}  {self.exp_type[c2[6]]}{c2[3]}'
                    tree.insert(parent_id, 'end', text=text, values=c2 + (c1[2],))
                tree.bind("<Double-1>", selected_treeview)

        scroll_c = Scrollbar(self.f_2B3, orient='vertical', command=tree.yview)
        scroll_c.grid(row=0, column=1, sticky="NS")
        tree.config(yscrollcommand=scroll_c.set)
        tree.grid(row=0, column=0, sticky='nsew')

        # STYLE AND THEME OF THE TREEVIEW-------------------------------------------------------------------------------
        theme = 'default'
        style_c = ttk.Style()
        style_c.theme_use(theme)
        style_c.configure('Treeview', rowheight=37, fieldbackground=self.bg, background=self.bg, foreground=self.fg,
                          font=('Arial', 13))
        self.f_2B3.lift()

    # FUNCTION TO CREATE TREEVIEW ORGANIZED BY DATE---------------------------------------------------------------------
    def tree_date_frame(self):
        def selected_treeview(*_):
            item = tree.selection()[0]
            item_type = tree.parent(item)
            if item_type != "":  # checks if there is a comment in the selected item
                if tree.item(item)['values'][5].startswith('UUID-'):  # if is transfer calls transfer_frame2
                    self.transfer_frame('UPDATE', tree.item(item)['values'][5])
                else:  # else calls add_remove_frame
                    self.movement_frame(self.exp_type[tree.item(item)["values"][6]], 'UPDATE', tree)
                    self.f_2A3.lift()
            else:
                pass

        self.static.garbage_collect(self.f_2B4)

        data_c = self.functions.date_view(self.wallet)
        tree = ttk.Treeview(self.f_2B4, show='tree', selectmode='extended', height=10)
        tree.column('#0', width=280, minwidth=280)
        tree.images = {}
        for c1 in data_c:
            sign = '+' if c1[2] >= 0 else ''
            date_obj = datetime.strptime(c1[0], '%Y-%m-%d')
            new_date = date_obj.strftime('%d-%m-%Y')
            parent_id = tree.insert('', 'end', text=f'{new_date} ({c1[1]})  {sign}{round(c1[2], 2)}',)
            data_d = self.functions.date_view2(self.wallet, c1[0])
            for c2 in data_d:
                image_path = c2[8]
                if image_path not in tree.images:
                    img = ImageTk.PhotoImage(Image.open(image_path).resize((33, 33)))
                    tree.images[image_path] = img
                else:
                    img = tree.images[image_path]
                if c2[5] != '':
                    text = f'{self.exp_type[c2[6]]}{c2[3]}  {c2[2]}\n# {c2[5]}'
                    if c2[5].startswith('UUID-'):
                        text = f'{self.exp_type[c2[6]]}{c2[3]}  {c2[2]}'
                    tree.insert(parent_id, 'end', text=text, values=c2 + (c1[2],), image=img)
                else:
                    text = f'  {self.exp_type[c2[6]]}{c2[3]}  {c2[2]}   '
                    tree.insert(parent_id, 'end', text=text, values=c2 + (c1[2],), image=img)
                tree.bind("<Double-1>", selected_treeview)
        scroll_c = Scrollbar(self.f_2B4, orient='vertical', command=tree.yview)
        scroll_c.grid(row=0, column=1, sticky="NS")
        tree.config(yscrollcommand=scroll_c.set)
        tree.grid(row=0, column=0, sticky='nsew')

        # STYLE AND THEME OF THE TREEVIEW-------------------------------------------------------------------------------
        theme = 'default'
        style_c = ttk.Style()
        style_c.theme_use(theme)
        style_c.configure('Treeview', rowheight=37, fieldbackground=self.bg, background=self.bg, foreground=self.fg,
                          font=('Arial', 13))
        self.f_2B4.lift()

    # FUNCTION TO CREATE A TREEVIEW OF THE WALLET MOVEMENT BY SEARCH----------------------------------------------------
    def tree_search_frame(self, search, *_):
        def selected_treeview(*_):
            item = tree.selection()[0]
            if tree.item(item)['values'][5].startswith('UUID-'):
                self.transfer_frame('UPDATE', tree.item(item)['values'][5])
            else:
                self.movement_frame(self.exp_type[tree.item(item)["values"][6]], 'UPDATE', tree, search)
                self.f_2A3.lift()

        self.static.garbage_collect(self.f_2B5)
        if not search.strip():
            return
        data_c = self.functions.search_view(self.wallet, search)
        tree = ttk.Treeview(self.f_2B5, show='tree', selectmode='extended', height=10)
        tree.column('#0', width=280, minwidth=280)
        tree.images = {}
        for c in data_c:
            image_path = c[8]
            if image_path not in tree.images:
                img = ImageTk.PhotoImage(Image.open(image_path).resize((33, 33)))
                tree.images[image_path] = img
            else:
                img = tree.images[image_path]
            date_obj = datetime.strptime(c[4], '%Y-%m-%d')
            new_date = date_obj.strftime('%d-%m-%Y')
            if c[5] != '':
                text = f'{c[2]} ({new_date}) {self.exp_type[c[6]]} {c[3]}\n {c[5]}'
                if c[5].startswith('UUID-'):
                    text = f'{c[2]} ({c[4]}) {self.exp_type[c[6]]} {c[3]}'
                tree.insert('', 'end', text=text, values=c, image=img)
            else:
                text = f'{c[2]}  ({new_date})  {self.exp_type[c[6]]} {c[3]}'
                tree.insert('', 'end', text=text, values=c, image=img)

        tree.bind("<Double-1>", selected_treeview)
        scroll_c = Scrollbar(self.f_2B5, orient='vertical', command=tree.yview)
        scroll_c.grid(row=0, column=1, sticky="NS")
        tree.config(yscrollcommand=scroll_c.set)
        tree.grid(row=0, column=0, sticky='w')

        # STYLE AND THEME OF THE TREEVIEW-------------------------------------------------------------------------------
        theme = 'default'
        style_c = ttk.Style()
        style_c.theme_use(theme)
        style_c.configure('Treeview', rowheight=37, fieldbackground=self.bg, background=self.bg, foreground=self.fg,
                          font=('Arial', 11))
        self.f_2B5.lift()

    # FUNCTION TO KEEP OPEN THE CURRENT TREEVIEW------------------------------------------------------------------------
    def tree_toggle(self):
        if self.c_toggle:
            self.tree_category_frame()
        else:
            self.tree_date_frame()

    # FUNCTION TO SWITCH BETWEEN THE DATE AND CATEGORY TREEVIEW---------------------------------------------------------
    def switch_tree(self, btn, lbl):
        if self.c_toggle:
            self.c_toggle = False
            self.tree_toggle()
            lbl.config(text='Date', bg=self.bg, fg=self.fg)
            img = ImageTk.PhotoImage(Image.open('icons/tools/sort_by_date.png').resize((35, 35)))
            btn.config(image=img)
            btn.image = img
        else:
            self.c_toggle = True
            self.tree_toggle()
            lbl.config(text='Category', bg=self.bg, fg=self.fg)
            img = ImageTk.PhotoImage(Image.open('icons/tools/sort_by_category.png').resize((35, 35)))
            btn.config(image=img)
            btn.image = img

    # FUNCTION TO CREATE A PIE CHART FRAME OF THE SELECTED WALLET-------------------------------------------------------
    def chart_frame(self):
        self.static.garbage_collect(self.f_2C2)

        def cancel():
            self.f_2A.lift()
            self.pie_toggle = False

        lbl = Button(self.f_2C1, text='Return', bg=self.bg, fg=self.fg, font=('Arial', 20))
        lbl.config(command=cancel)
        lbl.grid(row=0, column=0, sticky='e')

        data = [item for item in self.functions.category_view(self.wallet) if item[1].lower() == 'expense']
        data = sorted(data, key=lambda n: n[3], reverse=True)

        # Limit the data to the top 13 items
        data = data[:13]
        categories = [item[0] for item in data]
        values = [item[3] for item in data]
        icon_paths = [item[2] for item in data]

        hex_colors = []
        for icon_path in icon_paths:
            img = Image.open(icon_path)
            rgb = img.quantize(colors=2, method=2)
            hex_color = '#%02x%02x%02x' % tuple(rgb.getpalette()[3:6])
            hex_colors.append(hex_color)

        # Create the figure for the pie chart
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(self.bg2)

        ax = fig.add_subplot(111)
        ax.set_facecolor(self.bg2)
        # Reduce left margin to move the chart to the left
        fig.subplots_adjust(left=0.04, right=0.7, top=0.95, bottom=0.15)

        # Pie chart properties
        wedge_properties = {"width": 0.3, "edgecolor": self.bg2, 'linewidth': 1}
        wedges, texts, autotexts = ax.pie(values, startangle=90, colors=hex_colors, wedgeprops=wedge_properties,
                                          autopct='%1.1f%%')
        ax.axis('equal')

        # Set the font size for the percentage labels inside the pie
        for i, autotext in enumerate(autotexts):
            autotext.set_fontsize(9)
            theta = (wedges[i].theta1 + wedges[i].theta2) / 2
            theta_rad = np.deg2rad(theta)
            x = 1.1 * np.cos(theta_rad)
            y = 1.1 * np.sin(theta_rad)
            autotext.set_position((x, y))
            autotext.set_horizontalalignment('center')
            autotext.set_verticalalignment('center')
            autotext.set_color('white')

        # Add the chart to the main frame using grid
        chart = FigureCanvasTkAgg(fig, self.f_2C2)
        chart.draw()
        chart.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        center_x = 0
        center_y = 0

        # Define the labels and their vertical offset
        data_b = self.functions.update_balance(self.wallet)
        income, expense = self.functions.wallet_total(self.wallet)  # get total income and expense
        income = 0 if income is None else income
        expense = 0 if expense is None else expense
        f_income = f"{income:,.2f} {data_b[3]}"
        f_expense = f"{expense:,.2f} {data_b[3]}"
        vertical_offset = 0.1  # adjust as needed for proper spacing

        # Add the first label at the center
        ax.text(center_x, center_y + vertical_offset, f_income, ha='center', va='center', fontsize=10, color='#3FFF00',
                weight='bold')

        # Add the second label below the first one
        ax.text(center_x, center_y - vertical_offset, f_expense, ha='center', va='center', fontsize=10, color='#FF2800',
                weight='bold')

        ax.legend(wedges, categories, title="Categories", loc="center left", bbox_to_anchor=(1.05, 0.5))
        chart.draw()

        self.f_2C.lift()

    # FUNCTION TO SELECT THE ICON FOR THE MOVEMENT self.f_2A4-----------------------------------------------------------
    def movement_icon(self, icon, frame, operation):

        def confirm_icon(img_path, category):
            new_img = ImageTk.PhotoImage(Image.open(img_path).resize((100, 100)))
            icon.config(image=new_img, text=category)
            icon.image = new_img
            frame.lift()

        self.static.garbage_collect(self.f_2A4)
        frame1 = self.static.create_canvas(self.f_2A4)
        row = 0
        col = 0
        for icons in self.functions.get_icon(self.exp_type2[operation]):
            if icons[3] == 'icons/category/transfer-TO.png' or icons[3] == 'icons/category/transfer-FROM.png':
                continue
            else:
                font = self.static.calculate_font_size(icons[1])
                img = ImageTk.PhotoImage(Image.open(icons[3]).resize((68, 68)))
                bt = Button(frame1, image=img, bg=self.bg, bd=0, activebackground=self.bg, cursor='hand2',
                            fg=self.fg, text=icons[1], compound='top', font=('Arial', font))
                bt.config(command=lambda i=icons[3], category=icons[1]: confirm_icon(i, category))
                bt.image = img
                bt.grid(row=row, column=col, sticky='nsew', padx=5, pady=10)

                if col == 5:
                    col = 0
                    row += 1
                else:
                    col += 1
        self.f_2A4.lift()

    # FUNCTION TO SELECT THE ICON FOR THE TRANSFER self.f_2A4-----------------------------------------------------------
    def transfer_icon(self, button1, button2, data):

        def confirm_icon(i, n):
            new_img = ImageTk.PhotoImage(Image.open(i).resize((90, 90)))
            button1.config(text=n, image=new_img)
            button1.image = new_img
            self.f_2A8.lift()

        self.static.garbage_collect(self.f_2A4)
        frame = self.static.create_canvas(self.f_2A4)
        back_btn = Button(self.f_2A4, text='x', bg=self.bg, fg='red', font=('Arial', 10), bd=0,
                          activebackground=self.bg, cursor='hand2')
        back_btn.config(command=lambda: self.f_2A8.lift())
        back_btn.grid(row=0, column=0, sticky='ne', columnspan=1)

        row = 1
        col = 0
        wallets = self.functions.retrieve_wallets()
        for wallet in wallets:
            if wallet[1] == button2.cget('text'):
                continue
            elif wallet[3] != data[3]:
                continue
            img = ImageTk.PhotoImage(Image.open(wallet[6]).resize((60, 60)))
            btn = Button(frame, text=wallet[1], image=img, bg=self.bg, bd=0, activebackground=self.bg, fg=self.fg,
                         cursor='hand2', compound='top', font=('Arial', 12))
            btn.config(command=lambda i=wallet[6], n=wallet[1]: confirm_icon(i, n))
            btn.image = img
            btn.grid(row=row, column=col, sticky='nsew', padx=7, pady=5)
            if col == 5:
                col = 0
                row += 1
            else:
                col += 1
        self.f_2A4.lift()

    # FUNCTION TO SELECT ICON FOR CATEGORY AND WALLETS self.f_2A4-------------------------------------------------------
    def category_icon(self, path, widget, lift, x, y):

        # FUNCTION TO CONFIRM AND VALIDATE THE DATA FOR THE NEW CATEGORY------------------------------------------------
        def confirm_icon(img_path, category):
            new_img = ImageTk.PhotoImage(Image.open(img_path).resize((x, y)))
            widget.config(image=new_img, text=category)
            widget.image = new_img
            lift.lift()

        self.static.garbage_collect(self.f_2A4)
        frame = self.static.create_canvas(self.f_2A4)
        back_btn = Button(self.f_2A4, text='x', bg=self.bg, fg='red', font=('Arial', 10), bd=0,
                          activebackground=self.bg, cursor='hand2')
        back_btn.config(command=lambda: lift.lift())
        back_btn.grid(row=0, column=0, sticky='ne', columnspan=1)

        def create_buttons(p, f):
            row = 1
            col = 0
            for filename in os.listdir(f'icons/{p}'):
                if filename.endswith(".png"):
                    if filename == 'transfer-TO.png' or filename == 'transfer-FROM.png':
                        continue
                    else:
                        img = ImageTk.PhotoImage(Image.open(f'icons/{p}/{filename}').resize((65, 65)))
                        name = os.path.splitext(filename)[0]
                        btn = Button(f, text=name, image=img, bg=self.bg, bd=0, activebackground=self.bg,
                                     cursor='hand2')
                        btn.config(command=lambda i=f'icons/{p}/{filename}', n=name: confirm_icon(i, n))
                        btn.image = img
                        btn.grid(row=row, column=col, sticky='nsew', padx=7, pady=10)
                        if col == 5:
                            col = 0
                            row += 1
                        else:
                            col += 1

        button_thread = threading.Thread(target=create_buttons, args=(path, frame))
        button_thread.start()
        self.f_2A4.lift()
