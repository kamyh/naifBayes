from dataCollector import DataCollector
from naifBayes import NaifBayes



def compute_probas(directory_tagged, directory_untagged, percentage=0.8, number_blocks=10):
    d = DataCollector(directory_tagged)
    nB = NaifBayes(d, percentage, number_blocks )
    results = nB.compute_all(directory_tagged, directory_untagged)
    pos = 0
    neg = 0
    mean = 0

    for name, tupleResult in sorted(results.items(), key=lambda key: key[0]):
        print(name, " %Pos:", tupleResult[0], " %Neg", tupleResult[1], " %Tot",tupleResult[2], " Time",tupleResult[3])
        if(str(name).__contains__('cross')):
            if (str(name).__contains__('0')):
                pos = tupleResult[0]
                neg = tupleResult[1]
            else:
                pos += tupleResult[0]
                neg += tupleResult[1]

                if (str(name).__contains__('9')):
                   print("pos %d",(pos/10))
                   print("neg %d",(neg/10))
                   print("mean %d",(((pos/10)+(neg/10))/2))
        else:
            print("mean %d",(tupleResult[0] + tupleResult[1])/2)


def main():
    compute_probas( "./data/tagged/" , "./data/untagged/")

if __name__ == "__main__":
    main()