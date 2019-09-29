from crawler.models import Data
from preprocessing import preprocessing_tools as pt
import nltk
from nltk.corpus import stopwords as nltk_stopwords
from matplotlib import pyplot
import numpy as np
from sklearn.model_selection import train_test_split
from os.path import join
from glob import glob

import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.stem.snowball import SnowballStemmer
import pymorphy2
from sklearn.decomposition import LatentDirichletAllocation as LDA
from preprocessing.topic_modeler import TopicModeler



def preprocessing():    
    texts = Data.objects.all().values_list('content', flat=True)[:10]
    print('Numver of texts:', texts.count())

    texts = filter_by_length(texts)
    print('Numver of texts after filtering:', texts.size)

    stopwords = get_stopwords()
    print('Numver of stopwords:', len(stopwords))
    
    train_texts, test_texts = split_on_train_test(texts)
    print('Numver of train and test texts:', len(train_texts), len(test_texts))

    cleaned = tf_idf_filtering(stopwords, train_texts)
    print('Length of vocabulary after filtering:', len(cleaned))

    #stemmed = stemming(cleaned)
    #print('Length of vocabulary after stemming:', len(stemmed))

    lemmatized = lemmatize(cleaned)
    print('Length of vocabulary after lemmatization:', len(lemmatized))

    dataset, count_vect = training_count_vectorizer(lemmatized, stopwords, train_texts)
    lda = training_lda(dataset)

    dataset = count_vect.transform(test_texts)
    tm = TopicModeler(count_vect, lda)
    key_words = tm.get_keywords(test_texts[0], n_topics=1, n_keywords=10)
    print(key_words)


def filter_by_length(texts):
    #Tokenize all texts and collect texts lenghts to see texts lengths distribution
    texts_lens = []
    for text in texts:
        tok_text = nltk.word_tokenize(text)
        tok_text = pt.normalize(tok_text, tokenized=True)
        texts_lens.append(len(tok_text))

    #Texts lengths distribution
    #pyplot.hist(texts_lens, bins=[i * 100 for i in range(int(2000 / 100))])
    #pyplot.show()

    texts_lens = np.array(texts_lens)
    small_texts = np.array(texts)[texts_lens < 10]
    return np.setdiff1d(texts, small_texts)


def get_stopwords():
    #Loading text files with external stopwords
    stopwords_path = join('./stopwords', '*.txt')
    stopwords_files = glob(stopwords_path)
    extra_stopwords = set()
    for name in stopwords_files:
        with open(name, 'r') as f:
            words = f.readlines()
            words = [word.strip() for word in words]
            extra_stopwords.update(set(words))

    #Putting nltk stopwords
    stopwords = set()
    stopwords.update(set(nltk_stopwords.words('english')))
    stopwords.update(set(nltk_stopwords.words('russian')))
    stopwords.update(extra_stopwords)

    stopwords = list(stopwords)
    return stopwords


def split_on_train_test(texts):
    return train_test_split(texts, test_size=0.1, random_state=1)


def tf_idf_filtering(stopwords, train_texts):
    #Training tf-idf vectorizer
    tf_idf = TfidfVectorizer(input='content',
                                 stop_words=stopwords,
                                 smooth_idf=False)
    tf_idf.fit(train_texts)
    #getting idfs
    idfs = tf_idf.idf_
    #sorting out too rare and too common words (original 1.3 and 7)
    lower_thresh = 3.
    upper_thresh = 6.
    not_often = idfs > lower_thresh
    not_rare = idfs < upper_thresh
    mask = not_often * not_rare

    good_words = np.array(tf_idf.get_feature_names())[mask]
    #deleting punctuation
    cleaned = []
    for word in good_words:
        word = re.sub("^(\d+\w*$|_+)", "", word)    
        if len(word) == 0:
            continue
        cleaned.append(word)
    return cleaned


def stemming(cleaned):
    #m = Mystem()

    stemmer = SnowballStemmer("russian")

    stemmed = set()
    voc_len = len(cleaned)
    for i in range(voc_len):
        word = cleaned.pop()
        stemmed_word = stemmer.stem(word)
        stemmed.add(stemmed_word)    
    return list(stemmed)


def lemmatize(cleaned):
    morph = pymorphy2.MorphAnalyzer()
    lemmatized = set()
    voc_len = len(cleaned)
    for i in range(voc_len):
        word = cleaned.pop()
        lemma = morph.parse(word)[0].normal_form
        lemmatized.add(lemma)
    return list(lemmatized)



def training_count_vectorizer(tokens, stopwords, train_texts):
    voc = {word : i for i,word in enumerate(tokens)}
    count_vect = CountVectorizer(input='content',
                                 stop_words=stopwords,
                                 vocabulary=voc)
    return count_vect.fit_transform(train_texts), count_vect


def training_lda(dataset):
    lda = LDA(n_components = 60, max_iter=30, n_jobs=6, learning_method='batch', verbose=1)
    lda.fit(dataset)
    return lda