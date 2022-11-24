from flask import Flask, render_template, url_for, request
from flask_autoindex import AutoIndex
import os
port = os.environ.get('PORT', 8080)

app = Flask(__name__)
app.config['DEBUG'] = True
AutoIndex(app, browse_root=os.path.curdir)

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

app.run(host='0.0.0.0', port=port)