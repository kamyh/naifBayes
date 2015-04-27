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
def compute_probas(directory, is_canonical=True):
    dir = directory
    d = DataCollector(dir)

    percentage = 0.8
    nB = NaifBayes(d, percentage )
    result = nB.compute_all(is_canonical)
    print ("Resultat = %f" % result )

def main():
    path = "./data/tagged/" #tagged or untagged
    compute_probas(path , "./data/untagged/" != path)

if __name__ == "__main__":
    main()