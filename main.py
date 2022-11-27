from flask import Flask, render_template, url_for, request, abort, send_file
from hurry.filesize import size, alternative
import os
from datetime import datetime
port = os.environ.get('PORT', 8080)

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

@app.route("/files/",defaults={"reqpath": ""})
@app.route("/files/<path:reqpath>")
def files(reqpath):
	BASE_DIR = os.path.curdir
	abs_path = os.path.join(BASE_DIR, reqpath)
	if not os.path.exists(abs_path):
		return abort(404)
	if os.path.isfile(abs_path):
		return send_file(abs_path)
	files = os.listdir(abs_path)
	return render_template("files.html",files=files,getmtime=os.path.getmtime,getctime=os.path.getctime,size=size,alternative=alternative,getsize=os.path.getsize,path=os.path.curdir,fromtimestamp=datetime.fromtimestamp)

app.run(host='0.0.0.0', port=port)