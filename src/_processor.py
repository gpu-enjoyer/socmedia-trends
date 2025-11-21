
from   multiprocessing import Pool
from   os              import cpu_count

from   pymystem3       import Mystem
import nltk

from   collections     import Counter


__my_stopwords: set[str] = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    "0123456789"
    ".,;:!?-—()[]{}'\"«»‹›/\\@#№$%&*+=_<>^`~|^"
    " \t\n"
) | {
    "который", "которая", "которое",
    "https", "http", "://", "ru", "com",
    "»,", "%,", "↖"
}

__mystem        = Mystem(mystem_bin="/usr/local/bin/mystem")
__rus_stopwords = set(nltk.corpus.stopwords.words("russian")) | __my_stopwords


def init_worker():
    global mystem, rus_stopwords
    mystem        = __mystem
    rus_stopwords = __rus_stopwords

def worker_func(text: str) -> Counter:
    if not mystem or not text or not text.strip():
        return Counter()
    try:
        words = mystem.lemmatize(text.lower())
        filtered = [w
                    for w in words
                    if w.strip() and w.strip() not in rus_stopwords]
        return Counter(filtered)
    except Exception:
        return Counter()

class Processor:
    def __init__(self):
        self.log_info = []
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            self.log_info.append("   nltk.data.find() LookupError")
            try:
                nltk.download('stopwords')
            except:
                self.log_info.append("   nltk.download() Error")

    def start_pool(self, texts: list[str]) -> Counter:
        cores_num = cpu_count()
        if isinstance(cores_num, int):
            cores_num = max(1, cores_num - 1)
        else:
            cores_num = 1
        self.log_info.append(f"   cores_num = {cores_num}")
        with Pool(processes=cores_num, initializer=init_worker) as pool:
            try:
                test_text = "Который год разработчики говорят о новейших технологиях"
                test_res  = pool.apply(worker_func, [test_text]) 
                self.log_info.append(f"   test_text = \"{test_text}\"")
                self.log_info.append(f"   test_res  = \"{test_res}\"")
            except Exception as e:
                self.log_info.append(f"   ERR: Worker crashed: {e}")
                return Counter()
            results = pool.map(worker_func, texts)
            # [Counter('privet':1), Counter('kak_dela':2), ...]
        total_counter = Counter()
        for cnt in results:
            total_counter.update(cnt)
        return total_counter
