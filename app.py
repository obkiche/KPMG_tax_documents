from flask import Flask,render_template,url_for,request
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib


from Summarizer import summarize
from Getting_keywords_for_one_text import keywords
from Getting_relevancy_scores import cosine_score



app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
	if request.method == 'POST':
		message = request.form['message']
		summarized = summarize(message)
		keyworded = keywords(message)
		scored = cosine_score(message)
	return render_template('result.html',summaries = summarized, keywords=keyworded,scores=scored)

if __name__ == '__main__':
	app.run(debug=True)