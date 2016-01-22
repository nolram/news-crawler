import re
import string
import nltk

from bs4 import BeautifulSoup

__author__ = 'nolram'


class NewsItem:

    def __init__(self, news, stop_words):
        self.all_words = []
        self.stop_words = stop_words
        self.regex = re.compile('[%s]' % re.escape(string.punctuation))

        if "titulo" in news and "categoria" in news:
            self.add_words(news["titulo"])
            self.title = news["titulo"]

        if "subcategoria" in news:
            self.category = news["subcategoria"].lower()
        else:
            self.category = news["categoria"].lower()

        if "texto" in news:
            self.add_words(" ".join(news["texto"]))

        self.url = news["url"]

    def normalized_words(self, s):
        words = []
        oneline = s.replace('\n', ' ')
        soup = BeautifulSoup(oneline.strip(), 'html.parser')
        cleaned = soup.get_text()
        toks1 = cleaned.split()
        for t1 in toks1:
            translated = self.regex.sub('', t1)
            toks2 = translated.split()
            for t2 in toks2:
                t2s = t2.strip()
                if len(t2s) > 1:
                    words.append(t2s.lower())
        return words

    def word_count(self):
        return len(self.all_words)

    def word_freq_dist(self):
        freqs = nltk.FreqDist()  # class nltk.probability.FreqDist
        for w in self.all_words:
            freqs.inc(w, 1)
        return freqs

    def add_words(self, s):
        words = self.normalized_words(s)
        for w in words:
            if w not in self.stop_words:
                self.all_words.append(w)

    def features(self, top_words):
        word_set = set(self.all_words)
        features = {}
        features['url'] = self.url
        for w in top_words:
            features["w_%s" % w] = (w in word_set)
        return features

    def normalized_frequency_power(self, word, freqs, largest_count):
        n = self.normalized_frequency_value(word, freqs, largest_count)
        return pow(n, 2)

    def normalized_frequency_value(self, word, freqs, largest_count):
        count = freqs.get(word)
        n = 0
        if count is None:
            n = float(0)
        else:
            n = ((float(count) * float(largest_count)) / float(freqs.N())) * 100.0
        return n

    def normalized_boolean_value(self, word, freqs, largest_count):
        count = freqs.get(word)
        if count is None:
            return float(0)
        else:
            return float(1)

    def knn_data(self, top_words):
        data_array = []
        freqs = self.word_freq_dist()
        largest_count = freqs.values()[0]
        features = {}
        features['url'] = self.url
        for w in top_words:
            data_array.append(self.normalized_boolean_value(w, freqs, largest_count))
        print "knn_data: %s" % data_array
        return data_array


    def as_debug_array(self, guess):
        l = []
        l.append('---')
        #l.append('lookup_key:   %s' % (self.lookup_key()))
        l.append('Categoria:     %s' % (self.category))
        l.append('Palpite:        %s' % (guess))
        l.append('URL:     %s' % (self.url))
        l.append('Titulos:   %s' % (self.title))
        l.append('')
        l.append('Todas as palavras por contagem')
        freqs = nltk.FreqDist([w.lower() for w in self.all_words])
        for w in freqs.keys():
            l.append("%-20s  %d" % (w, freqs.get(w)))
        l.append('')
        l.append('all_words, sequentially:')
        for w in self.all_words:
            l.append(w)
        return l
