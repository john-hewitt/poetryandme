import React from "react";
import ReactDOM from "react-dom";
import { RaisedButton } from "material-ui"
import {
  green300,
  white,
  blue300
} from 'material-ui/styles/colors';

export default class SaveSonnetContainer extends React.Component{

	constructor(props) {
		super(props);
		this.styles = {
			button:{
				margin: 4
			}
		}
	}

	render(){
		return(
			<div className="saveSonnetContainer">
				<h1>Congrats you wrote a sonnet</h1>
				<RaisedButton
				 label="New Sonnet"
				 backgroundColor={blue300}
				 labelColor={white}
				 style={this.styles.button}
				 onClick={this.props.reset}>
				</RaisedButton>
			</div>
		)
	}
}