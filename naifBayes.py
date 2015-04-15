__author__ = 'derua_000'

from word import Word
from math import log
from dataCollector import DataCollector

class NaifBayes:
    def __init__(self, data_collector,traning_percentage):
        self.data_collector = data_collector
        self.traning_percentage = traning_percentage
        self.nbr_pos = 0.
        self.nbr_neg = 0.
        self.list_test_pos = None
        self.list_training_pos = None
        self.list_test_neg = None
        self.list_training_neg = None


    def count_words(self, is_canonical):
        if is_canonical:
            def find_words(line):
                listword = line.split(" ")
                for word in listword:
                    yield word
        else:
            def find_words(line):
                yield line.split(" ")[-1]

        self.dict_words = dict()
        self.list_test_pos, self.list_training_pos, self.list_test_neg, self.list_training_neg = self.data_collector.get_divide(self.traning_percentage)

        print("zgeg1")
        for file_name in self.list_training_pos:
            print(file_name)
            with open(file_name) as file:
                for line in file.readlines():
                    for word in find_words(line):
                        if word in self.dict_words.keys():
                            self.dict_words[word].incr_pos()
                            self.nbr_pos += 1
                        else:
                            self.dict_words[word] = Word(word)

        print("zgeg2")
        for file_name in self.list_training_neg:
            print(file_name)
            with open(file_name) as file:
                for line in file.readlines():
                    for word in find_words(line):
                        if word in self.dict_words.keys():
                            self.dict_words[word].incr_neg()
                            self.nbr_neg += 1
                        else:
                            self.dict_words[word] = Word(word)

        print("zgeg")

    def compute_proba(self):
        print("compute_proba")
        for word in self.dict_words.values():
            word.compute_probas(self.nbr_pos,self.nbr_neg)

    def compute_type(self):
        print("compute_type")
        for word in self.dict_words.values():
            word.define_type()

    # return true if document positive
    def compute_test(self, document, is_canonical):
        if is_canonical:
            def find_words(line):
                listword = line.split(" ")
                for word in listword:
                    yield word
        else:
            def find_words(line):
                yield line.split(" ")[-1]

        proba_pos = 1.
        proba_neg = 1.

        with open(document) as file:
            for line in file.readlines():
                for word in find_words(line):
                    if word in self.dict_words.keys():
                        proba_pos += log(self.dict_words[word].proba_pos)
                        proba_neg += log(self.dict_words[word].proba_neg)

        proba_pos += log(self.nbr_pos/(self.nbr_pos + self.nbr_neg))
        proba_neg += log(1-proba_pos)

        return proba_pos > proba_neg

    def compute_tests(self, is_canonical):
        print("compute_tests")
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

        print("resultat: %f" % (ok/tot))