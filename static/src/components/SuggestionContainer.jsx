import React from "react";
import ReactDOM from "react-dom";
import { Chip, Avatar } from "material-ui"
import {
  blue300,
  blue500,
  indigo900,
  orange200,
  deepOrange300,
  red300
} from 'material-ui/styles/colors';
const uuidv1 = require('uuid/v1');

export default class SuggestionContainer extends React.Component {

	constructor(props) {
		super(props);
		this.styles = {
			chip:{
				margin: 4
			}
		}
	}

	render(){
		var suggestions = this.props.suggestions.filter(suggestion => 
			suggestion.indexOf(this.props.currentWord) == 0
		);
		if(this.props.hasRhymes){
			var normalSuggestions = suggestions.slice(0, 5);
			var rhymeSuggestions = suggestions.slice(5, suggestions.length);
			return(
				<div className="suggestionContainer">
					{normalSuggestions.map((suggestion, index) => {
							return (
		                    <Chip 
		                    	key={uuidv1()}
		                    	style={this.styles.chip} 
		                    	backgroundColor={blue300} 
		                    	labelColor="white"
		                    	onClick={e => {this.props.chooseSuggestion({suggestion})}}
		                    >
		                    	<Avatar backgroundColor={blue500}>
		                    		{index == 9 ? 0 : index + 1}
		                    	</Avatar>
		                    	{suggestion == "eos" || suggestion == "</quatrain>" ? "New line" : suggestion}
		                    </Chip>
		                  )
	                })}
	                {rhymeSuggestions.map((suggestion, index) => {
							return (
		                    <Chip 
		                    	key={uuidv1()}
		                    	style={this.styles.chip} 
		                    	backgroundColor={red300} 
		                    	labelColor="white"
		                    	onClick={e => {this.props.chooseSuggestion({suggestion})}}
		                    >
		                    	<Avatar backgroundColor={blue500}>
		                    		{index + 5 == 9 ? 0 : index + 6}
		                    	</Avatar>
		                    	{suggestion == "eos" || suggestion == "</quatrain>" ? "New line" : suggestion}
		                    </Chip>
		                  )
	                })}
				</div>
			)
		} else {
			return(
				<div className="suggestionContainer">
					{suggestions.map((suggestion, index) => {
							return (
		                    <Chip 
		                    	key={uuidv1()}
		                    	style={this.styles.chip} 
		                    	backgroundColor={blue300} 
		                    	labelColor="white"
		                    	onClick={e => {this.props.chooseSuggestion({suggestion})}}
		                    >
		                    	<Avatar backgroundColor={blue500}>
		                    		{index == 9 ? 0 : index + 1}
		                    	</Avatar>
		                    	{suggestion == "eos" || suggestion == "</quatrain>" ? "New line" : suggestion}
		                    </Chip>
		                  )
	                })}
				</div>
			)
		}
	}

}