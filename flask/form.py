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
    for i in range(len(k)):
        if query[k[i]] != "":
            strQ += "({0}:{1}) AND".format(k[i], query[k[i]])
    strQ = strQ[:-4]

    q = {"query":  {"query_string":{"query" : strQ}}}
    res= es.search(index="database", body=q, size=10)

    return res


def add_facets(results):
    """
    only returns faculty for now, can optionally do more.
    """
    r = {}
    for i in results:
        if "Faculty" in i['_source'].keys():
            if i['_source']['Faculty'] in r.keys():
                r[i['_source']['Faculty']] += 1
            else:
                r[i['_source']['Faculty']] = 1
    return r


@app.route('/searchresultpage_adv/')
def advanced_search_page():
    if request.method=="GET":
        r_dict = request.args.to_dict()
        searchresult = build_query(r_dict)
        if searchresult["hits"]["total"] > 0:

            # Add all faculties for faceted search:
            searchresult['hits']['hits'] = [add_facets(searchresult['hits']['hits'])] + searchresult['hits']['hits']
            searchresult['hits']['hits'] = searchresult['hits']['hits'][:10]

            for result in searchresult["hits"]["hits"][1::]:
                if 'Abstract' in result['_source'].keys():
                    abstracts = result['_source']['Abstract']
                    abstracts = clean_text(abstracts)
                    result['_source']['wordcloud'] = generateWordCloud(abstracts)
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
        searchresult = es.search(index='database',  body=query, size=1000)
        if searchresult["hits"]["total"] > 0:

            # Add all faculties for faceted search:
            searchresult['hits']['hits'] = [add_facets(searchresult['hits']['hits'])] + searchresult['hits']['hits']
            searchresult['hits']['hits'] = searchresult['hits']['hits'][:10]
            
            # create hist
            histogramdata = create_hist(searchresult["hits"]["hits"])

            for result in searchresult["hits"]["hits"][1::]:
                if 'Abstract' in result['_source'].keys():
                    abstracts = result['_source']['Abstract']
                    abstracts = clean_text(abstracts)
                    result['_source']['wordcloud'] = generateWordCloud(abstracts)
            return render_template("searchresultpage.html", result = searchresult["hits"]["hits"], histogram = histogramdata)
        else:
            return render_template("searchresultpage.html", result = "No result found.")
    else:
        return render_template("searchpage.html")

def clean_text(text):
    words = text.lower().split(" ")
    words = list(filter(lambda a: a not in ['also', 'waardoor', 'gaan', 'gaat','die', 'hun', 'paragraaf', 'kernpunten', 'niet','geeft', 'meer', 'thesis', 'de', 'het', 'deze', 'wordt', 'een', 'voor', 'en', 'zijn', 'aan', 'van', 'dat', 'op', 'werd', 'met', 'er', 'als', 'te', 'uit', 'dit', 'om', 'tussen', 'geen', 'heeft', 'ook'], words))
    return ' '.join(words)

def create_hist(results):
    import numpy as np
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt
    import base64
    import urllib.parse

    from io import BytesIO

    yearList = []
    for result in results:
        try:
            yearList += [int(result['_source']['Year'])]
        except:
            pass
    x = yearList
    print(x)
    print("bins",np.arange(max(x) - min(x)) + min(x))
    plt.figure(figsize=(10, 4))
    n, bins, patches = plt.hist(x, bins=np.arange(max(x) + 2 - min(x)+2) + min(x)-1, facecolor='green', align='left', normed=True, rwidth=0.9)
    plt.xticks(np.arange(max(x) + 2 - min(x) + 2) + min(x)-1, rotation='45')
    f = plt.gca()
    f.axes.yaxis.set_ticklabels([])
    f.axes.yaxis.set_visible(False)
    f.spines['top'].set_visible(False)
    f.spines['left'].set_visible(False)
    f.spines['right'].set_visible(False)
    buffered = BytesIO()
    plt.savefig(buffered, format='png', dpi=100)
    img_str = base64.b64encode(buffered.getvalue())
    return urllib.parse.quote(img_str)

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
