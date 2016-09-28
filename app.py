#coding:utf-8
from flask import Blueprint, Flask, request, render_template, redirect, url_for
main = Blueprint('main', __name__)
 
import os, json
from engine import RecommendationEngine
from urllib.parse import unquote
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 

@main.route("/", methods=["GET"])
def index():
    return redirect(url_for('static',filename='index.html'))
 
@main.route("/vec/<resource>", methods=["GET"])
def resource_vec(resource):
    logger.debug("Resource %s vec requested", resource)
    resource_vec = {}
    resource_vec['resource'] = resource
    resource_vec['vec'] = recommendation_engine.get_vec([resource]).tolist()[0]
    #return json.dumps(resource_vec)
    return render_template('result.html', result=json.dumps(resource_vec))
 
@main.route("/ranking", methods=["POST"])
def ranking_by_similar():
    form = request.form
    positive = form['positive'].strip().split(",") 
    negative = form['negative'].strip().split(",") 
    rawdata = form['rawdata'].strip().split(",") 
    result = recommendation_engine.get_ranking_by_similar(positive,negative,rawdata)
    #return json.dumps(result)
    return render_template('result.html', result=json.dumps(result))
 
@main.route("/top/<int:topn>", methods=["POST"])
def get_topn(topn):
    form = request.form
    positive = form['positive'].strip().split(",") 
    negative = form['negative'].strip().split(",") 
    result = recommendation_engine.get_most_similar(positive,negative,topn)
    #return json.dumps(result)
    return render_template('result.html', result=json.dumps(result))
 
@main.route("/flush/engine", methods=["GET"])
def reload_model():
    result = recommendation_engine.reload_model()
    result=json.dumps('reload model sucess')
    return render_template('result.html', result=result)
 
def create_app():
    global recommendation_engine 

    recommendation_engine = RecommendationEngine()    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=1194, debug=True)
