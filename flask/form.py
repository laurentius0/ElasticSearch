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
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    # Convert to PIL image
    image = wordcloud.to_image()
    buffered = BytesIO()
    image.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue())

    # image.show()
    return render_template("image.html", img_data=urllib.parse.quote(img_str))

if __name__ == '__main__':
    app.run()
