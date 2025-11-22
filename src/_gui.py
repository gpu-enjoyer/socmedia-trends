
import threading
import asyncio
import time

import tkinter        as     tk
from   tkinter.ttk    import Treeview, Style
from   os.path        import exists, splitext, abspath

from   src._parser_tg import ParserTg
from   src._parser_vk import ParserVk
from   src._processor import Processor


class GUI:
    def __init__(self, disp: tk.Tk):
        self.parser_tg = ParserTg()
        self.parser_vk = ParserVk()
        self.processor = Processor()
        self.create_widgets(disp)
        self.config_grid()
        if self.DISP:
            self.DISP.update_idletasks()
            self.DISP.update()

    def config_grid(self):
        # DISP
        self.DISP.grid_columnconfigure(0, weight=1)
        self.DISP.grid_rowconfigure(0, weight=0,  minsize=70)
        self.DISP.grid_rowconfigure(1, weight=10, minsize=100)
        self.DISP.grid_rowconfigure(2, weight=13, minsize=130)
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
        self.ROW_2.grid_columnconfigure(0, weight=1) # TBL_20
        self.ROW_2.grid_columnconfigure(1, weight=1) # TBL_21

    def create_widgets(self, disp: tk.Tk):
        self.default_path = "./InpOut/input.json"
        ### DISP ###
        self.DISP = disp
        self.DISP.title("Soc-Media Trends")
        self.DISP.geometry("900x600")
        padx=10
        ### ROW_0 ###
        self.ROW_0 = tk.Frame(self.DISP)
        self.ROW_0.grid(row=0, column=0, padx=padx, pady=(10,10), sticky='nsew')
        ## 00
        B_00 = tk.Frame(self.ROW_0, borderwidth=3, relief=tk.SUNKEN, height=1)
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
        self.BTN_01 = tk.Button(B_01, text="Load", command=self.clk_BTN_01)
        self.BTN_01.pack(fill='both', expand=True)
        ## 02
        B_02 = tk.Frame(self.ROW_0, borderwidth=3, relief=tk.SUNKEN)
        B_02.grid(row=0, column=2, sticky='nsew')
        self.BTN_02 = tk.Button(B_02, text="Start", command=self.clk_BTN_02)
        self.BTN_02.pack(fill='both', expand=True)
        ### ROW_1 ###
        self.ROW_1 = tk.Frame(self.DISP)
        self.ROW_1.grid(row=1, column=0, padx=padx, pady=(0,10), sticky='nsew')
        B_1 = tk.Frame(self.ROW_1, borderwidth=3, relief=tk.SUNKEN)
        B_1.grid(row=0, column=0, sticky='nsew')
        self.LOG_1 = tk.Text(B_1, state='disabled', height=1, padx=10, relief=tk.FLAT)
        self.LOG_1.pack(side='left', fill='both', expand=True)
        self.LOG_1.bind('<Button>', lambda e: self.LOG_1.focus_set())
        ### ROW_2 ###
        self.ROW_2 = tk.Frame(self.DISP)
        self.ROW_2.grid(row=2, column=0, padx=padx, pady=(0,10), sticky='nsew')
        TBLS_style = Style() #!
        TBLS_style.configure("Treeview", padding=(10,5), rowheight=25)
        #
        B_20 = tk.Frame(self.ROW_2, borderwidth=3, relief=tk.SUNKEN)
        B_20.grid(row=0, column=0, sticky='nsew')
        self.TBL_20 = Treeview(B_20, height=1)
        self.TBL_20["columns"] = ("freq", "word")
        self.TBL_20['show'] = "headings"
        self.TBL_20.heading("freq", text="Freq.", anchor="center")
        self.TBL_20.heading("word", text="Word", anchor="center")
        self.TBL_20.column("freq", anchor="center")
        self.TBL_20.column("word", anchor="center")
        self.TBL_20.pack(fill="both", expand=True)
        #
        B_21 = tk.Frame(self.ROW_2, borderwidth=3, relief=tk.SUNKEN)
        B_21.grid(row=0, column=1, sticky='nsew')
        self.TBL_21 = Treeview(B_21, height=1)
        self.TBL_21["columns"] = ("freq", "word")
        self.TBL_21['show'] = "headings"
        self.TBL_21.heading("freq", text="Freq.", anchor="center")
        self.TBL_21.heading("word", text="Word", anchor="center")
        self.TBL_21.column("freq", anchor="center")
        self.TBL_21.column("word", anchor="center")
        self.TBL_21.pack(fill="both", expand=True)

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

    def log(self, msg: str | list[str]):
        self.LOG_1.config(state='normal') 
        if isinstance(msg, str):
            self.LOG_1.insert('end', msg+'\n')
        else:
            for line in msg:
                self.LOG_1.insert('end', line+'\n')
        self.LOG_1.see('end')
        self.LOG_1.config(state='disabled')

    def clk_BTN_01(self):
        val = self.ENT_00.get()
        if not self.check_path(val):
            self.log("Input expected: path to JSON")
            return
        val = abspath(val)
        #
        self.log(f"Loading Tg fields: \"{val}\" ...")
        self.parser_tg.set_fields(val)
        self.log(self.parser_tg.log_info)
        if self.parser_tg.is_prepared:
            self.log("GUI.parser_tg: prepared")
        else:
            self.log("GUI.parser_tg not prepared!\n Fix JSON")
        #
        self.log(f"Loading Vk fields: \"{val}\" ...")
        self.parser_vk.set_fields(val)
        self.log(self.parser_vk.log_info)
        if self.parser_vk.is_prepared:
            self.log("GUI.parser_vk: prepared")
        else:
            self.log("GUI.parser_vk not prepared!\n Fix JSON")

    def clk_BTN_02(self):
        self.BTN_01.config(state='disabled')
        self.BTN_02.config(state='disabled')
        #
        if not self.parser_tg.is_prepared:
            self.log("GUI.parser_tg not prepared - skip")
        else: 
            self.parser_tg.log_info = []
            self.processor.log_info = []
            threading.Thread(target=self.run_workflow_tg).start()
        #!
        if not self.parser_vk.is_prepared:
            self.log("GUI.parser_vk not prepared - skip")
        else: 
            self.parser_vk.log_info = []
            self.processor.log_info = []
            threading.Thread(target=self.run_workflow_vk).start()
        #
        self.BTN_01.config(state='normal')
        self.BTN_02.config(state='normal')

    def run_workflow_tg(self):
        self.log("=== Tg Pipeline Started ===")
        # 1. PARSING
        self.log("1. Tg parsing started ...")
        time_1 = time.time() #!
        raw_data = asyncio.run(self.parser_tg.parse())
        time_pars = time.time() - time_1 #!
        self.log(self.parser_tg.log_info)
        self.log(f"   Tg parsing done: {len(raw_data)} messages by {time_pars:.1f}s")
        # 2. PROCESSING
        self.log("2. Tg processing started ...")
        if not raw_data:
            self.log("   Tg: no data to process")
            self.log("=== Tg Pipeline Finished ===")
            return
        time_2 = time.time() #!
        proc_data = self.processor.start_pool(raw_data)
        #  : Counter
        proc_data = proc_data.most_common()
        #  : list[tuple[str, int]]
        idx = old_len = len(proc_data)
        for t in proc_data:
            if t[1] <= 2:
                idx = proc_data.index(t)
                break
        proc_data = proc_data[:idx]
        time_proc = time.time() - time_2 #!
        self.log(self.processor.log_info)
        self.log(f"   Tg processing done: {len(proc_data)}/{old_len} unique words by {time_proc:.1f}s")
        # 3. SAVING
        self.log("3. Tg saving started ...")
        #
        for (word,freq) in proc_data:
            self.TBL_20.insert("", "end", values=(freq, word))
        #
        rawdata_path = str(self.parser_tg.dir_path + "/tg_raw_data.csv")
        try:
            with open(rawdata_path, 'w', encoding='utf-8') as f:
                for s in raw_data: f.write(s + '\n')
            self.log(f"   Tg saved to: {rawdata_path}")
        except Exception as e:
            self.log(f"   Tg error saving {rawdata_path}: {e}")
        #
        procdata_path = str(self.parser_tg.dir_path + "/tg_proc_data.csv")
        try:
            with open(procdata_path, 'w', encoding='utf-8') as f:
                f.write("freq,word\n")
                for (word,freq) in proc_data:
                    f.write(f"{freq},{word}\n")
            self.log(f"   Tg saved to: {procdata_path}")
        except Exception as e:
            self.log(f"   Tg error saving {procdata_path}: {e}")
        self.log("=== Tg Pipeline Finished ===")

    def run_workflow_vk(self):
        self.log("=== Vk Pipeline Started ===")
        # 1. PARSING
        self.log("1. Vk parsing started ...")
        time_1 = time.time() #!
        raw_data = asyncio.run(self.parser_vk.parse())
        time_pars = time.time() - time_1 #!
        self.log(self.parser_vk.log_info)
        self.log(f"   Vk parsing done: {len(raw_data)} messages by {time_pars:.1f}s")
        # 2. PROCESSING
        self.log("2. Vk processing started ...")
        if not raw_data:
            self.log("   Vk no data to process")
            self.log("=== Vk Pipeline Finished ===")
            return
        time_2 = time.time() #!
        proc_data = self.processor.start_pool(raw_data)
        #  : Counter
        proc_data = proc_data.most_common()
        #  : list[tuple[str, int]]
        idx = old_len = len(proc_data)
        for t in proc_data:
            if t[1] <= 2:
                idx = proc_data.index(t)
                break
        proc_data = proc_data[:idx]
        time_proc = time.time() - time_2 #!
        self.log(self.processor.log_info)
        self.log(f"   Vk processing done: {len(proc_data)}/{old_len} unique words by {time_proc:.1f}s")
        # 3. SAVING
        self.log("3. Vk saving started ...")
        #
        for (word,freq) in proc_data:
            self.TBL_21.insert("", "end", values=(freq, word))
        #
        rawdata_path = str(self.parser_vk.dir_path + "/vk_raw_data.csv")
        try:
            with open(rawdata_path, 'w', encoding='utf-8') as f:
                for s in raw_data: f.write(s + '\n')
            self.log(f"   Vk saved to: {rawdata_path}")
        except Exception as e:
            self.log(f"   Vk error saving {rawdata_path}: {e}")
        #
        procdata_path = str(self.parser_vk.dir_path + "/vk_proc_data.csv")
        try:
            with open(procdata_path, 'w', encoding='utf-8') as f:
                f.write("freq,word\n")
                for (word,freq) in proc_data:
                    f.write(f"{freq},{word}\n")
            self.log(f"   Vk saved to: {procdata_path}")
        except Exception as e:
            self.log(f"   Vk error saving {procdata_path}: {e}")
        self.log("=== Vk Pipeline Finished ===")
