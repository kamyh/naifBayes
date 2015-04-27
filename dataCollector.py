import glob

class DataCollector:
    def __init__(self,dir_name):
        self.className ="dataCollector"
        self.files_pos = []
        self.files_neg = []
        self.get_dir_content(dir_name)

    def display_class_name(self):
        print(self.className)

    def get_dir_content(self, dir_name):
        self.files_pos = glob.glob(dir_name+'pos/*.txt')
        self.files_neg = glob.glob(dir_name+'neg/*.txt')

    def get_divide(self, training_percentage):
        list_test_pos, list_training_pos = DataCollector.divide_list(self.files_pos, training_percentage)
        list_test_neg, list_training_neg = DataCollector.divide_list(self.files_neg, training_percentage)

        return list_test_pos, list_training_pos, list_test_neg, list_training_neg

    def get_cross_validation_generator(self, number_blocks):
        for i in range(number_blocks):
            list_test_pos, list_training_pos = DataCollector.cross_validation_list(self.files_pos, i, number_blocks)
            list_test_neg, list_training_neg = DataCollector.cross_validation_list(self.files_neg, i, number_blocks)
            yield list_test_pos, list_training_pos, list_test_neg, list_training_neg

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

    @staticmethod
    def cross_validation_list(list_files, i, number_blocks):
        length_block = int(len(list_files)/number_blocks)
        list_training = list_files[i*length_block: (i+1)*length_block]
        return  list_training, [x for x in list_files if x not in list_training]