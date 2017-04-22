import os, sys

sys.path.append("./pylinguistics/pylinguistics/")

import Pylinguistics as pl #imcompatible with python 3
import pandas as pd
import numpy as np

import unicodedata

def remove_accents(input_str):
	#encoding = "utf-8"
	#byte_string = b(input_str)
	#unicode_string = byte_string.decode(encoding)
	nfkd_form = unicodedata.normalize('NFKD', unicode(input_str, 'utf8'))
	only_ascii = nfkd_form.encode('ASCII', 'ignore')
	return only_ascii

corpus = pd.read_csv('corpus.csv.gz', compression='gzip')

df = {}
columns = []

for idx in corpus.index.values:
	text = corpus.content[idx]
	objpl = pl.text(remove_accents(text))
	objpl.language = "pt";
	
	post_pd = []

	if columns == []:
		for attr in objpl.getFeatures():
			columns.append(attr)
		columns.append('class')

	for attr in objpl.getFeatures():
		post_pd.append(str(objpl.getFeatures()[attr]))
	post_pd.append(corpus['qual_a_melhor_classificao_para_esse_texto'][idx])

	df[idx] = post_pd
	print(idx)


posts = pd.DataFrame.from_dict(df, orient='index')
posts.columns = columns
posts.to_csv('corpus_readability.csv.gz', compression='gzip')