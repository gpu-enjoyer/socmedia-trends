
import tkinter         as     tk
from   tkinter.ttk     import Treeview, Style
from   os.path         import exists, splitext, abspath

from    src._parser_tg import ParserTg

class GUI:
    def __init__(self, disp: tk.Tk):
        self.create_widgets(disp)
        self.config_grid()

    def config_grid(self):
        # DISP
        self.DISP.grid_columnconfigure(0, weight=1)
        self.DISP.grid_rowconfigure(0, weight=1, minsize=80)
        self.DISP.grid_rowconfigure(1, weight=2, minsize=120)
        self.DISP.grid_rowconfigure(2, weight=2, minsize=120)
        # ROW_0
        self.ROW_0.grid_rowconfigure(0, weight=1)
        self.ROW_0.grid_columnconfigure(0, weight=7) # ENT_00
        self.ROW_0.grid_columnconfigure(1, weight=2) # BTN_01
        self.ROW_0.grid_columnconfigure(2, weight=2) # BTN_02
        # ROW_1
        self.ROW_1.grid_rowconfigure(0, weight=1)
        self.ROW_1.grid_columnconfigure(0, weight=1)
        # ROW_2
        self.ROW_2.grid_rowconfigure(0, weight=1)
        self.ROW_2.grid_columnconfigure(0, weight=1)

    def create_widgets(self, disp: tk.Tk):
        self.default_path = "./input.json"
        ### DISP ###
        self.DISP = disp
        self.DISP.title("Soc-Media Trends")
        self.DISP.geometry("700x500")
        ### ROW_0 ###
        self.ROW_0 = tk.Frame(self.DISP)
        self.ROW_0.grid(row=0, column=0, padx=30, pady=(10,10), sticky='nsew')
        ## 00
        B_00 = tk.Frame(self.ROW_0, borderwidth=3, relief=tk.SUNKEN)
        B_00.grid(row=0, column=0, sticky='nsew')
        self.ENT_00 = tk.Entry(B_00, borderwidth=10, relief=tk.FLAT)
        self.ENT_00.insert(0, self.default_path)
        self.ENT_00.pack(fill='both', expand=True)
        self.ENT_00.bind('<Map>', self.out_ENT_00)
        self.ENT_00.bind('<FocusIn>',  self.on_ENT_00 )
        self.ENT_00.bind('<FocusOut>', self.out_ENT_00)
        ## 01
        B_01 = tk.Frame(self.ROW_0, borderwidth=3, relief=tk.SUNKEN)
        B_01.grid(row=0, column=1, sticky='nsew')
        # !!!
        self.BTN_01 = tk.Button(B_01, text="Load", command=self.clk_BTN_01)
        self.BTN_01.pack(fill='both', expand=True)
        ## 02
        B_02 = tk.Frame(self.ROW_0, borderwidth=3, relief=tk.SUNKEN)
        B_02.grid(row=0, column=2, sticky='nsew')
        self.BTN_02 = tk.Button(B_02, text="Start", command=self.clk_BTN_02)
        self.BTN_02.pack(fill='both', expand=True)
        ### ROW_1 ###
        self.ROW_1 = tk.Frame(self.DISP)
        self.ROW_1.grid(row=1, column=0, padx=30, pady=(0,10), sticky='nsew')
        B_1 = tk.Frame(self.ROW_1, borderwidth=3, relief=tk.SUNKEN)
        B_1.grid(row=0, column=0, sticky='nsew')
        self.LOG_1 = tk.Text(B_1, state='disabled', height=6)
        self.LOG_1.pack(side='left', fill='both', expand=True)
        self.LOG_1.bind('<Button>', lambda e: self.LOG_1.focus_set())
        ### ROW_2 ###
        self.ROW_2 = tk.Frame(self.DISP)
        self.ROW_2.grid(row=2, column=0, padx=30, pady=(0,10), sticky='nsew')
        B_2 = tk.Frame(self.ROW_2, borderwidth=3, relief=tk.SUNKEN)
        B_2.grid(row=0, column=0, sticky='nsew')
        TBL_2_style = Style()
        TBL_2_style.configure("Treeview", padding=(10,5), rowheight=25)
        TBL_2 = Treeview(B_2, height=6)
        TBL_2["columns"] = ("freq", "word")
        TBL_2['show'] = "headings"
        TBL_2.heading("freq", text="Frequency", anchor="center")
        TBL_2.heading("word", text="Word", anchor="center")
        TBL_2.column("freq", anchor="center", )
        TBL_2.column("word", anchor="center", )
        TBL_2.insert("", "end", values=(10, "Привет"))
        TBL_2.insert("", "end", values=(3, "Пока"))
        TBL_2.pack(fill="both", expand=True)

    def check_path(self, p: str) -> bool:
        if exists(p):
            name, ext = splitext(p)
            if (ext == ".json"):
                return True
        return False

    def on_ENT_00(self, event):
        self.ENT_00.selection_clear()
        self.ENT_00.configure(background='white')

    def out_ENT_00(self, event):
        val = self.ENT_00.get()
        if not val:
            val = self.default_path
            self.ENT_00.insert(0, val)
        if self.check_path(val):
            self.ENT_00.configure(background='light green')
        else:
            self.ENT_00.configure(background='light coral')

    def log(self, msg):
        self.LOG_1.config(state='normal') 
        if isinstance(msg, str):
            self.LOG_1.insert('end', msg+'\n')
        elif isinstance(msg, list):
            for line in msg:
                self.LOG_1.insert('end', line+'\n')
        else:
            self.LOG_1.insert('end', "Unknown type of log message!\n")
        self.LOG_1.see('end')
        self.LOG_1.config(state='disabled')

    def clk_BTN_01(self):
        val = self.ENT_00.get()
        if not self.check_path(val):
            self.log("Input: path to \"*.json\"")
            return
        self.log(f"Loading: \"{val}\" ...")
        val = abspath(val)
        self.parser_tg = ParserTg(val)
        self.log(self.parser_tg.log)

    # todo: ParserTg.parse()
    def clk_BTN_02(self):
        # self.parser_tg.parse()
        pass
