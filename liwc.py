from __future__ import unicode_literals
import numpy as np
import codecs
import re

class LIWC:
    def __init__(self):
        self.words = []
        self.prefixes = []
        self.dim_map = {}
        self.dic = {}
        self.path = 'lexicons/LIWC2007_Portugues_win.dic'
        self.start_line = 66
        self.create_LIWC_dim_maps()
        self.compute_prefixes_and_words()
        self.create_dictionary()

    def create_LIWC_dim_maps(self):
        dim_idx = 0
        self.dim_map = {}
        with codecs.open(self.path, encoding='latin1') as f:
            for i, l in enumerate(f):
                if i == 0:
                    continue
                l = l.strip()
                if l == '%':
                    break
                given_dim = l.split('\t')[0]
                self.dim_map[given_dim] = dim_idx
                dim_idx += 1

    def compute_prefixes_and_words(self):
        with codecs.open(self.path, encoding='latin1') as f:
            for i, l in enumerate(f):
                if i < self.start_line:
                    continue
                target = l.strip().split('\t')[0]
                if target.endswith('*'):
                    self.prefixes.append(target[:-1])
                else:
                    self.words.append(target)

    def create_dictionary(self):
        with codecs.open(self.path, encoding='latin1') as f:
            for i, l in enumerate(f):
                if i < self.start_line:
                    continue
                l = l.strip().split('\t')
                word, dim = l[0], l[1:]

                if word.endswith('*'):
                    word = word[:-1]

                actual_dims = []
                for d in dim:
                    try:
                        actual_dims.append(self.dim_map[d])
                    except:
                        print(l)
                        print(word)
                        print(dim)
                self.dic[word] = actual_dims
                
    def build_features(self, texts):
        liwc_ret = np.zeros((len(texts), len(self.dim_map)))
        for idx, review in enumerate(texts):
            for word in re.findall(r'\w+', review):
                if word in self.dic:
                    for d in self.dic[word]:
                        liwc_ret[idx][d] += 1
                else:
                    if word.startswith(tuple(self.prefixes)):
                        for item in self.prefixes:
                            if word.startswith(item):
                                for d in self.dic[item]:
                                    liwc_ret[idx][d] += 1
        return liwc_ret