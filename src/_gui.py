
from   pathlib import Path
import tkinter as     tk


class GUI:
    def __init__(self, disp: tk.Tk):
        self.create_widgets(disp)
        self.config_grid()
    
    def create_widgets(self, disp: tk.Tk):
        self.default_path = "./input.json"
        ### DISP ###
        self.DISP = disp
        self.DISP.title("Soc-Media Trends")
        self.DISP.geometry("700x150")
        ### ROW_0 ###
        ROW_0 = tk.Frame(self.DISP)
        ROW_0.grid(row=0, column=0, padx=30, pady=(10, 5), sticky='nsew')
        #
        BRD_0 = tk.Frame(ROW_0, borderwidth=3, relief=tk.SUNKEN)
        BRD_0.pack(fill='both', expand=True)
        #
        self.ENT_0 = tk.Entry(BRD_0, borderwidth=10, relief=tk.FLAT)
        self.ENT_0.insert(0, self.default_path)
        self.ENT_0.pack(fill='both', expand=True)
        #
        self.ENT_0.bind('<FocusIn>',  self.on_ENT_0 )
        self.ENT_0.bind('<FocusOut>', self.out_ENT_0)
        ### ROW_1 ###
        ROW_1 = tk.Frame(self.DISP)
        ROW_1.grid(row=1, column=0, padx=30, pady=( 5,15), sticky='nsew')
        #
        BRD_1 = tk.Frame(ROW_1, borderwidth=3, relief=tk.SUNKEN)
        BRD_1.pack(fill='both', expand=True)
        #
        self.BTN_1 = tk.Button(BRD_1, text="Start", command=self.clk_BTN_1)
        self.BTN_1.pack(fill='both', expand=True)

    def config_grid(self):
        self.DISP.grid_columnconfigure(0, weight=1)
        self.DISP.grid_rowconfigure(0, weight=1)
        self.DISP.grid_rowconfigure(1, weight=1)

    def check_path(self, p: str) -> bool:
        if Path(p).exists(): return True
        return False

    def on_ENT_0(self, event):
        val = self.ENT_0.get()
        if self.ENT_0.get() == self.default_path:
            self.ENT_0.delete(0, 'end')
        self.ENT_0.selection_clear()
        self.ENT_0.configure(background='light gray')

    def out_ENT_0(self, event):
        val = self.ENT_0.get()
        if not val:
            self.ENT_0.insert(0, self.default_path)
            self.ENT_0.configure(background='light gray')
            return
        if self.check_path(val):
            self.ENT_0.configure(background='light green')
        else:
            self.ENT_0.configure(background='light coral')

    def clk_BTN_1(self, event):
        pass
