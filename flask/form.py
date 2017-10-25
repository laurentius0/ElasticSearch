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
    query = {"query": {"query_string": {"query" : text}}}
    return query

@app.route('/searchresultpage/')
def search_result_page():
    if request.method=="GET":
        searchtext = request.args['query']
        query = getQuery(searchtext)
        searchresult = es.search(index='database',  body=query)
        if searchresult["hits"]["total"] > 0:
            all_abstracts = ''
            for result in searchresult["hits"]["hits"]:
                if 'Abstract' in result['_source'].keys():
                    all_abstracts = all_abstracts + result['_source']['Abstract']
                    all_abstracts = clean_text(all_abstracts)
            cloud_image = generateWordCloud(all_abstracts)
            return render_template("searchresultpage.html", result = searchresult["hits"]["hits"], cloud = cloud_image)
        else:
            return render_template("searchresultpage.html", result = "No result found.", cloud = 0)
    else:
        return render_template("searchpage.html")

def clean_text(text):
    words = text.lower().split(" ")
    words = list(filter(lambda a: a not in ['thesis', 'de', 'het', 'deze', 'wordt', 'een', 'voor', 'en', 'zijn', 'aan', 'van', 'dat', 'op', 'werd', 'met', 'er', 'als', 'te', 'uit', 'dit', 'om', 'tussen', 'geen', 'heeft', 'ook'], words))
    return ' '.join(words)

def generateWordCloud(text):
    import urllib.parse
    import base64

    from io import BytesIO
    from wordcloud import WordCloud

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)


    # Convert to PIL image
    image = wordcloud.to_image()
    buffered = BytesIO()
    image.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue())

    # image.show()
    return urllib.parse.quote(img_str)

if __name__ == '__main__':
    app.run()
