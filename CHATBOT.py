from flask import Flask
from flask import request
from flask import render_template
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
import matplotlib.pyplot as plt
import MySQLdb
from pandas.io import sql
from sqlalchemy import create_engine
import re
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

data = pd.read_csv('cleanedmrdata.csv',error_bad_lines=False, engine= 'python')
data= pd.DataFrame(data)
df = data.drop(['CurrentAffairs','Education','Music','Philosophy','PoliticalScience','Science','History','Law','Games','Books','FoodandDrink','DataSource','WebTech','Economics','Medicine'], axis=1)
engine = create_engine("mysql://root:@localhost/data"'?charset=utf8')
df.to_sql(name='chatbot', con=engine,flavor=None, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)

stops = set(stopwords.words("english"))
def cleanData(text):
    txt = str(text)
    txt = re.sub(r'[^A-Za-z0-9\s]',r'',txt)
    txt = re.sub(r'\n',r' ',txt) #instead of newline we input corpus with a space 
    txt = " ".join([w.lower() for w in txt.split()])  #convert to lowercase
    txt = " ".join([w for w in txt.split() if w not in stops]) #remove stopwords
    return txt

a= ['author','title','wrote']
db = MySQLdb.connect("localhost","root","","data" )

app = Flask(__name__)

chatbot.train("chatterbot.corpus.english")

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():

    txt = request.form['text']
    txt = cleanData(txt)
    txt = str(txt)
    txt = txt.split(" ")
    col = ['author','comment','date','text','title','wordcount','time','number','count','word']
    k = list(set(txt).intersection(col))
    if len(k) ==0:
        return str(chatbot.get_response(txt))
    else:
        if len(set(a).intersection(set(txt))) > 0:
            text = request.form['text']
            text = cleanData(text)
            k = text.split(" ")
            k.remove(a[0])
            k.remove(a[1])
            k.remove(a[2])
            k = " ".join(k)
            k=str(k)
            query = "SELECT author from chatbot where title ='" + k + "';"
            cursor = db.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results[0][0]
if __name__ == '__main__':
    app.run()