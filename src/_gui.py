

from   src._data_parser       import DataParser
from   src._data_processor    import DataProcessor
from   src._frequency_counter import FrequencyCounter

from   concurrent.futures     import ThreadPoolExecutor
import tkinter                as     tk


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Social-Media Trends")
        self.geometry("900x600")
        self.data_parser    = DataParser()
        self.data_processor = DataProcessor()
        self.topic_modeler  = FrequencyCounter()
        self.create_widgets()
    
    # элементы GUI
    def create_widgets(self):
        # отступ
        tk.Label(self, text="").pack(pady=10)
        # LABEL: path to TG
        self.tg_label = tk.Label(self, text="Path to tg.txt")
        self.tg_label.pack(pady=5)
        # ENTRY: path to TG
        self.tg_entry = tk.Entry(self, width=100)
        self.tg_entry.pack(pady=5)
        self.tg_entry.insert(0, "input/tg.txt")
        # LABEL: path to VK
        self.vk_label = tk.Label(self, text="Path to vk.txt")
        self.vk_label.pack(pady=5)
        # ENTRY: path to VK
        self.vk_entry = tk.Entry(self, width=100)
        self.vk_entry.pack(pady=5)
        self.vk_entry.insert(0, "input/vk.txt")
        # BUTTON
        self.run_button = tk.Button(self, text="Okay lets go", command=self.parsing)
        self.run_button.pack(pady=10)
        # вывод статуса и ошибок выполнения
        self.status_label = tk.Label(self, text="Ready to run ..")
        self.status_label.pack(pady=10)
    
    # метод для self.run_button
    def parsing(self):
        # отобразить статус работы
        self.status_label.config(text="Processing ..")
        self.update_idletasks()
        # получить чаты TG
        tg_path = self.tg_entry.get()
        try:
            with open(tg_path, "r", encoding="utf-8") as tg_file:
                tg_lines = tg_file.readlines()
            # @name
            self.data_parser.tg_chat_names = [f"@{line.strip()}" for line in tg_lines if line.strip()]
        except FileNotFoundError:
            self.status_label.config(text=self.status_label["text"] + f"\nFile not found: {tg_path}")
        except Exception as e:
            self.status_label.config(text=self.status_label["text"] + f"Error: {e}")
        # получить чаты VK
        vk_path = self.vk_entry.get()
        try:
            with open(vk_path, "r", encoding="utf-8") as vk_file:
                vk_lines = vk_file.readlines()
            # -1234567
            self.data_parser.vk_chat_ids = [f"-{line.strip()}" for line in vk_lines if line.strip()]
        except FileNotFoundError:
            self.status_label.config(text=self.status_label["text"] + f"\nFile not found: {vk_path}")
        except Exception as e:
            self.status_label.config(text=self.status_label["text"] + f"Error: {e}")
        # обновить статус GUI
        self.update_idletasks()
        #!#######################################################
        with ThreadPoolExecutor() as executor:
            tg_future = executor.submit(self.data_parser.tg_parse)
            vk_future = executor.submit(self.data_parser.vk)
        tg_data = tg_future.result()
        vk_data = vk_future.result()
        tg_data_processed = start_pool(tg_data)
        vk_data_processed = start_pool(vk_data)
        #!#######################################################
        # TODO _count_frequency.count()
        tg_result = self.topic_modeler.getWeights(tg_data_processed)
        vk_result = self.topic_modeler.getWeights(vk_data_processed)
        # TODO GUI output: tg_result_text
        tg_result_text = ""
        for topic in tg_result:
            tg_result_text += f'{topic}\n'
        with open(str("../output/tg.txt"), "w") as tg_output:
            tg_output.write(tg_result_text)
        # TODO GUI output: vk_result_text
        vk_result_text = ""
        for topic in vk_result:
            vk_result_text += f'{topic}\n'
        with open(str("../output/vk.txt"), "w") as vk_output:
            vk_output.write(vk_result_text)
        # отобразить статус работы
        self.status_label.config(text="Done")
        self.update_idletasks()
