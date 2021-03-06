import React from "react";
import ReactDOM from "react-dom";
import InputRow from "./InputRow.jsx";
import CompleteRow from "./CompleteRow.jsx";
import SuggestionContainer from "./SuggestionContainer.jsx";
import SaveSonnetContainer from "./SaveSonnetContainer.jsx";

const uuidv1 = require('uuid/v1');

export default class InputContainer extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            suggestions: [],
            hasRhymes: false,
            setLines: [],
            currentWord: "",
            currentLine: "",
            sonnetComplete: false
        }
    }

    reset(){
        $.post('/')
        this.setState({
            suggestions: [],
            hasRhymes: false,
            setLines: [],
            currentWord: "",
            currentLine: "",
            deleting: false,
            sonnetComplete: false
        }, () => { $(".inputForm").focus();})
    }

    isValidLetter(char) {
        return char.length == 1 && char.match(/[a-z.,?:;-_`~#$!\"\'\[\]\{\}/]/i);
    }

    isNum(char) {
        return char.length == 1 && char.match(/[0-9]/);
    }

    handleInput(e){
        if(e.key == "Enter"){

            // Do not allow empty sonnet lines
            if(this.state.currentLine.length == 0){
                return;
            }

            var numLines = this.state.setLines.length;

            // Completed sonnet
            if(numLines == 16){
                console.log("Completed Sonnet")
                this.setState({
                    sonnetComplete: true
                })
            }

            if(numLines == 3 || numLines == 8 || numLines == 13){
                console.log("New Quatrain")
                var setLines = this.state.setLines.concat([<CompleteRow key={uuidv1()} text={this.state.currentLine}/>])
                setLines = setLines.concat([<br key={uuidv1()} />])
                this.setState({
                    setLines: setLines,
                    currentWord: "",
                    currentLine: ""
                });
            } else {
                this.setState({
                    setLines: this.state.setLines.concat([<CompleteRow key={uuidv1()} text={this.state.currentLine}/>]),
                    currentWord: "",
                    currentLine: ""
                });
            }
            this.getSuggestions("\n");
        } else if (e.key == "Backspace") {
            var currLine = this.state.currentLine;
            if(currLine.length == 0){
                return
            }
            if(currLine.slice(-1) != " "){
                this.setState({
                    currentWord: this.state.currentWord.slice(0, -1),
                    currentLine: currLine.slice(0, -1),
                    deleting: false
                });
            } else {
                if(this.state.deleting){
                    this.handleDeleteWord()
                    this.setState({
                        currentWord: "",
                        currentLine: currLine.slice(0, currLine.lastIndexOf(" ", currLine.lastIndexOf(" ") - 1) + 1),
                        deleting: false
                    });
                } else {
                    this.setState({
                        deleting: true
                    }, () => {
                        var inputForm = $(".inputForm")[0];
                        var deleteFrom = currLine.lastIndexOf(" ", currLine.lastIndexOf(" ") - 1);
                        deleteFrom = deleteFrom > -1 ? deleteFrom : 0;
                        setTimeout(() => {
                            inputForm.setSelectionRange(deleteFrom, currLine.length - 1);
                            inputForm.focus();
                        }, 0);
                    })
                }
            }
        } else if (e.key == " ") {
            this.getSuggestions(this.state.currentWord);
            this.setState({
                currentLine: this.state.currentLine + e.key,
                currentWord: ""
            });
        } else if (this.isNum(e.key)) {
            var filteredSuggestions = this.state.suggestions.filter(
                suggestion => suggestion.indexOf(this.state.currentWord) == 0
            )
            if (parseInt(e.key) > 0 && parseInt(e.key) <= filteredSuggestions.length) {
                this.chooseSuggestion({suggestion: filteredSuggestions[parseInt(e.key) - 1]})
            } else if (parseInt(e.key) == 0 && filteredSuggestions.length > 9){
                this.chooseSuggestion({suggestion: filteredSuggestions[9]})
            }
        } else if (this.isValidLetter(e.key)) {
            this.setState({
                currentLine: this.state.currentLine + e.key,
                currentWord: this.state.currentWord + e.key
            });
        } 
        // console.log('Current word: ' + this.state.currentWord);
        // console.log('Current line: ' + this.state.currentLine)
    }

    handleDeleteWord(){
         $.post('/api/deleteword', res => {
            this.setState({
                suggestions: res['suggestions'],
                hasRhymes: res['hasRhymes']
            })
        })
    }

    getSuggestions(word){
        $.post('/api/getsuggestions', {word: word}, res => {
            this.setState({
                suggestions: res['suggestions'],
                hasRhymes: res['hasRhymes']
            })
        })
    }

    chooseSuggestion(suggestion){
        if(suggestion["suggestion"] == "eos" || suggestion["suggestion"] == "</quatrain>"){
            this.handleInput({key: "Enter"});
        } else {
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
    }

    render(){
        return(
                <div className="inputContainer">
                    {this.state.setLines}
                    {!this.state.sonnetComplete &&
                         <InputRow handleInput={this.handleInput.bind(this)} currentLine={this.state.currentLine}/>   
                    }
                    {!this.state.sonnetComplete &&
                         <SuggestionContainer
                         currentWord={this.state.currentWord}
                         suggestions={this.state.suggestions}
                         hasRhymes={this.state.hasRhymes}
                         chooseSuggestion={this.chooseSuggestion.bind(this)}
                         /> 
                    }
                    {this.state.sonnetComplete &&
                        <SaveSonnetContainer reset={this.reset.bind(this)}/>
                    }
                </div>
        )
    }
}