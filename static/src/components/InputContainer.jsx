import React from "react";
import ReactDOM from "react-dom";
import InputRow from "./InputRow.jsx";
import CompleteRow from "./CompleteRow.jsx";

import { Card, CardText, CardTitle } from 'react-md';

export default class InputContainer extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            children: [],
            currentWord: "",
            currentLine: ""
        }
    }

    isLetter(char) {
        return char.match(/[a-z]/i);
    }

    handleInput(e){
        if(e.key == "Enter"){
            this.setState({
                children: this.state.children.concat([<CompleteRow text={this.state.currentLine}/>]),
                currentWord: "",
                currentLine: ""
            });
        } else if (e.key == " ") {
            this.props.getSuggestions(this.state.currentWord);
            this.setState({
                currentLine: this.state.currentLine + e.key,
                currentWord: ""
            });
        } else if (this.isLetter(e.key)) {
            this.setState({
                currentLine: this.state.currentLine + e.key,
                currentWord: this.state.currentWord + e.key
            });
        }
    }

    render(){
        return(
            <Card className="md-block-centered" raise={true} >
            <CardTitle title="hello world"></CardTitle>
            <div className="inputContainer">
                <CardText>
                    {this.state.children}
                </CardText>
                <InputRow handleInput={this.handleInput.bind(this)} currentLine={this.state.currentLine}/>
            </div>
            </Card>
        )
    }
}