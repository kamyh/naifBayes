__author__ = 'derua_000'
import glob

class DataCollector:
    def __init__(self,dir_name):
        self.className ="dataCollector"
        self.files_pos = []
        self.files_neg = []
        self.dir_name = dir_name
        self.get_dir_content()

    def display_class_name(self):
        print(self.className)

    def get_dir_content(self):
        self.files_pos = glob.glob(self.dir_name+'pos/*.txt')
        self.files_neg = glob.glob(self.dir_name+'neg/*.txt')

    def get_divide(self, training_percentage):

        list_test_pos, list_training_pos = DataCollector.divide_list(self.files_pos, training_percentage)
        list_test_neg, list_training_neg = DataCollector.divide_list(self.files_neg, training_percentage)

        return list_test_pos, list_training_pos, list_test_neg, list_training_neg

    @staticmethod
    def divide_list(list_files, training_percentage):
        from random import random
        from copy import deepcopy
        list_files_copy = deepcopy(list_files)
        training_len = len(list_files) * training_percentage
        list_training = []
        while len(list_training) < training_len:
            index = random() * len(list_files_copy)
            list_training.append(list_files_copy.pop(int(index)))

        return list_files_copy, list_training