import React from "react";
import ReactDOM from "react-dom";

export default class CompleteRow extends React.Component {
    render(){
        return(
            <div className="completeRow">
                {this.props.text}
            </div>
        )
    }
}