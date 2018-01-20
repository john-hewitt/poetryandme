from flask import Flask, request, render_template, jsonify
app = Flask(__name__)

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
	return ['suggestion1', 'suggestion2', 'suggestion3']