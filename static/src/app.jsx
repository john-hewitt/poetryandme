import React from "react";
import ReactDOM from "react-dom";
import styles from "./app.css";

import InputContainer from "./components/InputContainer.jsx";


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

