
# Пул процессов. Разделяемая память.
from multiprocessing import Pool

# "Natural Language Toolkit"
from nltk.corpus import stopwords

# Приведение слов к начальной форме
from pymystem3 import Mystem


rus_stopwords = None
mystem        = None

class DataProcessor:

    def __init__(self) -> None:
        pass
    
    def init_worker():
        global mystem, rus_stopwords
        rus_stopwords = set(stopwords.words("russian"))
        mystem        = Mystem("/usr/local/bin/mystem")

    def process_text(text):
        if not mystem or text.strip():
            return ""
        words    = mystem.lemmatize(text.lower())
        filtered = [w for w in words if w.strip() and w != " " and w not in rus_stopwords]
        return " ".join(filtered)

    def start_pool(texts):
        with Pool(processes=4, initializer=init_worker) as pool:
            results = pool.map(process_text, texts)
        return results
