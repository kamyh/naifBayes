__author__ = 'derua_000'

from dataCollector import DataCollector
from naifBayes import NaifBayes

def main():
    dir = "./data/untagged/"
    d = DataCollector(dir)
    list_test_pos, list_training_pos, list_test_neg, list_training_neg = d.get_divide(0.8)

    nB = NaifBayes(d)

if __name__ == "__main__":
    main()