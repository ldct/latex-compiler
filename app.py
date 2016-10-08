#!/usr/bin/env python3

import subprocess

import flask
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route("/")
def index():
	return send_file('index.html')

@app.route("/compile", methods=['POST'])
def compile():
	latexSource = request.get_data()
	with open('./tmp.tex', 'wb') as f:
		f.write(latexSource)
	returnCode = subprocess.call(
		['pdflatex', '-halt-on-error', './tmp.tex'],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL
	)
	print(returnCode, type(returnCode))
	if returnCode == 0:
		return flask.jsonify(
			return_code=0
		)
	else:
		with open('./tmp.log') as logfile:
			l = logfile.read()
		return flask.jsonify(
			return_code=returnCode,
			log=l
		)

if __name__ == "__main__":
    app.run(debug=True)
