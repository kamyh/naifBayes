from word import Word
from math import log
from dataCollector import DataCollector
import codecs
from Timer import Timer

class NaifBayes:
    def __init__(self, data_collector, traning_percentage, number_blocks, list_exclusion_file = './data/frenchST.txt'):
        self.data_collector = data_collector
        self.traning_percentage = traning_percentage
        self.number_blocks = number_blocks
        self.nbr_pos = 0.
        self.nbr_neg = 0.
        NaifBayes.list_exclusion_file = list_exclusion_file
        NaifBayes.reset_list_exclusion()

    @staticmethod
    def reset_list_exclusion():
        NaifBayes.list_exclusion = []
        with codecs.open(NaifBayes.list_exclusion_file, "r", "utf-8") as file:
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
            pass

    def count_words(self, is_canonical, list_test_pos, list_training_pos, list_test_neg, list_training_neg):
        if is_canonical:
            find_words = NaifBayes.find_words_tagged
        else:
            find_words = NaifBayes.find_words_untagged

        dict_words = dict()

        for file_name in list_training_pos:
            with codecs.open(file_name, "r", "utf-8") as file:
                for line in file.readlines():
                    for word in find_words(line):
                        self.nbr_pos += 1
                        if word in dict_words.keys():
                            dict_words[word].incr_pos()
                        else:
                            dict_words[word] = Word(word)

        for file_name in list_training_neg:
            with codecs.open(file_name, "r", "utf-8") as file:
                for line in file.readlines():
                    for word in find_words(line):
                        self.nbr_neg += 1
                        if word in dict_words.keys():
                            dict_words[word].incr_neg()
                        else:
                            dict_words[word] = Word(word)
        return dict_words

    def compute_proba(self, dict_words):
        for word in dict_words.values():
            word.compute_probas(self.nbr_pos,self.nbr_neg)

    def compute_type(self, dict_words):
        for word in dict_words.values():
            word.define_type()

    # return true if document positive
    def compute_test(self, document, is_canonical, dict_words):
        if is_canonical:
            find_words = NaifBayes.find_words_tagged
        else:
            find_words = NaifBayes.find_words_untagged

        proba_pos = 1.
        proba_neg = 1.

        with codecs.open(document, "r", "utf-8") as file:
            for line in file.readlines():
                for word in find_words(line):
                    if word in dict_words.keys():
                        proba_pos += log(dict_words[word].proba_pos)
                        proba_neg += log(dict_words[word].proba_neg)

        proba_pos += log(self.nbr_pos/(self.nbr_pos + self.nbr_neg))
        proba_neg += log(1-proba_pos)

        return proba_pos > proba_neg

    def compute_tests(self, is_canonical, dict_words,list_test_pos, list_test_neg):
        total_pos = 0.
        ok_pos = 0.
        total_neg = 0.
        ok_neg = 0.
        for doc_pos in list_test_pos:
            total_pos += 1
            if self.compute_test(doc_pos, is_canonical, dict_words):
                ok_pos += 1
        for doc_neg in list_test_neg:
            total_neg += 1
            if not self.compute_test(doc_neg, is_canonical, dict_words):
                ok_neg += 1
        return (ok_pos/total_pos,ok_neg/total_neg,(ok_pos+ok_neg)/(total_pos+total_neg))

    def compute(self, is_canonical, list_test_pos, list_training_pos, list_test_neg, list_training_neg):
        with Timer() as t:
            dict_words = self.count_words(is_canonical, list_test_pos, list_training_pos, list_test_neg, list_training_neg)
            self.compute_proba(dict_words)
            self.compute_type(dict_words)
            toReturn =self.compute_tests(is_canonical, dict_words, list_test_pos, list_test_neg)
        return (toReturn[0], toReturn[2], toReturn[2], t.interval)

    def compute_all(self, canonical_dir, normal_dir):
        dict_results = {}
        print("Computing normal_exclusion_divided")
        self.data_collector.get_dir_content(normal_dir)
        list_test_pos, list_training_pos, list_test_neg, list_training_neg = self.data_collector.get_divide(self.traning_percentage)
        dict_results['normal_exclusion_divided'] = self.compute(False, list_test_pos, list_training_pos, list_test_neg, list_training_neg)

        print("Computing normal_exclusion_cross0...9")
        i = 0
        for list_test_pos, list_training_pos, list_test_neg, list_training_neg in self.data_collector.get_cross_validation_generator(self.number_blocks):
            dict_results['normal_exclusion_cross'+str(i)] = self.compute(False, list_test_pos, list_training_pos, list_test_neg, list_training_neg)
            print (i)
            i += 1
        NaifBayes.list_exclusion = []

        print("Computing normal_no_exclusion_divided")

        list_test_pos, list_training_pos, list_test_neg, list_training_neg = self.data_collector.get_divide(self.traning_percentage)
        dict_results['normal_no_exclusion_divided'] = self.compute(False, list_test_pos, list_training_pos, list_test_neg, list_training_neg)

        print("Computing normal_no_exclusion_cross0...9")
        i = 0
        for list_test_pos, list_training_pos, list_test_neg, list_training_neg in self.data_collector.get_cross_validation_generator(self.number_blocks):
            dict_results['normal_no_exclusion_cross'+str(i)] = self.compute(False, list_test_pos, list_training_pos, list_test_neg, list_training_neg)
            print (i)
            i += 1
        NaifBayes.reset_list_exclusion()

        print("Computing canonical_divided")
        self.data_collector.get_dir_content(canonical_dir)
        list_test_pos, list_training_pos, list_test_neg, list_training_neg = self.data_collector.get_divide(self.traning_percentage)
        dict_results['canonical_divided'] = self.compute(True, list_test_pos, list_training_pos, list_test_neg, list_training_neg)

        print("Computing canonical_cross0...9")
        i = 0
        for list_test_pos, list_training_pos, list_test_neg, list_training_neg in self.data_collector.get_cross_validation_generator(self.number_blocks):
            dict_results['canonical_cross'+str(i)] = self.compute(True, list_test_pos, list_training_pos, list_test_neg, list_training_neg)
            print (i)
            i += 1
        return dict_results

