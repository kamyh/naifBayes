__author__ = 'derua_000'

from dataCollector import DataCollector

def main():
    print("main")
    dir = "./data/pos/*.txt"
    d = DataCollector()
    d.get_dir_content(dir)

if __name__ == "__main__":
    main()