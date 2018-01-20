class InputRow extends React.Component {
	render(){
		return(
			<div className="inputRow">
				<input className="inputForm" onKeyPress={this.props.handleInput}/>
			</div>
		)
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
			children: []
		}
	}

	handleInput(e){
		if(e.key == "Enter"){
			console.log("new line");
			this.setState({
				children: this.state.children.concat([<CompleteRow text="child"/>])
			});
		} else if (e.key == " "){
			this.props.getSuggestions("word")
		}
	}

	render(){
		console.log(this.props)
		return(
			<div className="inputContainer">
				{this.state.children}
				<InputRow handleInput={this.handleInput.bind(this)}/>
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

