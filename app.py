__author__ = 'cangcang'
from flask import Flask, render_template, request, session, redirect, url_for
from elasticsearch import Elasticsearch
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_cors import *
import json

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['DEBUG'] = True
CORS(app, supports_credentials=True)

@app.route('/')
def home():
    return redirect('../templates/advancedSearch.html')

@app.route('/fullSearch/', methods=['GET', 'POST'])
def fullSearch():
    if request.method == 'POST':
        requestdata1= request.get_data()
        return redirect(url_for('searchResult', query=requestdata1, type='fullType'))
    else:
        return redirect('../templates/Result.html')

@app.route('/advancedSearch/', methods=['GET', 'POST'])
def advancedSearch():
    if request.method=='POST':
        requestdata2=request.get_data()
        return redirect(url_for('searchResult', query=requestdata2, type='advancedType'))
    else:
        return redirect(url_for('home'))

@app.route('/searchResult/', methods=['GET', 'POST'])
def searchResult():
    if request.values.get('type') == 'fullType':
        query = request.values.get('query')
        es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
        res = es.search(
            index='douban',
            body={
                "query":{
                    "multi_match": {
                        "query": query,
                        "type":                 "best_fields",
                        "fields":               [ "authorIntro.cn", "title.cn^10","contentIntro.cn^5"],
                        "minimum_should_match": "50%"
                         }
                 },
                "highlight" : {
                    "pre_tags" : ["<mark>"],
                    "post_tags" : ["</mark>"],
                    "fields": {
                        "authorIntro.cn":  {},
                        "title.cn": {},
                        "contentIntro.cn":{}
                     }
                }
            }
        )
        for e in res['hits']['hits']:
            e['_source']['title2']=e['_source']['title']
            e['_source']['contentIntro2']=e['_source']['contentIntro']
            e['_source']['authorIntro2']=e['_source']['authorIntro']

        i=0
        while i<res['hits']['total']:
            if 'title.cn' in res['hits']['hits'][i]['highlight'].keys():
                res['hits']['hits'][i]['_source']['title']="\n".join(str(e) for e in res['hits']['hits'][i]['highlight']['title.cn'])
            if 'contentIntro.cn' in res['hits']['hits'][i]['highlight'].keys():
                res['hits']['hits'][i]['_source']['contentIntro'] = "\n".join(str(e) for e in res['hits']['hits'][i]['highlight']['contentIntro.cn'])
            if 'authorIntro.cn' in res['hits']['hits'][i]['highlight'].keys():
                res['hits']['hits'][i]['_source']['authorIntro'] = "\n".join(str(e) for e in res['hits']['hits'][i]['highlight']['authorIntro.cn'])
            i=i+1
        return json.dumps(res)
    elif request.values.get('type') == 'advancedType':
        query = request.values.get('query')
        es = Elasticsearch()
        res = es.search(
            index='douban',
            doc_type='newbook',
            body=query
        )
        for e in res['hits']['hits']:
            e['_source']['title2']=e['_source']['title']
            e['_source']['contentIntro2']=e['_source']['contentIntro']
            e['_source']['authorIntro2']=e['_source']['authorIntro']
        i=0
        while i < res['hits']['total']:
            if 'title' in res['hits']['hits'][i]['highlight'].keys():
                res['hits']['hits'][i]['_source']['title']="\n".join(str(e) for e in res['hits']['hits'][i]['highlight']['title'])
            if 'contentIntro' in res['hits']['hits'][i]['highlight'].keys():
                res['hits']['hits'][i]['_source']['contentIntro'] ="\n".join(str(e) for e in res['hits']['hits'][i]['highlight']['contentIntro'])
            if 'authorIntro' in res['hits']['hits'][i]['highlight'].keys():
                res['hits']['hits'][i]['_source']['authorIntro'] = "\n".join(str(e) for e in res['hits']['hits'][i]['highlight']['authorIntro'])
            i=i+1
        return json.dumps(res)

# @app.error_handler(404)
# def page_not_found(e):
#     render_template('404.html'),404
#
# @app.error_handler(500)
# def internal_server_error(e):
#     return render_template('500.html'),500

if __name__ == '_main_':
    app.debug = True
    app.run()