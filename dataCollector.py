__author__ = 'derua_000'
import glob

class DataCollector:
    def __init__(self):
        self.className ="dataCollector"
        self.files = []

    def display_class_name(self):
        print(self.className)

    def get_dir_content(self, name):

        self.files = glob.glob(name)
        print(self.files)