from dataCollector import DataCollector
from naifBayes import NaifBayes

def compute_probas(directory_tagged, directory_untagged, percentage=0.8, number_blocks=10):
    d = DataCollector(directory_tagged)
    nB = NaifBayes(d, percentage, number_blocks )
    results = nB.compute_all(directory_tagged, directory_untagged)


    for name, tupleResult in sorted(results.items(), key=lambda key: key[0]):
        print(name, " %Pos:", tupleResult[0], " %Neg", tupleResult[1], " %Tot",tupleResult[2], " Time",tupleResult[3])

def main():
    compute_probas( "./data/tagged/" , "./data/untagged/")

if __name__ == "__main__":
    main()