from Authenticate import *
from Signup import *
from tkinter import *
from PIL import Image, ImageTk


class Login:
    def __init__(self, master):
        self.root = master
        self.root.title('Wallet')
        self.root.resizable(False, False)
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        app_w = 350
        app_h = 400
        self.root.geometry(f'{app_w}x{app_h}+{(screen_w // 2) - (app_w // 2)}+{(screen_h // 2) - (app_h // 2)}')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.iconbitmap('icons/tools/wallet.ico')
        self.bg = '#404040'
        self.bg2 = '#606060'
        self.fg = '#ffffff'
        self.font = ('Arial', 19, 'italic')
        icon_w = 80
        icon_h = 80

        # MAIN LOGIN FRAME AND THE LOOP CONFIGURE OF THE COLUMNS AND THE ICONS------------------------------------------
        self.f_login = Frame(self.root, width=app_w, height=app_h, bg=self.bg)
        self.f_login.grid(row=0, column=0)
        self.f_login.grid_propagate(False)
        for i in range(4):
            self.f_login.columnconfigure(index=i, weight=1)
            login_icon = ImageTk.PhotoImage(Image.open(f'icons/tools/login_icon {i+1}.png').resize((icon_w, icon_h)))
            self.l_login = Label(self.f_login, image=login_icon, bg=self.bg)
            self.l_login.image = login_icon
            self.l_login.grid(row=0, column=i, pady=5)

        # USERNAME LABELFRAME AND ENTRY---------------------------------------------------------------------------------
        self.lf_username = LabelFrame(self.f_login, text='Username', font=self.font, bg=self.bg, fg=self.fg)
        self.lf_username.grid(row=1, column=0, columnspan=4, padx=25, pady=10, sticky='ew')
        self.e_username = Entry(self.lf_username, font=self.font, width=13, bg=self.bg2, fg=self.fg)
        self.e_username.grid(row=0, column=0, padx=50, pady=5)  # Changed from pack to grid

        # PASSWORD LABELFRAME AND ENTRY--------------------------------------------------------------------------------
        self.lf_password = LabelFrame(self.f_login, text='Password', font=self.font, bg=self.bg, fg=self.fg)
        self.lf_password.grid(row=2, column=0, columnspan=4, padx=25, pady=10, sticky='ew')
        self.e_password = Entry(self.lf_password, font=self.font, show='*', width=13, bg=self.bg2, fg=self.fg)
        self.e_password.grid(row=0, column=0, padx=(50, 10), pady=5)

        # SHOW AND HIDE PASSWORD BUTTON AND IMAGES----------------------------------------------------------------------
        self.show_pass = ImageTk.PhotoImage(Image.open('icons/tools/pass_shown.png').resize((20, 20)))
        self.hide_pass = ImageTk.PhotoImage(Image.open('icons/tools/pass_hidden.png').resize((20, 20)))
        self.show_hide = Button(self.lf_password, image=self.hide_pass, bg=self.bg, bd=0, cursor='hand2')
        self.show_hide.config(command=self.password_view, activebackground=self.bg)
        self.show_hide.grid(row=0, column=1, padx=(0, 5), pady=5)

        # LABEL FOR SHOWING ERRORS--------------------------------------------------------------------------------------
        self.l_message = Label(self.f_login, text='', bg=self.bg, font=('Arial', 12), fg='red')
        self.l_message.grid(row=3, column=0, columnspan=4, sticky='ew')

        # LOGIN AND SIGNUP BUTTONS WITH ICONS---------------------------------------------------------------------------
        login_bt = ImageTk.PhotoImage(Image.open('icons/tools/login.png').resize((100, 50)))
        self.bt_login = Button(self.f_login, image=login_bt, cursor="hand2", bg=self.bg, bd=0, activebackground=self.bg)
        self.bt_login.image = login_bt
        self.bt_login.grid(row=4, column=0, columnspan=2)
        self.bt_login.config(command=self.on_login_clicked)

        sign_bt = ImageTk.PhotoImage(Image.open('icons/tools/signup.png').resize((100, 45)))
        self.bt_sign = Button(self.f_login, image=sign_bt, cursor="hand2", bg=self.bg, bd=0, activebackground=self.bg)
        self.bt_sign.image = sign_bt
        self.bt_sign.grid(row=4, column=2, columnspan=2)
        self.bt_sign.config(command=self.on_signup_clicked)

        self.remember_var = IntVar()
        self.remember = Checkbutton(self.f_login, text='Remember me', font=('Arial', 12), bg=self.bg, onvalue=1,
                                    variable=self.remember_var, cursor='hand2', activebackground=self.bg)
        self.remember.grid(row=5, column=0, columnspan=2, padx=5, sticky='w')
        self.root.mainloop()

    def password_view(self):
        if self.e_password.cget('show') == '*':
            self.e_password.configure(show='')
            self.show_hide.configure(image=self.show_pass)
        else:
            self.e_password.configure(show='*')
            self.show_hide.configure(image=self.hide_pass)

    # FUNCTION THAT AUTHENTICATES THE USERNAME AND PASSWORD-------------------------------------------------------------
    def on_login_clicked(self):
        username = self.e_username.get()
        password = self.e_password.get()
        login_result = validate_login(username, password)

        if login_result == 'user not found':
            self.l_message.config(text=login_result)
        elif login_result == 'invalid password':
            self.l_message.config(text=login_result)
        else:
            from User import User
            from Static import Static
            from Functions import Functions
            Static.garbage_collect(self.f_login)
            self.f_login.grid_remove()
            if self.remember_var.get() == 1:
                Functions.remember(username, value=1)
            User(role=login_result, username=username, master=self.root)

    # HIDE THE LOGIN WINDOW AND CALL THE SIGNUP WINDOW------------------------------------------------------------------
    def on_signup_clicked(self):
        Static.garbage_collect(self.f_login)
        self.f_login.grid_remove()
        Signup(self.root, 'user')
