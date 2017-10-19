from flask import Flask
from flask import request
from flask import render_template

from elasticsearch import Elasticsearch

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return render_template("result-form.html", text = processed_text)

@app.route('/searchpage/')
def search_page():
    return render_template("searchpage.html")

def getQuery(text):
    query =  {"query": { "match": { "Abstract": text} },"size": 1 }
    return query

@app.route('/searchresultpage/')
def search_result_page():
    if request.method=="GET":
        searchtext = request.args['query']
        query = getQuery(searchtext)
        searchresult = es.search(index='uvascripties', doc_type='scripties', body=query)
        if searchresult["hits"]["total"] > 0 and "Abstract" in searchresult["hits"]["hits"][0]["_source"]:
            return render_template("searchresultpage.html", result = searchresult["hits"]["hits"][0]["_source"]["Abstract"])
        else:
            return render_template("searchresultpage.html", result = "No abstract")
    else:
        return render_template("searchpage.html")

if __name__ == '__main__':
    app.run()
