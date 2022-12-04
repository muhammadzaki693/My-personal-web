import os
import replit
import glob
import json
import sys
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite
import pygments
from replit import db
from datetime import datetime
from flask import Flask, render_template, url_for, request, jsonify
from pygments.formatters import HtmlFormatter

port = os.environ.get('PORT', 8080)

for apifile in glob.glob("api/*.json"):
	with open(apifile) as f:
		globals()[apifile.rsplit("/",1)[1].rsplit(".",1)[0]] = json.load(f)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.template_filter('autoversion')
def autoversion_filter(filename):
	fullpath = os.path.join(os.path.dirname(__file__), filename[1:])
	try:
		timestamp = os.path.getmtime(fullpath)
	except OSError:
		return filename
	newfilename = "{0}?v={1}".format(filename, timestamp)
	return newfilename

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api", defaults={"query":""})
@app.route('/api/<string:query>')
def api(query):
	if query == "":
		return jsonify({"error":"you didnt provide any api"})
	return jsonify(globals()[query]) if query in globals() else jsonify({"error":"api doesnt exist"})

@app.route("/zakipy")
def zakipy():
	formatter = HtmlFormatter(style="emacs",full=True,cssclass="codehilite")
	css_string = formatter.get_style_defs()
	md_css_string = "<style>"+css_string+"</style>"
	readme_file = open("templates/README_ZAKIPY.md","r")
	readme_string = markdown.markdown(
		readme_file.read(),extensions=["fenced_code","codehilite"]
	)
	readme_template = md_css_string + readme_string
	return readme_template

app.run(host='0.0.0.0', port=port)