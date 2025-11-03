
from multiprocessing import Pool
#
# Пул процессов.
#  Разделяемая память.
#   Подходит для Mystem.
#

from nltk.corpus import stopwords
#
# "Natural Language Toolkit"
#  stopwords: список стоп-слов
#

from pymystem3 import Mystem
#
# Mystem
#  Приведение слов к начальной форме
#


rus_stopwords = None
mystem        = None


def init_worker():
    global mystem, rus_stopwords
    rus_stopwords = set(stopwords.words("russian"))
    mystem        = Mystem("/usr/local/bin/mystem")

def process_text(text):
    if not text.strip(): return ""
    words    = mystem.lemmatize(text.lower())
    filtered = [w for w in words if w.strip() and w != " " and w not in rus_stopwords]
    return " ".join(filtered)

def start_pool(texts):
    with Pool(processes=4, initializer=init_worker) as pool:
        results = pool.map(process_text, texts)
    return results
