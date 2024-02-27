from tkinter import *
from tkcalendar import Calendar
from tkinter import messagebox


class Static:
    def __init__(self):
        self.bg = '#404040'
        self.bg2 = '#606060'
        self.fg = '#ffffff'

    @staticmethod
    def on_close(w1, w2):
        w1.config(state='normal')
        w2.destroy()

    @staticmethod
    def on_destroy(w1, w2):
        w1.destroy()
        w2.destroy()

    @staticmethod
    def garbage_collect(widget):
        children = widget.winfo_children()
        for child in children:
            for grandchild in child.winfo_children():
                grandchild.destroy()
            child.destroy()
        del children

    @staticmethod
    def scroll(widget, event):
        widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

    @staticmethod
    def final_scroll(widget, func, *_):
        widget.bind_all("<MouseWheel>", func)

    @staticmethod
    def stop_scroll(widget, *_):
        widget.unbind_all("<MouseWheel>")

    @staticmethod
    def update_scrollregion(widget, *_):
        widget.configure(scrollregion=widget.bbox('all'))

    @staticmethod
    def calculate_font_size(text, base_size=14, min_size=10):
        text_length = len(text)
        font = base_size
        if text_length > 3:
            for i in range(3, text_length):
                # Increase decrease rate every 2 characters
                if (i - 3) % 2 == 0:
                    font -= (i - 3) // 2 + 1

        # Ensure the font size does not fall below the minimum size
        font = max(font, min_size)

        return font

    @staticmethod
    def entry_ctrl_delete(event):
        widget = event.widget
        if isinstance(widget, Entry):
            entry_text = widget.get()
            parts = entry_text.split()
            parts_without_last = parts[:-1]
            new_string = ' '.join(parts_without_last)
            widget.delete(0, "end")
            widget.insert(0, new_string)
        elif isinstance(widget, Text):
            text_content = widget.get("1.0", "end-1c")
            parts = text_content.split()
            parts_without_last = parts[:-1]
            new_string = ' '.join(parts_without_last)
            widget.delete("1.0", "end")  # Clear the existing content
            widget.insert("1.0", new_string)
        else:
            pass
        return "break"

    @staticmethod
    def grab_date(master, widget):
        def on_confirm(c, w):
            w.config(text=c.get_date(), state='normal')
            top.destroy()

        master_x = master.winfo_rootx()
        master_y = master.winfo_rooty()
        top = Toplevel(master)
        top.update_idletasks()
        top_w = top.winfo_width()
        top_h = top.winfo_height()
        top_x = master_x
        top_y = master_y - top_h
        top.geometry(f'{top_w}x{top_h}+{top_x}+{top_y-30}')
        top.iconbitmap('icons/tools/wallet.ico')
        widget.config(state='disabled')
        cal = Calendar(top, selectmode="day", date_pattern='dd-mm-yyyy')
        # noinspection PyProtectedMember
        for i in cal._calendar:
            for j in i:
                j.bind("<Double-1>", lambda e, c=cal, w=widget: on_confirm(c, w))
        cal.pack()
        bt_confirm = Button(top, text='Confirm', bd=0, cursor='hand2', command=lambda: on_confirm(cal, widget))
        bt_confirm.pack(pady=3)
        top.protocol("WM_DELETE_WINDOW", lambda: Static.on_close(widget, top))

    @staticmethod
    def create_canvas(widget):
        canvas = Canvas()
        Static.garbage_collect(canvas)
        canvas = Canvas(widget, width=483, height=196, bd=0, highlightthickness=0, bg='#404040')
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar = Scrollbar(widget, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda event: event.widget.configure(scrollregion=event.widget.bbox('all')))
        frame = Frame(canvas, width=500, height=196, bg='#404040')
        canvas.create_window((0, 2), window=frame, anchor='nw')
        canvas.bind("<Enter>", lambda e: Static.final_scroll(e.widget,
                                                             lambda event: Static.scroll(e.widget, event), e))
        canvas.bind("<Leave>", lambda e: Static.stop_scroll(e.widget, e))
        Static.update_scrollregion(canvas)
        frame.bind('<Configure>', lambda event: Static.update_scrollregion(canvas))
        Static.garbage_collect(frame)
        return frame

    @staticmethod
    def validate_input_number(entry, master):
        input_str = entry.get().replace(',', '.')
        if ' ' in input_str:
            messagebox.showerror("Error", "Input should not contain spaces.", parent=master)
            return
        try:
            e_sum_value = float(input_str)
            return e_sum_value
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a number.", parent=master)
            return
