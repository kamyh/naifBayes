__author__ = 'derua_000'

class Type():
    negatif = 0
    positif = 1

class Word:

    def __init__(self, word):
        self.word = word
        self.type = None
        self.count_pos = 1
        self.count_neg = 1
        self.proba_pos = 0
        self.proba_neg = 0

    def incr_pos(self):
        self.count_pos += 1

    def incr_neg(self):
        self.count_neg += 1

    """ nombre de mot positif,negatif total dans les donnees dentrees """
    def compute_probas(self,nbr_pos,nbr_neg):
        proba_sachant_positif = (self.count_pos)/(nbr_pos)
        proba_sachant_negatif = (self.count_neg)/(nbr_neg)
        proba_word = (self.count_pos+self.count_neg)

        self.proba_pos = (proba_sachant_positif * nbr_pos)/(proba_word)
        self.proba_neg = (proba_sachant_negatif * nbr_neg)/(proba_word)

    def define_type(self):
        if(self.proba_pos > self.proba_neg):
            self.type = Type.positif
        else:
            self.type = Type.negatif