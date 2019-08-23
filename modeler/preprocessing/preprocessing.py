from crawler.models import Data
import sqlite3
import re
import nltk
from nltk.corpus import stopwords


nltk.download('punkt')
nltk.download('stopwords')

def preprocessing():
    print(Data.objects.count())
    texts = Data.objects.all().values('content')[:10]
    for text in texts:
        print(text['content'])
        print('\n')
        print(normalize(text['content'], del_stopwords = True))
        print('\n')



def delete_non_letters(words):
    new_words = []
    for word in words:
        new_word = "".join(c for c in word if c.isalpha())
        if new_word != '':
            new_words.append(new_word)
    return new_words

def delete_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english') and word not in stopwords.words('russian'):
            new_words.append(word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def normalize(text, tokenized=False, del_stopwords=False):
    if not tokenized:
        text = nltk.word_tokenize(text)
    
    text = delete_non_letters(text)
    if del_stopwords:
        text = delete_stopwords(text)
        
    text = to_lowercase(text)
    
    text = [word for word in text if len(word) > 1]
    return text

#def cleanSentences(string):
#    strip_special_chars = re.compile("[^А-Яа-я\xa0 ]+")
#    #string = string.lower().replace("<br />", " ")
#    string = re.sub()
#    string = re.sub(r'\w+\-\w+','', string)
#    string = re.sub(r'@\w+','',string) # Delete @* references
#    string = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',' ', string) # Delete http(s):// links
#    string = re.sub(strip_special_chars, "", string.lower())
#    string = re.sub("\s\s+", " ", string.strip())
#    return string

    #    for index, row in df.iterrows():
     #   row["content"] = cleanSentences(row["content"])

        # print("Raw data head:", df.head(100))

#preprocessing()