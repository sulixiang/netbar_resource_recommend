#coding:utf-8
from flask import Blueprint
main = Blueprint('main', __name__)
 
import os, json
from engine import RecommendationEngine
from urllib.parse import unquote
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request, render_template
from time import time
 
@main.route("/resource/add", methods = ["POST"])
def add_sentences():
    t0 = time()
    sentences = request.form['sentences'].strip().split("\n")
    sentences = map(lambda x: x.strip(), sentences)
    recommendation_engine.add_sentences(sentences)
    #from urllib import request as req
    ##通知线上服务重新加载模型
    #f = req.urlopen(req.Request("http://10.0.1.138:1194/flush/engine"))
    #result = f.read()
    #f.close()
    tt = time()-t0
    result = json.dumps("rebuild model sucess in %s seconds" % round(tt,3))
    return render_template('result.html', result=result)

@main.route("/build/model",methods = ["GET"])
def build_model():
    t0 = time()
    dataset_path = os.path.join('datasets')
    recommendation_engine.build_model(dataset_path)
    tt = time()-t0
    result = json.dumps("build model sucess in %s seconds" % round(tt,3))
    return render_template('result.html', result=result)

 
 
def create_app():
    global recommendation_engine 

    recommendation_engine = RecommendationEngine()

    app = Flask(__name__)
    app.register_blueprint(main)
    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=1195, debug=True)
