import nltk
import random
from news_item import NewsItem
from pymongo import MongoClient

def _load_stop_words():
    stop_words = nltk.corpus.stopwords.words('portuguese')
    d_stop_words = set(stop_words)
    return d_stop_words


class Classificador:
    """
        Script de aprendizado de máquina para aprender com os textos extraidos pelo Scrapy
        e determinar a categoria dado uma palavra
    """

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.articles_news
        self.news = self.db.articles
        self.stop_words = _load_stop_words()
        self.classify()


        #self.collect_news()
        #self.top_words = self.identify_top_words()
        # self.word_set = set(self.all_words)
        # self.array_de_categorias = self.coletar_categorias_unicas_por_frequencia()
        #self.training_set()

    def coletar_categorias_unicas_por_frequencia(self):
        freqs = nltk.FreqDist()
        sorted_cats = []
        for item in self.labeled_news:
            freqs.inc(item[1], 1)
        for cat in freqs.keys():
            sorted_cats.append(cat)
            print("collect_sorted_categories: %s  %d" % (cat, freqs.get(cat)))
        return sorted_cats

    def identify_top_words(self):
        freq_dist = nltk.FreqDist(w.lower() for w in self.all_words)
        return list(freq_dist)[:1000]

    def training_set(self):
        featuresets = list()
        for i in self.labeled_news:
            for j in i[0]:
                featuresets.append((self.word_features(j), i[1]))
        size = 100  # int(len(featuresets) * 0.1)
        # print(size)
        self.train_set, self.test_set = featuresets[size:], featuresets[:size]
        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)

    def collect_news(self):
        news_list = []
        for news in self.news.find():
            ns = NewsItem(news, self.stop_words)
            news_list.append(ns)
        return news_list

    def collect_all_words(self, news_list):
        all_words = []
        for news in news_list:
            all_words.extend(news.all_words)
        return all_words

    def classificar(self, word):
        return self.classifier.classify(self.word_features(word))

    def word_features(self, word):
        return {"palavra": word}

    def features(self, top_words):
        features = {}
        for w in self.top_words:
            features["w_%s" % w] = (w in self.word_set)
        return features

    def classify(self):
        news_items = self.collect_news()
        all_words = self.collect_all_words(news_items)
        top_words = self.identify_top_words(all_words)

        random.shuffle(news_items)

        featuresets = []
        for item in news_items:
            item_features = item.features(top_words)
            tup = (item_features, item.category)
            featuresets.append(tup)

        train_set = featuresets

        print('featuresets count: ' + str(len(featuresets)))

        print("training...")
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)
        print("training complete")


    def testar(self):
        print("{} - {}".format("obama", self.classificar("obama")))
        print("{} - {}".format("dilma", self.classificar("dilma")))
        print("{} - {}".format("aécio", self.classificar("aécio")))
        print("{} - {}".format("neves", self.classificar("neves")))
        print("{} - {}".format("google", self.classificar("google")))
        print("{} - {}".format("microsoft", self.classificar("microsoft")))
        print("{} - {}".format("warcraft", self.classificar("warcraft")))
        print("{} - {}".format("starcraft", self.classificar("starcraft")))
        print("{} - {}".format("detran", self.classificar("detran")))
        print("{} - {}".format("fbi", self.classificar("fbi")))
        print("{} - {}".format("dicraprio", self.classificar("dicaprio")))
        print("{} - {}".format("leonardo", self.classificar("leonardo")))
        print("{} - {}".format("marlon", self.classificar("oscar")))
        print("{} - {}".format("yahoo", self.classificar("yahoo")))
        print("{} - {}".format("anéis", self.classificar("anéis")))
        print("{} - {}".format("witcher", self.classificar("witcher")))
        print("{} - {}".format("stanford", self.classificar("stanford")))
        print("{} - {}".format("dengue", self.classificar("dengue")))
        print("{} - {}".format("água", self.classificar("água")))
        print("{} - {}".format("fome", self.classificar("fome")))
        print("{} - {}".format("internacional", self.classificar("internacional")))
        print("{} - {}".format("grêmio", self.classificar("grêmio")))


if __name__ == "__main__":
    clas = Classificador()
    clas.testar()
    print(nltk.classify.accuracy(clas.classifier, clas.test_set))
