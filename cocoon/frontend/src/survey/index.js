import React from 'react';
import { Component } from 'react';
import ReactDOM from "react-dom";

import './survey.css';

class Survey extends Component {
    componentDidMount = () => {
        console.log('rendered!');
    }

    render(){
        return (
            <h1 className="survey-headline">Survey will go here!</h1>
        );
    }
}

ReactDOM.render(
    React.createElement(Survey, window.props),
    window.react_mount
);