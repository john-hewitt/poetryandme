import React from "react";
import ReactDOM from "react-dom";
import styles from "./app.css";

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import InputContainer from "./components/InputContainer.jsx";

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
  <MaterialWrapper/>,
  document.getElementById('root')
);

