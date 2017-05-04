import re


class MapperUtils(object):

    def __init__(self):
        pass

    @staticmethod
    def transform_word(w):
        w = w.lower()
        w = re.sub(r'(,\s*?inc)|(,\s*?llc)', '', w)
        w = re.sub(r'(https?)|(www\.)|\.(com|net|org|int|edu|gov|mil|it)|\/$', '', w)
        w = re.sub(r'\W', '', w) # re.sub(r';|-|\s|"|\'|:', '', w) or [;\-\s\(\)\!=\+\?:\/"\|\\']
        # r'^xaxis' is one word that we can remove
        return w

