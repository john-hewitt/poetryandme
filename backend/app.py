from flask import Flask, request, render_template, jsonify
from predictor import SonnetPredictor
import spacy
import sys

sys.path.append("../scripts")
from syllables import count_syllables

model_path = "../model.pt"
vocab_path = "../vocabs.json"
sp = SonnetPredictor(model_path, vocab_path)

current_sonnet = ""

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

nlp = spacy.load('en')

app.config['DEBUG'] = True

@app.route('/')
def main():
	global current_sonnet
	current_sonnet = ""
	sp = SonnetPredictor(model_path, vocab_path)
	return render_template('main.html')

@app.route('/api/newquatrain', methods=['POST'])
def new_quatrain():
	global current_sonnet
	sp.new_quatrain()
	current_sonnet = ""

@app.route('/api/getsuggestions', methods=['POST'])
def get_suggestions():
	word = request.form['word']
	suggestions = getSuggestions(word)
	return jsonify({'suggestions': suggestions})

# this will be the backend call
def getSuggestions(word):
	global current_sonnet
	if word == "\n":
		current_sonnet = current_sonnet + " EOS"
	else:
		current_sonnet = current_sonnet + " " + word;

	tokens = nlp(current_sonnet)
	last_token = tokens[len(tokens) - 1]

	token = last_token.text
	pos_tag = last_token.pos_
	suffix = token[-2:]
	num_syllables = count_syllables(token)
	return sp.add_word((token.lower(), pos_tag, suffix, num_syllables));