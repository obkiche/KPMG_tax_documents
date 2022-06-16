import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import nltk
nltk.download('stopwords') 
nltk.download('wordnet')
from nltk.corpus import stopwords

# For one text

def keywords(text):
    string = text
    '--------------------------'
    
    def pre_process(string):
        # lowercase
        string =string.lower()
    
        #remove tags
        string =re.sub("</?.*?>"," <> ",text)
    
        # remove special characters and digits
        string =re.sub("(\\d|\\W)+"," ",text)
    
        return string
    
    article = pre_process(string)
    
    '--------------------------'
    #load a set of stop words
    stop_words= stopwords.words("dutch")
    stop_words.extend(['bis', 'NL', 'FR','artikel', "januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"])
    
    #get the text 
    
    docs=[article]  
    
    #create a vocabulary of words, 
    #ignore words that appear in 85% of documents, 
    #eliminate stop words
    cv=CountVectorizer(stop_words=stop_words)
    word_count_vector=cv.fit_transform(docs)
    
    # transform it to tf-idf vector
    
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    
    '--------------------------'
    
    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    '--------------------------'
    
    def extract_topn_from_vector(feature_names, sorted_items, topn=10):
        """get the feature names and tf-idf score of top n items"""
    
        #use only topn items from vector
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        for idx, score in sorted_items:
            fname = feature_names[idx]
        
        #keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        #create a tuples of feature,score
        #results = zip(feature_vals,score_vals)
        results= {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]]=score_vals[idx]
        
        return results
    
    '--------------------------'
    
    # you only needs to do this once
    feature_names=cv.get_feature_names()
    
    result_list=[]
    def get_keywords(x):

        #generate tf-idf for the given document
        tf_idf_vector=tfidf_transformer.transform(cv.transform(x))

        #sort the tf-idf vectors by descending order of scores
        sorted_items=sort_coo(tf_idf_vector.tocoo())

        #extract only the top n; n here is 10
        keys=extract_topn_from_vector(feature_names,sorted_items,10)
        
        result_list.append(list(keys.keys()))
        return result_list
    
    end = get_keywords(docs)
    return end