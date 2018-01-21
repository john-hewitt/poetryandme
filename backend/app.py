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
line_values = {1: []}
line_inx = 1
curr_quatrain = 1

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

nlp = spacy.load('en')

app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def main():
	global current_sonnet
	global line_inx
	global line_endings
	global line_values
	global last_word
	global curr_quatrain
	line_endings = {}
	line_values = {1: []}
	line_inx = 1
	curr_quatrain = 1
	current_sonnet = ""
	last_word = ""
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
	suggestions, has_rhymes = getSuggestions(word)
	return jsonify({'suggestions': suggestions, 'hasRhymes': has_rhymes})

@app.route('/api/deleteword', methods=['POST'])
def delete_word():
	global current_sonnet
	global last_word
	sp.delete_word()
	lastSpaceIndex = current_sonnet.rfind(" ")
	current_sonnet = current_sonnet[:lastSpaceIndex]
	last_word = current_sonnet[current_sonnet.rfind(" ") + 1:]
	suggestions, has_rhymes = getSuggestions(last_word)
	return jsonify({'suggestions': suggestions, 'hasRhymes': has_rhymes})

def suggestion_contains_newline(suggestions):
	return "eos" in suggestions or "<quatrain/>" in suggestions

def num_syllables(line_values, line_inx):
	return sum([count_syllables(x) for x in line_values[line_inx]])

# this will be the backend call
def getSuggestions(word):
	global current_sonnet
	global line_inx
	global line_endings
	global line_values
	global last_word
	global curr_quatrain
	if word == "\n":
		sp.new_quatrain()
		current_sonnet += " eos"
		line_endings[line_inx] = last_word
		line_inx += 1
		line_values[line_inx] = []
		if line_inx == 5:
			curr_quatrain += 1
			line_endings = {}
			line_values = {1: []}
			line_inx = 1
	else:
		current_sonnet += " " + word;

	tokens = nlp(current_sonnet)
	last_token = tokens[len(tokens) - 1]

	token = last_token.text
	line_values[line_inx].append(token);
	last_word = token
	pos_tag = last_token.pos_
	suffix = token[-2:]
	num_syllables = count_syllables(token)
	suggestions = sp.add_word((token.lower(), pos_tag, suffix, num_syllables));

	total_syllables_line = sum([count_syllables(x) for x in line_values[line_inx]])

	if suggestion_contains_newline(suggestions) or total_syllables_line > 6:
		if line_inx - 2 in line_endings:
			return ["eos"] + suggestions[:4] + p.rhymes(line_endings[line_inx - 2])[:5], True
		elif line_inx - 1 in line_endings and curr_quatrain == 4:
			return ["eos"] + suggestions[:4] + p.rhymes(line_endings[line_inx - 1])[:5], True
		return ["eos"] + suggestions[:9], False
	return suggestions, False

