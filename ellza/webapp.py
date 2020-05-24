# coding: utf-8
'''
Ellpedia is released under the AGPL-3.0 Licence.
See the LICENCE file.
(C) ThunderRa1n, <podsn0w@gmail.com>
'''
import json, html
from flask import Flask, render_template, request, jsonify
from reply_generator import generate_reply
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		query = html.escape(request.form['chat_text'])
		if query == '':
			reply = '再度入力してください。'
		else:
		    reply = generate_reply(query)
		return jsonify(results = reply)
	else:
		return render_template('index.html')

app.run(port=50003, debug=False)