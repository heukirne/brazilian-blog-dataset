import pandas as pd
import nltk
from nltk import sent_tokenize, word_tokenize
import sys

print(sys.argv)

sent_tokenizer_pt = nltk.data.load('tokenizers/punkt/portuguese.pickle')
reg_tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

chunck = 50 * 1000
#skiprows = (int(sys.argv[1]) * chunck) + 1
num = str(sys.argv[1])


posts = pd.read_csv('jq_posts/posts_' + str(num) + '.csv', header=None, error_bad_lines=False, verbose=True)
#posts = pd.read_csv('jq_posts/posts_99.csv', header=None, error_bad_lines=False, 
#						verbose=True, nrows=chunck, skiprows=skiprows)

print(posts.shape)
print(posts.columns)

countPosts = 0
countTokens = 0
countWords = 0
countWordsPT = 0
countSentences = 0
countSentencesPT = 0
countTags = 0
countComments = 0
countError = 0

columns = ['countPosts','countTokens', 'countWords', 'countWordsPT', 'countSentences', 'countSentencesPT',
			'countTags' , 'countTokens', 'countComments', 'countError']

filename = 'counts/'+str(sys.argv[1])+'.csv'
#if False:
for index, row in posts.iterrows():
	countPosts += 1
	#if True:
	try:
		content = row[4]
		countTokens += len(content.split(' '))
		countWords += len(word_tokenize(content, language='portuguese'))
		countSentences += len(sent_tokenize(content, language='portuguese'))
		countWordsPT += len(reg_tokenizer.tokenize(content))
		countSentencesPT += len(sent_tokenizer_pt.tokenize(content))
		countComments += int(row[7])
		#print(type(row[8]))
		if type(row[8]) is str:
			countTags += len(row[8])
			#print(str(row[8]))
	except:
		countError += 1


	if True:
		if index % 10000 == 0:				
			#break
			values = [countPosts, countTokens, countWords, countWordsPT, countSentences, countSentencesPT,
						countTags, countTokens, countComments, countError]

			pd.DataFrame([values], columns=columns).to_csv(filename)


values = [countPosts, countTokens, countWords, countWordsPT, countSentences, countSentencesPT,
			countTags, countTokens, countComments, countError]

pd.DataFrame([values], columns=columns).to_csv(filename)

print("Done: ", filename)
