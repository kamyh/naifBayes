__author__ = 'derua_000'

from dataCollector import DataCollector
from naifBayes import NaifBayes

import time

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts))
        return result

    return timed

@timeit
def main():
    dir = "./data/tagged/"
    d = DataCollector(dir)


    nB = NaifBayes(d, 0.8)
    is_canonical = True
    nB.count_words(is_canonical)
    nB.compute_proba()
    nB.compute_type()
    nB.compute_tests(is_canonical)

if __name__ == "__main__":
    main()