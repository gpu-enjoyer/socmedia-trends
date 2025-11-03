
from . import text_processor
#
# start_pool(texts)
#

from concurrent.futures import ThreadPoolExecutor
#
# Используется для вызова
#  DataParser.tg()
#  DataParser.vk()
#
# TODO
#  Почему именно это?
#

import requests
#
# requests.get():
#  выполнения GET-запросов vk
#
# TODO
#  Возможно, vk api подойдет лучше?
#

import asyncio
#
#  get async func result?
#

from pyrogram import Client
#
# Client:
#  для взаимодействия с Telegram API
#   (аутентификация, истории чатов)
#

import gensim
#
# gensim.models.LdaModel
#  создание и обучения тематической модели LDA
#
# TODO
#  обычная frequency
#

from gensim import corpora
#
# TODO
#  remove from project
#
# gensim.corpora:
#  словарь и корпус для LdaModel?
#

import json
#
# Получение токенов 
#  из ../input/tokens.json
#

import tkinter as tk
#
#  Создание GUI
#

from pathlib import Path
project_dir = Path(__file__).resolve().parent.parent
#
# корень проекта
#


#
# Отвечает за сбор текстов tg + vk
#
class DataParser:

    #
    def __init__(self):

        self.tg_chat_names  = []  # заполняется в ProgramInterface
        self.vk_chat_ids    = []  # заполняется в ProgramInterface
        self.tokens         = {}

        # tokens
        try:
            tokens_path = "input/tokens.json"
            with open(tokens_path) as t:
                self.tokens = json.load(t)
        except FileNotFoundError:
            print(f"ERROR: {tokens_path} not found")
        except json.JSONDecodeError:
            print(f"ERROR: {tokens_path} json decode error")

    # TODO: improve
    ##################################   tg task  ##################################
    async def async_tg_task(self, api_id, api_hash):

        result    = []

        #
        # TODO
        #  improve
        #
        # TODO
        #  Проверить, возможен ли доступ прежде,
        #   чем ProgramInterface заполнит
        #    self.tg_chat_names и self.vk_chat_ids
        #
        # output/tg.session
        #
        async with Client(str(project_dir/"output/tg"), api_id, api_hash) as client:
            for cid in self.tg_chat_names:
                chat = await client.get_chat(cid)
                async for msg in client.get_chat_history(chat.id, limit=1000):
                    result.append(msg.caption or msg.text or '')
        return result

    ##################################   tg       ##################################
    def tg(self):
        api_id    = self.tokens["tg"]["api_id"]
        api_hash  = self.tokens["tg"]["api_hash"]
        return asyncio.run(self.async_tg_task(api_id, api_hash))

    # TODO
    ##################################   vk task  ##################################

    ##################################   vk       ##################################
    def vk(self):

        api       = self.tokens["vk"]["api"]
        version   = '5.131'
        amount    = 1000  # TODO
        result    = []

        #
        # TODO: async_vk_task
        #
        # TODO: возможна проблема:
        #  доступ раньше, чем ProgramInterface заполнит
        #   self.tg_chat_names, self.vk_chat_ids
        #
        for cid in self.vk_chat_ids:
            response = requests.get(
                'https://api.vk.com/method/wall.get',
                params={
                    'access_token': api,
                    'v': version,
                    'owner_id': int(cid),  ## int (?!) там строки с минусом в начале
                    'count': amount}
            ).json()
            for item in response['response']['items']:
                result.append(item.get('text', ''))

        return result


#
# TODO
#  frequency_counter.py
#
class TopicModeler:
    def getWeights(self, lines):
        # создать словарь
        dictionary = corpora.Dictionary([x.split() for x in lines])
        # обучить модель
        model = gensim.models.LdaModel
        lda_model = model(id2word=dictionary, num_topics=5, passes=50)
        # вернуть главные темы
        return lda_model.print_topics(num_topics=5, num_words=3)


#
# Класс графического интерфейса.
#  Содержит: tk.Label, tk.Entry, tk.Button.
#   Обрабатывает: нажатие КНОПКИ.
#
class ProgramInterface(tk.Tk):

    #
    # TODO
    #  background-color: #171421
    #  widgets-color:    #D0CFCC
    #  serif:            monospace
    #
    # TODO
    #  вывод в поле с текстом:
    #   можно:  копировать, скроллить
    #   нельзя: редактировать
    #
    # TODO
    #  адаптивная разметка GUI
    #
    # TODO
    #  if is_resize: GUI_window.resize()
    #
    # TODO
    #  self.prepare_button = tk.Button(self, text="Prepare", command=self.prepare)
    #   забрать часть ответственности self.parsing
    #    на этапе проверки корректности окружения
    #
    # TODO
    #  получать логи из вызываемых модулей
    #

    # инициализация GUI
    def __init__(self, data_parser, topic_modeler):

        # инициализировать родительский класс (tk.Tk)
        super().__init__()

        self.title("Social-Media Trends")     # заголовок окна
        self.geometry("900x600")              # размер окна

        self.data_parser    = data_parser     # экземпляр DataParser
        self.topic_modeler  = topic_modeler   # экземпляр TopicModeler

        ### self.text_processor = text_processor
        ###  экземпляр TextProcessor

        # запустить создание виджетов
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
            data_parser.tg_chat_names = [f"@{line.strip()}" for line in tg_lines if line.strip()]
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
            data_parser.vk_chat_ids = [f"-{line.strip()}" for line in vk_lines if line.strip()]
        except FileNotFoundError:
            self.status_label.config(text=self.status_label["text"] + f"\nFile not found: {vk_path}")
        except Exception as e:
            self.status_label.config(text=self.status_label["text"] + f"Error: {e}")

        # обновить статус GUI
        self.update_idletasks()

        # парсинг tg + vk
        with ThreadPoolExecutor() as executor:
            tg_future = executor.submit(self.data_parser.tg)
            vk_future = executor.submit(self.data_parser.vk)

        tg_data = tg_future.result()
        vk_data = vk_future.result()

        tg_data_processed = text_processor.start_pool(tg_data)
        vk_data_processed = text_processor.start_pool(vk_data)

        # TODO: frequency
        tg_result = self.topic_modeler.getWeights(tg_data_processed)
        vk_result = self.topic_modeler.getWeights(vk_data_processed)

        # TODO
        #  GUI: output: tg_result_text
        tg_result_text = ""
        for topic in tg_result:
            tg_result_text += f'{topic}\n'
        with open(str(project_dir/"output/tg.txt"), "w") as tg_output:
            tg_output.write(tg_result_text)

        # TODO
        #  GUI: output: vk_result_text
        vk_result_text = ""
        for topic in vk_result:
            vk_result_text += f'{topic}\n'
        with open(str(project_dir/"output/vk.txt"), "w") as vk_output:
            vk_output.write(vk_result_text)

        # отобразить статус работы
        self.status_label.config(text="Done")
        self.update_idletasks()


if __name__ == "__main__":

    #
    # Поля: tg_chat_names, vk_chat_ids
    #  заполняются в program_interface
    #   после нажатия КНОПКИ запуска
    #
    data_parser       = DataParser()

    topic_modeler     = TopicModeler()

    program_interface = ProgramInterface(data_parser, topic_modeler)
    program_interface.mainloop()
