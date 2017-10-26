# import all necessary libraries
import os
import sys
import pickle
from elasticsearch import Elasticsearch

# index name
index_name = 'uvascripties'

# type name
type_name = 'scripties'

# host of the elasticsearch service
HOST = 'localhost:9200'

# get instance of elasticsearch
es = Elasticsearch(hosts=[HOST])



def index(path = '/home/pieter/Documents/Zoekmachines dataset 5+GB/pdfdata/',
          ndocs = 10):
    '''
    path:  path to the data (json format) that needs to be indexed
    ndocs: number of documents to be indexed from the folder above
    '''

    # list all files in the data folder
    docnames = os.listdir(path)
    # index all files that end with .pkl
    for i, picklename in enumerate([docname for docname in docnames[:ndocs] if docname[-3:] == "pkl"]):
        if (picklename[:-3] + "txt" in docnames):
            file = pickle.load(open(path + picklename, "rb"))
            file["Author"] = file[" Author"]
            del file[" Author"]
            file["Download"] = file["Download"].replace('http://www.scriptiesonline.uba.uva.nl/', 'http://www.arno.uva.nl/')
            with open(path + picklename[:-3] + "txt", 'r') as textfile:
                file["Text"] = ''.join([line[:-1] for line in textfile.readlines()])
                 # textfile.read()
            es.index(index=index_name, doc_type=type_name, id=i, body=file)

    return i+1

def test(total_indexed):
    '''
    Test if 'total_indexed' is the number of elements in the database.

    total_indexed: number of elements that was put into the database
    '''

    query = {
        'query' : {
            'match_all': {}
        }
    }
    result = es.search(index = index_name, doc_type = type_name, body=query)

    print("Total files indexed: ", total_indexed)
    print("Total successfully indexed: ", result["hits"]["total"])
    if (total_indexed == result["hits"]["total"]):
        print("Test successful!")
    else:
        print("Test failed!")


def help():
    print("Usage: \"python bulk_index_files.py\"")
    print("Usage: \"python bulk_index_files.py <path_to_folder> <number_of_docs_to_parse>\"")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        n_indexed = index()
        test(n_indexed)
    elif len(sys.argv) == 3:
        n_indexed = index(sys.argv[1], int(sys.argv[2]))
        test(n_indexed)
    else:
        help()