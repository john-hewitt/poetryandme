import React from "react";
import ReactDOM from "react-dom";
import { Chip, Avatar } from "material-ui"
import {
  blue300,
  blue500,
  indigo900,
  orange200,
  deepOrange300,
} from 'material-ui/styles/colors';
const uuidv1 = require('uuid/v1');

export default class SuggestionContainer extends React.Component {

	constructor(props) {
		super(props);
		// this.state = {
		// 	suggestions: this.props.suggestions
		// }
		this.styles = {
			chip:{
				margin: 4
			}
		}
	}

	render(){
		var suggestions = this.props.suggestions;
		return(
			<div className="suggestionContainer">
				{suggestions.map((suggestion, index) => {
                  return (
                    <Chip key={uuidv1()} style={this.styles.chip} backgroundColor={blue300} labelColor="white">
                    	<Avatar backgroundColor={blue500}>
                    		{index + 1}
                    	</Avatar>
                    	{suggestion}
                    </Chip>
                  )
                })}
			</div>
		)
	}

}