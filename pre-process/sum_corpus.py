import pandas as pd
import numpy as np
from datetime import datetime
from os import walk

for (dirpath, dirnames, filenames) in walk('counts'):
    break

counts = pd.DataFrame(columns=['id', 'countPosts','countTokens', 'countWords', 'countWordsPT',
       'countSentences', 'countSentencesPT', 'countTags', 'countTokens.1',
       'countComments', 'countError'])

for file in filenames:
    if 'csv' in file:
        counts = counts.append(pd.read_csv('counts/'+file))
    #break

print(counts.shape)
print(counts.sum())

for summy in counts.sum():
    print("{:10,.2f}".format(summy))
