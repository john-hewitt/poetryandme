function handleInput(){
	console.log("here");
}

class InputRow extends React.Component {
	render(){
		return(
			<div className="inputRow">
				<input className="inputForm" onkeypress="handleInput"/>
			</div>
		)
	}
}

class InputContainer extends React.Component {
	render(){
		return(
			<div className="inputContainer">
				<InputRow/>
			</div>
		)
	}
}

class App extends React.Component {
	render(){
		return(
			<div className="app">
				<h1>Poetry and Me</h1>
				<InputContainer/>
			</div>
		)
	}
}

ReactDOM.render(
  <App/>,
  document.getElementById('root')
);

