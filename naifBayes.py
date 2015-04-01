__author__ = 'derua_000'

from word import Word
from dataCollector import DataCollector

class NaifBayes:
    def __init__(self, data_collector,traning_percentage):
        self.data_collector = data_collector
        self.traning_percentage = traning_percentage

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
        list_test_pos, list_training_pos, list_test_neg, list_training_neg = self.data_collector.get_divide(self.traning_percentage)

        for file_name in list_training_pos:
            with open(file_name) as file:
                for line in file.readlines():
                    for word in line.split(' '):
                        if word in self.dict_words.keys():
                            self.dict_words[word].incr_pos()
                        else:
                            self.dict_words[word] = Word(word)

        for file_name in list_training_neg:
            with open(file_name) as file:
                for line in file.readlines():
                    for word in line.split(' '):
                        if word in self.dict_words.keys():
                            self.dict_words[word].incr_neg()
                        else:
                            self.dict_words[word] = Word(word)
