# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 19:16:07 2021

@author: Md Fakrul Islam
"""

from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np

embedder = SentenceTransformer('paraphrase-distilroberta-base-v1')

import numpy as np
import spacy
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
#import nl_core_news_sm
#import gensim
import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import re
import string

#df = pd.read_excel('D:/test_data/all_customer_conversations.xlsx', sheet_name=0)
df = pd.read_excel('D:/test_data/all_customer_conversations.xlsx', sheet_name=0)
#first_reaction = df.iloc[:, 4]
#Customer Speech
first_reaction = df.iloc[:, 8]

print(first_reaction)

listToStr = ' '.join([str(elem) for elem in first_reaction]) 
sentences=listToStr.split('.')
import re
flat_list = []
#text_sentences = nlp(listToStr)
for sentence in sentences:
    s = re.sub(r"^nan+", "", sentence, flags=re.UNICODE) #White space at the begining
    ss = re.sub(r"nan+$", "", s, flags=re.UNICODE) #White space at the end
    sss = " ".join(re.split("nan+", ss, flags=re.UNICODE)) #Duplicate White space at the middle
    #flat_list.append(sentence.text)
    flat_list.append(sss)
    #print(sentence.text)

messages = pd.DataFrame(flat_list,  columns =['Customer_Reaction'])
messages.dropna(subset = ["Customer_Reaction"], inplace=True)
def clean_white_space(x):
    sentence = re.sub(r"^\s+", "", x, flags=re.UNICODE) #White space at the begining
    sentence = re.sub(r"\s+$", "", sentence, flags=re.UNICODE) #White space at the end
    sentence = " ".join(re.split("\s+", sentence, flags=re.UNICODE)) #Duplicate White space at the middle
    return sentence.lower()

messages['text_clean_white_space'] = messages['Customer_Reaction'].apply(clean_white_space)
print(string.punctuation)
def remove_punctuation(x):
    sentence=" ".join("".join([" " if ch in string.punctuation else ch for ch in x]).split())
    return sentence   

messages['text_clean_punctuation'] = messages['text_clean_white_space'].apply(remove_punctuation)


corpus_ws=messages['text_clean_white_space'].to_list()
test_list_corpus_ws = [i for i in corpus_ws if i] 
corpus_ws_pu=messages['text_clean_punctuation'].to_list()
test_list_corpus_ws_pu = [i for i in corpus_ws_pu if i] 

embedder = SentenceTransformer('paraphrase-distilroberta-base-v1')
#test_list_corpus_ws
#test_list_corpus_ws_pu
corpus_embeddings = embedder.encode(test_list_corpus_ws_pu)
#corpus_embeddings = embedder.encode(test_list_corpus_ws)