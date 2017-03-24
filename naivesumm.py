# NaiveSumm is a naive summarization approach based on Luhn1958 work
# "The Automatic Creation of Literature Abstracts"
# It uses the frequencies of words in the document in order to 
# calculate and extract the sentences that include the most frequent words.

# Copyright (C) 2012 Alejandro Mosquera <amsqr2@gmail.com>
 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist 
from nltk.corpus import stopwords


class NaiveSummarizer:

	
	def summarize(self, input, num_sentences ):

		punt_list=['.',',','!','?']
		summ_sentences = []

		sentences = sent_tokenize(input, language='portuguese')
		lowercase_sentences =[sentence.lower() 
			for sentence in sentences]
		#print lowercase_sentences
		
		s=list(input)
		ts=''.join([ o for o in s if not o in  punt_list ]).split()
		lowercase_words=[word.lower() for word in ts]
		words = [word for word in lowercase_words if word not in stopwords.words()]
		word_frequencies = FreqDist(words)
		
		most_frequent_words = [pair[0] for pair in 
			word_frequencies.most_common(50)]

                # add sentences with the most frequent words
		for word in most_frequent_words:
			for i in range(0, len(lowercase_sentences)):
				if len(summ_sentences) < num_sentences:
					if (lowercase_sentences[i] not in summ_sentences and word in lowercase_sentences[i]):
						summ_sentences.append(sentences[i])
						break
                                        
			
		# reorder the selected sentences
		# summ_sentences.sort( lambda s1, s2: input.find(s1) - input.find(s2) )
		return " ".join(summ_sentences)