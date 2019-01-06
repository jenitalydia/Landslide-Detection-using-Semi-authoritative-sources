from gensim.models import KeyedVectors
import json
import numpy as np
import nltk
import pandas as pd
nltk.download('punkt')
import pdb

def load_vector():


    model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True,unicode_errors='ignore',limit=2000)

    tweet_data = '/Users/jenita/PycharmProjects/TweetFinder/data/cat.json'

    mean_vector = []

    df = pd.DataFrame()
    df2 = pd.DataFrame()

    with open(tweet_data,'r') as tweets:
        for line in tweets:
            line = json.loads(line.strip())
            sentence = line['text']
            word = nltk.word_tokenize(sentence)
            count = 0
            embeddings = np.zeros(300)
            for w in word:
                if w in model:
                    vector = model[w]
                    embeddings += vector
                    count = count + 1

            mean = embeddings/count
            mean_vector.append(mean)
            df2 = pd.DataFrame([[mean, line['label']]], columns = ['vector', 'label'])
            df = df.append(df2, ignore_index = True)
            print df




if __name__ == "__main__":
    load_vector()