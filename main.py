
import requests
#
# get (из requests):
#   выполнения GET-запросов (загрузка данных vk)
#

import asyncio
#
# call processes async 
#

from pyrogram import Client
#
# Client:
#   для взаимодействия с telegram API
#    (аутентификация, истории чатов)
#

from concurrent.futures import ThreadPoolExecutor
#
# ThreadPoolExecutor:
#   параллельное выполнение парсинга и обработки
#

from nltk.corpus import stopwords
# nltk.download('stopwords')
#
# "Natural Language Toolkit"
#
# stopwords:
#   список стоп-слов
#

from pymystem3 import Mystem
#
# Mystem:
#   приведение слов к начальной форме
#

import gensim
#
# TODO:
# LdaModel (из gensim.models):
#   создание и обучения тематической модели LDA
#

from gensim import corpora
#
# corpora (из gensim):
#   словарь (Dictionary) + корпус для LdaModel
#

import json
#
# получение токенов из input/tokens.json
#

import tkinter as tk
#
# tk (модуль tkinter):
#   создание GUI
#


#
# Отвечает за сбор 
#  текстовых данных vk и tg
#
class DataParser:

    #
    # tg_chat_names:     list[ каналы tg ], заполняется в ProgramInterface
    # vk_chat_ids:       list[ каналы vk ], заполняется в ProgramInterface
    # russian_stopwords:  set[ стоп-слов ]
    #
    def __init__(self):
        self.tg_chat_names     = []
        self.vk_chat_ids       = []
        self.russian_stopwords = set(stopwords.words("russian"))
        with open("input/tokens.json") as t:
            self.tokens = json.load(t)

    ##########################################   tg task  #########################################
    async def async_telegram_task(self):

        api_id    = self.tokens["tg"]["api_id"]
        api_hash  = self.tokens["tg"]["api_hash"]
        result    = []

        # TODO: возможная проблема:
        #  доступ раньше, чем ProgramInterface заполнит
        #   self.tg_chat_names и self.vk_chat_ids
        #
        async with Client('output/tg', api_id, api_hash) as client:
            for cid in self.tg_chat_names:
                chat = await client.get_chat(cid)  ## await
                # TODO: GUI:
                async for msg in client.get_chat_history(chat.id, limit=1000):
                    result.append(msg.caption or msg.text or '')
        return result

    ##########################################     tg     #########################################
    def telegram(self):
        return asyncio.run(self.async_telegram_task())

    ##########################################     vk     #########################################
    def vk(self):

        api       = self.tokens["vk"]["api"]
        version   = '5.131'
        amount    = 100  # TODO: GUI
        result    = []

        # TODO: async task for vk
        # TODO: возможная проблема:
        #  доступ раньше, чем ProgramInterface заполнит self.tg_chat_names, self.vk_chat_ids
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
# Отвечает за предварительную обработку текста.
#  Выполняет лемматизацию и удаление стоп-слов.
#
class TextProcessor:

    #
    def __init__(self, russian_stopwords):
        self.russian_stopwords = russian_stopwords

    #
    # text : исходный текст (str)
    #  -> обработанный текст, леммы без стоп-слов (str)
    #
    def get_words(self, text):
        if not text or not text.strip():
            return ""

        mystem = Mystem(mystem_bin="/usr/local/bin/mystem")

        try:
            # лемматизировать текст в нижнем регистре
            words = mystem.lemmatize(text.lower())
            # условие парсинга: убрать стоп-слова и пробелы:
            filtered = [w for w in words if w.strip() and w != " " and w not in self.russian_stopwords]
            # собрать в строку
            return " ".join(filtered)
        finally:
            # выполнить, независимо от возможных ошибок в try
            del mystem


#
# TODO
# Тематическое моделирование (LDA).
#  Принимает:  список обработанных текстов.
#  Возвращает: выделенные темы.
#
class TopicModeler:

    #
    # lines: list[str], список обработанных текстов
    #  -> list[tuple], список кортежей (тем) с весами и ключевыми словами
    #
    def getWeights(self, lines):
        # создать словарь:
        dictionary = corpora.Dictionary([x.split() for x in lines])

        # обучить модель:
        model = gensim.models.LdaModel
        lda_model = model(id2word=dictionary, num_topics=5, passes=50)

        # вернуть 3 главные темы
        return lda_model.print_topics(num_topics=3, num_words=4)


