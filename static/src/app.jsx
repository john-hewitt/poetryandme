import React from "react";
import ReactDOM from "react-dom";
import styles from "./app.css";

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import InputContainer from "./components/InputContainer.jsx";
import SuggestionContainer from "./components/SuggestionContainer.jsx";

class MaterialWrapper extends React.Component{
	render(){
		return(
			<MuiThemeProvider>
				<App />
			</MuiThemeProvider>
		)
	}
}

class App extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			suggestions: []
		}
	}

	getSuggestions(word){
		console.log(word);
		$.post('/api/getsuggestions', {word: word}, res => {
			this.setState({
				suggestions: res['suggestions']
			})
		})
	}

	render(){
		return(
			<div className="app">
				<h1>Poetry and Me</h1>
				<InputContainer getSuggestions={this.getSuggestions.bind(this)}/>
				<SuggestionContainer suggestions={this.state.suggestions}/>
			</div>
		)
	}
}

ReactDOM.render(
  <MaterialWrapper/>,
  document.getElementById('root')
);

