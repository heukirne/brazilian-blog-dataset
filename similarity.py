#!/usr/bin/python
import math
import json

#idf score calculation
def idf(word_tokens, words, N):
    dict = {}
    for word in words:
        for sent in word_tokens:
            if word in sent:
                if word in dict.keys():
                    dict[word] += 1

                else:
                    dict[word] = 1
    for word, count in dict.items():
        dict[word] = math.log((N/float(count)))
    with open("idfBg","w") as f:
        json.dump(dict, f)
    return dict

#centrality score calculation
def idf_modified_cosine(x, y, idf):
    try:
        sum = 0
        combine = x + y
        for word in combine:
            tf1, tf2 = x.count(word), y.count(word)
            sum += int(tf1) * int(tf2) * float((idf[word] ** 2))
            total1, total2 = 0, 0
        for word in x:
            tf = x.count(word)
            total1 += int(tf) * float(idf[word])
        for word in y:
            tf = y.count(word)
            total2 += int(tf) * float(idf[word])
        deno = (math.sqrt((total1**2))) * (math.sqrt((total2**2)))
        return float(sum)/deno
    except Exception as e:
        pass


#for investigation puspose
def get_similarity_matrix(word_tokens, idf):
    matrix = []
    for sent1 in word_tokens:
        row = []
        for sent2 in word_tokens:
            sim = idf_modified_cosine(sent1, sent2, idf)
            row.append(sim)
        matrix.append(row)
    return matrix


