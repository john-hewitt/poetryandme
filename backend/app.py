from flask import Flask, request, render_template, jsonify
import spacy
import sys

sys.path.append("../scripts")
from syllables import count_syllables

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

# nlp = spacy.load('en')

app.config['DEBUG'] = True

@app.route('/')
def main():
	return render_template('main.html')

@app.route('/api/getsuggestions', methods=['POST'])
def get_suggestions():
	word = request.form['word']
	suggestions = getSuggestions(word)
	return jsonify({'suggestions': suggestions})

# this will be the backend call
def getSuggestions(word):
	# tokens = nlp(word);
	# token = tokens[0].text;
	# pos_tag = tokens[0].pos_;
	# suffix = token[-2:];
	# num_syllables = count_syllables(token);

	return [word + '1', word + '2', word + '3']