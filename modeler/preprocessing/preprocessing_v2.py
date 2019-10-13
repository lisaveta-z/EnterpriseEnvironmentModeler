from crawler.models import Data
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction

from preprocessing import preprocessing as v1

def preprocessing():    
    texts = Data.objects.all().values_list('content', flat=True)[:10]
    print('Numver of texts:', texts.count())

    stopwords = v1.get_stopwords()
    print('Numver of stopwords:', len(stopwords))