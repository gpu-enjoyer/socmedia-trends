import requests
#
# get (из requests):
#   выполнения GET-запросов (загрузка данных VK)
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
# LdaModel (из gensim.models):
#   создание и обучения тематической модели LDA
#   ("латентное распределение Дирихле")
#
from gensim import corpora
#
# corpora (из gensim):
#   словарь (Dictionary) + корпус для LdaModel
#
import tkinter as tk
#
# tk (модуль tkinter):
#   создание GUI
#

import json

#
# Отвечает за сбор текстовых данных vk и telegram. 
#  Инициализирует Mystem (приведение слов к начальной форме)
#   и стоп-слова для передачи в TextProcessor.
#
class DataParser:

    # russian_stopwords: set, набор стоп-слов
    def __init__(self):
        self.russian_stopwords = set(stopwords.words("russian"))

    with open("input/tokens.json") as t:
        tokens = json.load(t)

    ##########################################   tg task  #########################################
    async def async_telegram_task(self):

        api_id    = self.tokens["tg"]["api_id"]     # !!! !!! !!!
        api_hash  = self.tokens["tg"]["api_hash"]   # !!! !!! !!!
        channels  = []
        result    = []

        with open('input/tg.txt') as file:
            # += ID канала:
            channels.append(file.readline().strip())

        # 'async with' для асинхронного клиента:
        async with Client('output/tg', api_id, api_hash) as client:  # !!! !!! !!!
            for cid in channels:
                # 'await' для получения чата:
                chat = await client.get_chat(cid)
                
                # 'async for' для асинхронного генератора:
                async for msg in client.get_chat_history(chat.id, limit=1000):
                    # += текст поста или += ничего (если всё):
                    result.append(msg.caption or msg.text or '')
        return result

    ##########################################     tg     #########################################
    def telegram(self):
        # создать и запустить цикл событий:
        return asyncio.run(self.async_telegram_task())

    ##########################################     vk     #########################################
    def vk(self):

        api       = self.tokens["vk"]["api"]  # !!! !!! !!!
        version   = '5.131'
        amount    = 100                  # !!! !!! !!!
        channels  = []
        result    = []
        
        with open('input/vk.txt') as file:                     # !!! !!! !!!
            # прочитать ID из файла
            channels.append(file.readline().strip())

        for id in channels:
            # GET-запрос для vk:
            response = requests.get(
                'https://api.vk.com/method/wall.get',
                params={'access_token': api, 'v': version, 'owner_id': int(id), 'count': amount}
            ).json()

            # проходим по каждому посту:
            for item in response['response']['items']:
                # взять значение поля text, иначе - пустая строка
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
# Тематическое моделирование (LDA).
#  Принимает:  список обработанных текстов.
#  Возвращает: выделенные темы.
#
class TopicModeler:   # !!! !!! !!!

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
#  Содержит виджеты (кнопки, метки) и
#   обрабатывает нажатия кнопок.
#
class ProgramInterface(tk.Tk):

    #
    def __init__(self, data_parser, text_processor, topic_modeler):
        super().__init__()  # инициализировать родительский класс (tk.Tk)

        self.title("Soc-Media Trends")  # заголовок окна
        self.geometry("500x300")           # размер окна

        self.data_parser = data_parser        # экземпляр DataParser
        self.text_processor = text_processor  # экземпляр TextProcessor
        self.topic_modeler = topic_modeler    # экземпляр TopicModeler

        self.create_widgets()  # запустить создание виджетов

    #
    def create_widgets(self):
        # главный заголовок
        self.main_label = tk.Label(self, text="Soc-Media Trends", font=("Helvetica", 16))
        self.main_label.pack(pady=20)

        # кнопка
        self.process_button = tk.Button(self, text="Okay lets go", command=self.parsing)
        self.process_button.pack(pady=10)

        # метка для вывода результатов
        self.result_label = tk.Label(self, text="")
        self.result_label.pack(pady=10)

    #
    # -> None (метод обратного вызова для кнопки)
    #
    def parsing(self):
        self.result_label.config(text="Processing.. ")  # обновить статус в UI

        # параллельно спарсить vk + tg
        with ThreadPoolExecutor() as executor:
            vk_result = executor.submit(self.data_parser.vk)
            tg_result = executor.submit(self.data_parser.telegram)

        # параллельно обработать полученные тексты
        with ThreadPoolExecutor() as executor:
            processed_data_parallel_vk = list(executor.map(self.text_processor.get_words, vk_result.result()))
            processed_data_parallel_tg = list(executor.map(self.text_processor.get_words, tg_result.result()))

        # получить темы vk
        vk_results = self.topic_modeler.getWeights(processed_data_parallel_vk)

        # получить темы tg
        tg_results = self.topic_modeler.getWeights(processed_data_parallel_tg)

        # форматирование тем для вывода в GUI
        result_text = ''
        result_text += f'VK themes:\n'
        for topic in vk_results:
            result_text += f'{topic}\n'
        result_text += f'\n\nTelegram themes:\n'
        for topic in tg_results:
            result_text += f'{topic}\n'

        # записать в файл темы vk 
        with open('output/vk_results.txt', 'a') as topics_vk:
            for topic in vk_results:
                topics_vk.write(str(topic) + '\n')

        # записать в файл темы tg
        with open('output/tg_results.txt', 'a') as topics_tg:
            for topic in tg_results:
                topics_tg.write(str(topic) + '\n')

        # отобразить статус выполнения
        self.result_label.config(text=result_text)


if __name__ == '__main__':
    data_parser = DataParser()
    text_processor = TextProcessor(data_parser.russian_stopwords)
    topic_modeler = TopicModeler()
    program_interface = ProgramInterface(data_parser, text_processor, topic_modeler)
    program_interface.mainloop()
