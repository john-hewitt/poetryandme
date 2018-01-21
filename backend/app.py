from flask import Flask, request, render_template, jsonify
from predictor import SonnetPredictor
import spacy
import sys
import pronouncing as p

sys.path.append("../scripts")
from syllables import count_syllables

model_path = "../model.pt"
vocab_path = "../vocabs.json"
sp = SonnetPredictor(model_path, vocab_path)


current_sonnet = ""
last_word = ""

line_endings = {}
line_inx = 1

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

nlp = spacy.load('en')

app.config['DEBUG'] = True

@app.route('/')
def main():
	global current_sonnet
	current_sonnet = ""
	global sp
	sp = SonnetPredictor(model_path, vocab_path)
	sp.new_poem()
	return render_template('main.html')

@app.route('/api/newquatrain', methods=['POST'])
def new_quatrain():
	global current_sonnet
	global line_endings
	global line_inx
	sp.new_quatrain()
	current_sonnet = ""
	line_endings = {}
	line_inx = 1

@app.route('/api/getsuggestions', methods=['POST'])
def get_suggestions():
	word = request.form['word']
	suggestions = getSuggestions(word)
	return jsonify({'suggestions': suggestions})

def suggestion_contains_newline(suggestions):
	return "eos" in suggestions or "<quatrain/>" in suggestions

# this will be the backend call
def getSuggestions(word):
	global current_sonnet
	global last_word
	if word == "\n":
		sp.new_quatrain()
		current_sonnet += " eos"
		line_endings[line_inx] = last_word
		line_inx += 1
	else:
		current_sonnet += " " + word;

	tokens = nlp(current_sonnet)
	last_token = tokens[len(tokens) - 1]

	token = last_token.text
	last_word = token
	pos_tag = last_token.pos_
	suffix = token[-2:]
	num_syllables = count_syllables(token)
	suggestions = sp.add_word((token.lower(), pos_tag, suffix, num_syllables));
	if suggestion_contains_newline(suggestions) and line_inx - 2 in line_endings:
		return p.rhymes(line_endings[line_inx - 2])[:10]

