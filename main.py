__author__ = 'derua_000'

from dataCollector import DataCollector
from naifBayes import NaifBayes

def main():
    dir = "./data/untagged/"
    d = DataCollector(dir)


    nB = NaifBayes(d, 0.8)
    is_canonical = True
    nB.count_words(is_canonical)
    nB.compute_proba()
    nB.compute_type()
    nB.compute_tests(is_canonical)

if __name__ == "__main__":
    main()