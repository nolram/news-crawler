#-.- encoding:utf-8 -.-
import json
import nltk
import codecs
import random

from news_item import NewsItem
from pymongo import MongoClient
from nltk.classify import apply_features

DEBUG = True


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

    def identify_top_words(self, all_words):
        freq_dist = nltk.FreqDist(w.lower() for w in all_words)
        return list(freq_dist)[:1000]

    def collect_news(self):
        news_list = []
        contador = 0
        for news in self.news.find():
            if contador < 10000:
                ns = NewsItem(news, self.stop_words)
                news_list.append(ns)
            else:
                break
            contador += 1
        return news_list

    def collect_all_words(self, news_list):
        all_words = []
        for news in news_list:
            all_words.extend(news.all_words)
        return all_words

    def classificar(self, word):
        return self.classifier.classify(word)

    def features(self, top_words):
        word_set = set(self.all_words)
        features = {}
        features['url'] = self.url
        for w in top_words:
            features["w_%s" % w] = (w in word_set)
        return features

    def classify(self):
        print(u"Coletando as Notícias")
        news_items = self.collect_news()

        print(u"Coletando todas as palavras")
        all_words = self.collect_all_words(news_items)

        print(u"Coletando as principais palavras")
        top_words = self.identify_top_words(all_words)

        print(u"Embaralhando")
        random.shuffle(news_items)

        print(u"Gerando conjunto de treinamento")
        featuresets = []
        for item in news_items:
            item_features = item.features(top_words)
            tup = (item_features, item.category)
            featuresets.append(tup)

        train_set = featuresets[1000:]

        #test_set = featuresets[:1000]

        print('Featuresets tamanho: ' + str(len(featuresets)))

        print("Treinando...")
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)
        print("Treinamento Completo complete")

        if DEBUG:
            arquivo_teste = codecs.open("doc_test_2.json", "r", encoding="utf-8")
            items_news = json.loads(arquivo_teste.read())
            list_test = []
            for item in items_news:
                news = NewsItem(item, self.stop_words)
                list_test.append(news)

            for i in list_test:
                feat = i.features(top_words)
                print(u"{} - {}".format(i.title, self.classificar(feat)))
            #print(nltk.classify.accuracy(self.classifier, test_set))

if __name__ == "__main__":
    clas = Classificador()
