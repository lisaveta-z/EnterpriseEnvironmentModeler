from crawler.models import Data
from preprocessing import preprocessing_tools as pt
import sqlite3
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from matplotlib import pyplot
import numpy as np
#from numpy.random import choice

#import nltk
from nltk.corpus import stopwords as nltk_stopwords

from sklearn.model_selection import train_test_split

from os.path import join
from glob import glob

#from tqdm import tqdm_notebook as tqdm

import pickle

#from os import mkdir 
#from shutil import move

def preprocessing():
    print(Data.objects.count())
    texts = Data.objects.all().values_list('content', flat=True)[:10]
    texts_lens = tokenize(texts)
    texts = filter_by_length(texts, texts_lens)
    print(texts.size)
    stopwords = get_stopwords()
    train_names, test_names = split_on_train_test(texts)
    print(len(train_names), len(test_names))


def tokenize(texts):
    #Let`s tokenize all texts and collect texts lenghts to see texts lengths distribution.
    texts_lens = []
    for text in texts:
        tok_text = nltk.word_tokenize(text)
        tok_text = pt.normalize(tok_text, tokenized=True)
        texts_lens.append(len(tok_text))

    #texts lengths distribution
    #pyplot.hist(texts_lens, bins=[i * 100 for i in range(int(2000 / 100))])
    #pyplot.show()
    return texts_lens


def filter_by_length(texts, texts_lens):
    texts_lens = np.array(texts_lens)
    small_texts = np.array(texts)[texts_lens < 10]
    return np.setdiff1d(texts, small_texts)


def get_stopwords():
    stopwords_path = join('./stopwords')
    stopwords_template = join(stopwords_path, '*.txt')
    stopwords_files = glob(stopwords_template)
    extra_stopwords = set()
    for name in stopwords_files:
        with open(name, 'r') as f:
            words = f.readlines()
            words = [word.strip() for word in words]
            extra_stopwords.update(set(words))

    #Also putting there nltk stopwords
    stopwords = set()
    stopwords.update(set(nltk_stopwords.words('english')))
    stopwords.update(set(nltk_stopwords.words('russian')))
    stopwords.update(extra_stopwords)

    stopwords = list(stopwords)
    print('Total numver of stopwords:', len(stopwords))
    return stopwords


def split_on_train_test(texts):
    return train_test_split(texts, test_size=0.1, random_state=1) 