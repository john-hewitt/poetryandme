import React from "react";
import ReactDOM from "react-dom";

class InputRow extends React.Component {
	render(){
		return (
			<div className="inputRow">
				<input value={this.props.currentLine} className="inputForm" onKeyPress={this.props.handleInput}/>
			</div>
		);
	}
}

class CompleteRow extends React.Component {
	render(){
		return(
			<div className="completeRow">
				{this.props.text}
			</div>
		)
	}
}

class InputContainer extends React.Component {

	constructor(props){
		super(props);
		this.state = {
			children: [],
			currentWord: "",
			currentLine: ""
		}
	}

	isLetter(char) {
		return char.match(/[a-z]/i);
	}

	handleInput(e){
		if(e.key == "Enter"){
			this.setState({
				children: this.state.children.concat([<CompleteRow text={this.state.currentLine}/>]),
				currentWord: "",
				currentLine: ""
			});
		} else if (e.key == " ") {
			this.props.getSuggestions(this.state.currentWord);
			this.setState({
				currentLine: this.state.currentLine + e.key,
				currentWord: ""
			});
		} else if (this.isLetter(e.key)) {
			this.setState({
				currentLine: this.state.currentLine + e.key,
				currentWord: this.state.currentWord + e.key
			});
		}
	}

	render(){
		return(
			<div className="inputContainer">
				{this.state.children}
				<InputRow handleInput={this.handleInput.bind(this)} currentLine={this.state.currentLine}/>
			</div>
		)
	}
}

class App extends React.Component {
	getSuggestions(word){
		console.log(word);
		$.post('/api/getsuggestions', {word: 'hello'}, function(suggestions){
			console.log(suggestions);
		})
	}

	render(){
		return(
			<div className="app">
				<h1>Poetry and Me</h1>
				<InputContainer getSuggestions={this.getSuggestions.bind(this)}/>
			</div>
		)
	}
}

ReactDOM.render(
  <App/>,
  document.getElementById('root')
);

