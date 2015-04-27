from word import Word
from math import log
from dataCollector import DataCollector
import codecs

class NaifBayes:
    def __init__(self, data_collector, traning_percentage, list_exclusion_file = './data/frenchST.txt'):
        self.data_collector = data_collector
        self.traning_percentage = traning_percentage
        self.nbr_pos = 0.
        self.nbr_neg = 0.
        self.list_test_pos = None
        self.list_training_pos = None
        self.list_test_neg = None
        self.list_training_neg = None
        if list_exclusion_file is not None:
            NaifBayes.list_exclusion = []
            with codecs.open(list_exclusion_file, "r", "utf-8") as file:
                    NaifBayes.list_exclusion.extend(file.readlines())


    list_exclusion = None
    @staticmethod
    def find_words_untagged(line):
        return [word for word in line.split(" ") if word not in NaifBayes.list_exclusion]

    list_taken =['VER','ADJ','ADV', 'NOM', 'NAM']
    @staticmethod
    def find_words_tagged(line):
        split = line.split('\t')
        try:
            if split[1].split(':')[0] in NaifBayes.list_taken:
                yield split[-1]
        except:
            print ("Ignored: " + split[-1])

    def count_words(self, is_canonical):
        if is_canonical:
            find_words = NaifBayes.find_words_tagged
        else:
            find_words = NaifBayes.find_words_untagged

        self.dict_words = dict()
        self.list_test_pos, self.list_training_pos, self.list_test_neg, self.list_training_neg = self.data_collector.get_divide(self.traning_percentage)


        for file_name in self.list_training_pos:
            with codecs.open(file_name, "r", "utf-8") as file:
                for line in file.readlines():
                    for word in find_words(line):
                        self.nbr_pos += 1
                        if word in self.dict_words.keys():
                            self.dict_words[word].incr_pos()
                        else:
                            self.dict_words[word] = Word(word)

        for file_name in self.list_training_neg:
            with codecs.open(file_name, "r", "utf-8") as file:
                for line in file.readlines():
                    for word in find_words(line):
                        self.nbr_neg += 1
                        if word in self.dict_words.keys():
                            self.dict_words[word].incr_neg()
                        else:
                            self.dict_words[word] = Word(word)

    def compute_proba(self):
        for word in self.dict_words.values():
            word.compute_probas(self.nbr_pos,self.nbr_neg)

    def compute_type(self):
        for word in self.dict_words.values():
            word.define_type()

    # return true if document positive
    def compute_test(self, document, is_canonical):
        if is_canonical:
            find_words = NaifBayes.find_words_tagged
        else:
            find_words = NaifBayes.find_words_untagged

        proba_pos = 1.
        proba_neg = 1.

        with codecs.open(document, "r", "utf-8") as file:
            for line in file.readlines():
                for word in find_words(line):
                    if word in self.dict_words.keys():
                        proba_pos += log(self.dict_words[word].proba_pos)
                        proba_neg += log(self.dict_words[word].proba_neg)

        proba_pos += log(self.nbr_pos/(self.nbr_pos + self.nbr_neg))
        proba_neg += log(1-proba_pos)

        return proba_pos > proba_neg

    def compute_tests(self, is_canonical):
        tot = 0.
        ok = 0.
        for doc_pos in self.list_test_pos:
            tot += 1
            if self.compute_test(doc_pos, is_canonical):
                ok += 1

        for doc_neg in self.list_test_neg:
            tot += 1
            if not self.compute_test(doc_neg, is_canonical):
                ok += 1
        return (ok/tot)

    def compute_all(self, is_canonical):
        dict_words = self.count_words(is_canonical)
        self.compute_proba()
        self.compute_type()
        return self.compute_tests(is_canonical)