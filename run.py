from flask import Flask, render_template, request, redirect, url_for
import os
import json
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key='7eb93ec8c9b1f828f3b6cc0798e7594a1b06dcc6')

app = Flask(__name__)

port = int(os.getenv('VCAP_APP_PORT', 8080))

@app.route('/')
def index_load():      
	return render_template('index.html')

def extract_concept(input_text):
	return (json.dumps(alchemy_language.concepts(text=input_text), indent=2))
  
@app.route('/CV/')
def load_cv_form():
	return render_template('name.html')
	
@app.route('/CV/', methods=['POST'])
def cv_form():
	name = request.form['fullname']
	cv = request.form['CV']
    
	print "Name: ", name
	print "CV: ", cv
	
	#Get concept
	result = alchemy_language.concepts(text=cv)
	concept_list = result["concepts"]
	page = "<title>Person Concepts </title>"
	page += "<h1>Person Concepts </h1>"
	page += "<br><br>"
	
	for item in concept_list:
		concept = item["text"]
		relevance = item["relevance"]
		print "Concept: ", concept
		print "Relevance: ", relevance
		page += "Concept: " + concept + "<br/>"
		page += "Relevance: " + relevance + "<br/><br/><br/>"
	return page
#	return redirect(url_for("index_load"))
	
@app.route('/job/')
def load_job_form():
	return render_template('job.html')

@app.route('/job/', methods=['POST'])
def job_form():
	title = request.form['jobtitle']
	job_des = request.form['job_des']
   
	print 'Job Title: ', title
	print 'Job Description: ', job_des
	
	#Get concepts
	result = alchemy_language.concepts(text=job_des)
	print "Result len = ", len(result)
	print "Type = ", type(result)
	
	concept_list = result["concepts"]
	page = "<title>Job Concepts </title>"
	page += "<h1>Job Concepts </h1>"
	page += "<br><br>"
	
	for item in concept_list:
		concept = item["text"]
		relevance = item["relevance"]
		print "Concept: ", concept
		print "Relevance: ", relevance
		page += "Concept: " + concept + "<br/>"
		page += "Relevance: " + relevance + "<br/><br/><br/>"
	return page
#	return redirect(url_for("index_load"))
	
@app.route('/', methods=['POST'])
def index():
    if request.form['submit'] == 'Enter CV':
        return redirect(url_for("load_cv_form"))
                
    elif request.form['submit'] == 'Enter Job':
        return redirect(url_for("load_job_form"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
