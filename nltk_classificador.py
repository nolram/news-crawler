import re
import nltk
import string
from pymongo import MongoClient

class Classificador:
    """
	Script de aprendizado de máquina para aprender com os textos extraidos pelo Scrapy e determinar a categoria dado uma palavra
    """
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.articles_news
        self.news = self.db.articles
        self.regex = re.compile('[%s]' % re.escape(string.punctuation))
        self.stop_words = self._load_stop_words()
        self.classificar_palavras()
        #self.top_words = self.identify_top_words()
        #self.word_set = set(self.all_words)
        self.training_set()
        #self.array_de_categorias = self.coletar_categorias_unicas_por_frequencia()

    def _load_stop_words(self):
        stop_words = nltk.corpus.stopwords.words('portuguese')
        d_stop_words = set(stop_words)
        return d_stop_words

    def coletar_categorias_unicas_por_frequencia(self):
        freqs = nltk.FreqDist()
        sorted_cats = []
        for item in self.rss_items:
            for w in item.categories:
                freqs.inc(w, 1)
        for cat in freqs.keys():
            sorted_cats.append(cat)
            print("collect_sorted_categories: %s  %d" % (cat, freqs.get(cat)))
        return sorted_cats

    
    def identify_top_words(self):
        freq_dist = nltk.FreqDist(w.lower() for w in self.all_words)
        return list(freq_dist)[:1000]
    

    def normalizar(self, texto):
        words = list()
        oneline = texto.replace('\n', ' ')
        #cleaned = nltk.clean_html(oneline.strip())
        toks1 = oneline.strip().split()
        for t1 in toks1:
            translated = self.regex.sub('', t1)
            toks2 = translated.split()
            for t2 in toks2:
                t2s = t2.strip().lower()
                if t2s not in self.stop_words:
                    words.append(t2s)
        return words

    def training_set(self):
        featuresets = list()
        for i in self.labeled_news:
            for j in i[0]:
                featuresets.append((self.word_features(j), i[1]))
        size = 100 #int(len(featuresets) * 0.1)
        #print(size)
        self.train_set, self.test_set = featuresets[size:], featuresets[:size]
        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)

    def classificar_palavras(self):
        self.labeled_news = list()
        self.all_words = list()
        for news in self.news.find():
            #print(news)
            if "titulo" in news and "categoria" in news:
                titulo = self.normalizar(news["titulo"])
                if "subcategoria" in news:
                    self.labeled_news.append((titulo, news["subcategoria"].lower()))
                else:
                    self.labeled_news.append((titulo, news["categoria"].lower()))
                #self.all_words.extend(titulo)

    def classificar(self, word):
        return self.classifier.classify(self.word_features(word))

    def word_features(self, word):
        return {"palavra": word}

    def features(self, top_words):
        features = {}
        for w in self.top_words:
            features["w_%s" % w] = (w in self.word_set)
        return features

    def testar(self):
        print("{} - {}".format("obama",self.classificar("obama")))
        print("{} - {}".format("dilma",self.classificar("dilma")))
        print("{} - {}".format("aécio",self.classificar("aécio")))
        print("{} - {}".format("neves",self.classificar("neves")))
        print("{} - {}".format("google",self.classificar("google")))
        print("{} - {}".format("microsoft",self.classificar("microsoft")))
        print("{} - {}".format("warcraft",self.classificar("warcraft")))
        print("{} - {}".format("starcraft",self.classificar("starcraft")))
        print("{} - {}".format("detran",self.classificar("detran")))
        print("{} - {}".format("fbi",self.classificar("fbi")))
        print("{} - {}".format("dicraprio",self.classificar("dicaprio")))
        print("{} - {}".format("leonardo",self.classificar("leonardo")))
        print("{} - {}".format("marlon",self.classificar("oscar")))
        print("{} - {}".format("yahoo",self.classificar("yahoo")))
        print("{} - {}".format("anéis",self.classificar("anéis")))
        print("{} - {}".format("witcher",self.classificar("witcher")))
        print("{} - {}".format("stanford",self.classificar("stanford")))
        print("{} - {}".format("dengue",self.classificar("dengue")))
        print("{} - {}".format("água",self.classificar("água")))
        print("{} - {}".format("fome",self.classificar("fome")))
        print("{} - {}".format("internacional",self.classificar("internacional")))
        print("{} - {}".format("grêmio",self.classificar("grêmio")))

if __name__ == "__main__":
    clas = Classificador()
    clas.testar()
    print(nltk.classify.accuracy(clas.classifier, clas.test_set))
