__author__ = 'derua_000'


class Word:

    def __init__(self, word):
        self.word = word
        self.type = None
        self.count_pos = 1
        self.count_neg = 1

    def incr_pos(self):
        self.count_pos += 1

    def incr_neg(self):
        self.count_neg += 1