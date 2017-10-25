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

@app.route('/advanced-search.html')
def advanced_search():
    return render_template("advanced-search.html")

def build_query(query):
    """
    query: dictionary with results
    """

    k = list(query.keys())

    strQ = ""
    for i in range(len(k)-1):
        # -1 because the last element is my_form, we dont want that
        if query[k[i]] != "":
            strQ += "({0}:{1}) AND".format(k[i], query[k[i]])
    strQ = strQ[:-4]

    q = {"query": {"query_string":{"query" : strQ}}}

    res= es.search(index="database", body=q, size=100)

    return res


@app.route('/searchresultpage_adv/')
def advanced_search_page():
    if request.method=="GET":
        r_dict = request.args.to_dict()
        searchresult = build_query(r_dict)
        if searchresult["hits"]["total"] > 0:
            return render_template("searchresultpage.html", result = searchresult["hits"]["hits"])
        else:
            return render_template("searchresultpage.html", result = "No result found.")
    else:
        return render_template("searchpage.html")

@app.route('/searchresultpage/')
def search_result_page():
    if request.method=="GET":
        searchtext = request.args['query']
        query = getQuery(searchtext)
        searchresult = es.search(index='database',  body=query)
        if searchresult["hits"]["total"] > 0:
            return render_template("searchresultpage.html", result = searchresult["hits"]["hits"])
        else:
            return render_template("searchresultpage.html", result = "No result found.")
    else:
        return render_template("searchpage.html")

@app.route("/wordcloud.png")
def simple():
    import urllib.parse
    import base64

    from io import BytesIO
    from wordcloud import WordCloud

    # Todo: text van queries gebruiken.
    text = "De kaas is een grote ronde dikke kaas die vrij dikke is is een dikke kaas"

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
    return render_template("image.html", img_data=urllib.parse.quote(img_str))

if __name__ == '__main__':
    app.run()