#
# Класс графического интерфейса.
#  Содержит: tk.Label, tk.Entry, tk.Button.
#   Обрабатывает: нажатие КНОПКИ.
#
class ProgramInterface(tk.Tk):

    #
    # инициализация GUI
    #
    def __init__(self, data_parser, text_processor, topic_modeler):

        # инициализировать родительский класс (tk.Tk)
        super().__init__()

        self.title("Social-Media Trends")     # заголовок окна
        self.geometry("900x600")              # размер окна

        self.data_parser    = data_parser     # экземпляр DataParser
        self.text_processor = text_processor  # экземпляр TextProcessor
        self.topic_modeler  = topic_modeler   # экземпляр TopicModeler

        # запустить создание виджетов
        self.create_widgets()

    #
    # элементы GUI
    #
    def create_widgets(self):

        # отступ
        tk.Label(self, text="").pack(pady=10)

        # label: path to TG
        self.tg_label = tk.Label(self, text="Path to tg.txt")
        self.tg_label.pack(pady=5)

        # path to TG
        self.tg_entry = tk.Entry(self, width=100)
        self.tg_entry.pack(pady=5)
        
        # label: path to VK
        self.vk_label = tk.Label(self, text="Path to vk.txt")
        self.vk_label.pack(pady=5)

        # path to VK
        self.vk_entry = tk.Entry(self, width=100)
        self.vk_entry.pack(pady=5)

        # КНОПКА
        self.process_button = tk.Button(self, text="Okay lets go", command=self.parsing)
        self.process_button.pack(pady=10)

        # метка для вывода результатов
        self.status_label = tk.Label(self, text="Ready to run ..")
        self.status_label.pack(pady=10)

    #
    # метод обратного вызова 
    #  для КНОПКИ
    #
    def parsing(self):

        # TODO отобразить статус работы
        self.status_label.config(text="Processing ..")

        # получить чаты TG
        tg_path = self.tg_entry.get()
        try:
            with open(tg_path, "r", encoding="utf-8") as tg_file:
                tg_lines = tg_file.readlines()
            #####################
            data_parser.tg_chat_names = [f"@{line.strip()}" for line in tg_lines if line.strip()]
            #####################
        except FileNotFoundError:
            self.status_label.config(text=self.status_label["text"] + f"\nFile not found: {tg_path}")
        except Exception as e:
            self.status_label.config(text=self.status_label["text"] + f"Error: {e}")

        # получить чаты VK
        vk_path = self.vk_entry.get()
        try:
            with open(vk_path, "r", encoding="utf-8") as vk_file:
                vk_lines = vk_file.readlines()
            #####################
            data_parser.vk_chat_ids = [f"-{line.strip()}" for line in vk_lines if line.strip()]
            #####################
        except FileNotFoundError:
            self.status_label.config(text=self.status_label["text"] + f"\nFile not found: {vk_path}")
        except Exception as e:
            self.status_label.config(text=self.status_label["text"] + f"Error: {e}")

        #####################
        self.update_idletasks()
        # self.update()


        # параллельно спарсить vk + tg
        with ThreadPoolExecutor() as executor:
            vk_result = executor.submit(self.data_parser.vk)
            tg_result = executor.submit(self.data_parser.telegram)

        # параллельно обработать полученные тексты
        with ThreadPoolExecutor() as executor:
            processed_data_parallel_vk = list(executor.map(self.text_processor.get_words, vk_result.result()))
            processed_data_parallel_tg = list(executor.map(self.text_processor.get_words, tg_result.result()))

        # TODO частотность тем: vk
        vk_result = self.topic_modeler.getWeights(processed_data_parallel_vk)

        # TODO частотность тем: tg
        tg_result = self.topic_modeler.getWeights(processed_data_parallel_tg)


        # вывод тем tg
        tg_result_text = ""
        for topic in tg_result:
            tg_result_text += f'{topic}\n'
        #
        # TODO вывод в поле GUI
        #
        # -> output/tg.txt
        with open("output/tg.txt", "w") as tg_output:
            tg_output.write(tg_result_text)

        # вывод тем vk
        vk_result_text = ""
        for topic in vk_result:
            vk_result_text += f'{topic}\n'
        #
        # TODO вывод в поле GUI
        #
        # -> output/vk.txt
        with open("output/vk.txt", "w") as vk_output:
            vk_output.write(vk_result_text)

        # отобразить статус работы
        self.status_label.config(text="Done")


if __name__ == '__main__':

    # Поля: tg_chat_names, vk_chat_ids
    #  заполняются после нажатия кнопки в program_interface
    data_parser = DataParser()

    text_processor = TextProcessor(data_parser.russian_stopwords)

    topic_modeler = TopicModeler()

    program_interface = ProgramInterface(data_parser, text_processor, topic_modeler)
    program_interface.mainloop()
