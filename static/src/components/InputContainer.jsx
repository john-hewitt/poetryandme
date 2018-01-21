import React from "react";
import ReactDOM from "react-dom";
import InputRow from "./InputRow.jsx";
import CompleteRow from "./CompleteRow.jsx";
import SuggestionContainer from "./SuggestionContainer.jsx";

const uuidv1 = require('uuid/v1');

export default class InputContainer extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            suggestions: [],
            setLines: [],
            currentWord: "",
            currentLine: ""
        }
    }

    isLetter(char) {
        return char.length == 1 && char.match(/[a-z]/i);
    }

    isNum(char) {
        return char.length == 1 && char.match(/[0-9]/);
    }

    handleInput(e){
        if(e.key == "Enter"){
            this.setState({
                setLines: this.state.setLines.concat([<CompleteRow key={uuidv1()} text={this.state.currentLine}/>]),
                currentWord: "",
                currentLine: ""
            });
        } else if (e.key == "Backspace") {
            this.setState({
                currentWord: this.state.currentWord.slice(0, -1),
                currentLine: this.state.currentLine.slice(0, -1)
            })
        } else if (e.key == " ") {
            this.getSuggestions(this.state.currentWord);
            this.setState({
                currentLine: this.state.currentLine + e.key,
                currentWord: ""
            });
        } else if (this.isNum(e.key)) {
            if(parseInt(e.key) > 0 && parseInt(e.key) <= this.state.suggestions.length)
            this.chooseSuggestion({suggestion: this.state.suggestions[parseInt(e.key) - 1]})
        } else if (this.isLetter(e.key)) {
            this.setState({
                currentLine: this.state.currentLine + e.key,
                currentWord: this.state.currentWord + e.key
            });
        } 
        console.log('Current word: ' + this.state.currentWord);
        console.log('Current line: ' + this.state.currentLine)
    }

    getSuggestions(word){
        console.log(word);
        $.post('/api/getsuggestions', {word: word}, res => {
            this.setState({
                suggestions: res['suggestions']
            })
        })
    }

    chooseSuggestion(suggestion){
        this.getSuggestions(suggestion["suggestion"]);
        var currentLine = this.state.currentLine;
        var currWordLength = this.state.currentWord.length;
        if(currWordLength != 0){
            currentLine = currentLine.slice(0, -currWordLength);
        }
        currentLine += suggestion["suggestion"] + ' '
        this.setState({
            currentWord: "",
            currentLine: currentLine
        })
        $(".inputForm").focus();
    }

    render(){
        return(
                <div className="inputContainer">
                    {this.state.setLines}
                    <InputRow handleInput={this.handleInput.bind(this)} currentLine={this.state.currentLine}/>
                    <SuggestionContainer
                     currentWord={this.state.currentWord}
                     suggestions={this.state.suggestions}
                     chooseSuggestion={this.chooseSuggestion.bind(this)}
                     />
                </div>
        )
    }
}