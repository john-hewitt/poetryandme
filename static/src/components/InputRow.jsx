import React from "react";
import ReactDOM from "react-dom";

export default class InputRow extends React.Component {
    render(){
        return (
            <div className="inputRow">
                <input value={this.props.currentLine} className="inputForm" onKeyDown={this.props.handleInput}/>
            </div>
        );
    }
}