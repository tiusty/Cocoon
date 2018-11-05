import React from 'react';
import { Component } from 'react';

import './survey.css';

export default class Survey extends Component {
    componentDidMount = () => {
        console.log('rendered!');
    }

    render(){
        return (
            <h1 className="survey-headline">Survey will go here!</h1>
        );
    }
}