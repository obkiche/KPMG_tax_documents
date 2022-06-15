import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import nltk
nltk.download('stopwords') 
nltk.download('wordnet')
from nltk.corpus import stopwords

# Going through a csv file

def keywords_csv(filepath):
    df_idf= pd.read_csv(filepath)
    
    # Removing German translations.
    
    df_idf= df_idf[df_idf["Text"].str.contains("Duitse vertaling")==False]
    
    def pre_process(text):
    
        # lowercase
        text=text.lower()
    
        #remove tags
        text=re.sub("</?.*?>"," <> ",text)
    
        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
    
        return text

    df_idf['Text'] = df_idf['Text'].apply(lambda x:pre_process(x))

    #load a set of stop words
    
    stop_words= stopwords.words("dutch")
    stop_words.extend(['bis', 'NL', 'FR','artikel', "januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"])

    #get the text column 
    
    docs=df_idf['Text'].tolist()
    docs_title=df_idf['Title'].tolist()
    
    #create a vocabulary of words, 
    #ignore words that appear in 85% of documents, 
    #eliminate stop words
    cv=CountVectorizer(max_df=0.85,stop_words=stop_words)
    word_count_vector=cv.fit_transform(docs)
    
    # Call TfidTransformer
    
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    
    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

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
    
    # you only needs to do this once
    feature_names=cv.get_feature_names()

    # put the common code into several methods
    def get_keywords(idx):

        #generate tf-idf for the given document
        tf_idf_vector=tfidf_transformer.transform(cv.transform([docs[idx]]))

        #sort the tf-idf vectors by descending order of scores
        sorted_items=sort_coo(tf_idf_vector.tocoo())

        #extract only the top n; n here is 10
        keywords=extract_topn_from_vector(feature_names,sorted_items,10)
    
        return keywords

       #generate tf-idf for all documents in your list.
    tf_idf_vector=tfidf_transformer.transform(cv.transform(docs))

    results=[]
    for i in range(tf_idf_vector.shape[0]):
    
        # get vector for a single document
        curr_vector=tf_idf_vector[i]
    
        #sort the tf-idf vector by descending order of scores
        sorted_items=sort_coo(curr_vector.tocoo())

        #extract only the top n; n here is 10
        keywords=extract_topn_from_vector(feature_names,sorted_items,10)
    
        results.append(list(keywords.keys()))

    df=pd.DataFrame(zip(docs,results),columns=['doc','keywords'])
    
    return df.head()