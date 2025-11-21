
from   multiprocessing import Pool
from   os              import cpu_count

from   pymystem3       import Mystem
import nltk


mystem        = None
rus_stopwords = None

def init_worker():
    global mystem, rus_stopwords
    rus_stopwords = set(nltk.corpus.stopwords.words("russian"))
    mystem        = Mystem(mystem_bin="/usr/local/bin/mystem")

def worker_func(text: str) -> str:
    if not mystem or not text or not text.strip(): return ""
    try:
        words = mystem.lemmatize(text.lower())
        filtered = [w for w in words if w.strip() and w not in rus_stopwords]
        return " ".join(filtered)
    except Exception:
        return ""

class Processor:
    def __init__(self):
        self.log_info = []
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            self.log_info.append("  nltk.data.find() LookupError")
            try:
                nltk.download('stopwords')
            except:
                self.log_info.append("  nltk.download() Error")

    def start_pool(self, texts: list[str]) -> list[str]:
        cpu_num = cpu_count()
        if isinstance(cpu_num, int): cpu_num = max(1, cpu_num - 1)
        else: cpu_num = 1
        self.log_info.append(f"   cpu_num = {cpu_num}")
        with Pool(processes=cpu_num, initializer=init_worker) as pool:
            results = pool.map(worker_func, texts)
        clean_results = [r for r in results if r]
        self.log_info.append(f"   Processed: {len(clean_results)} lines")
        return clean_results
