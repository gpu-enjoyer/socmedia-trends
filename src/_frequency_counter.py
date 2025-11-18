
import gensim
from   gensim import corpora

# TODO
class FrequencyCounter:
    pass

class TopicModeler:
    def getWeights(self, lines):
        dictionary = corpora.Dictionary(
            [x.split() for x in lines]) # создать словарь
        lda_model = gensim.models.LdaModel(
            id2word=dictionary, num_topics=5, passes=50) # обучить модель
        return lda_model.print_topics(
            num_topics=5, num_words=3)
