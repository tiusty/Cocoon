// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveySmall.css'
import surveyIcon from './Questionnaire_dragon-512.png';

export default class SurveySmall extends Component {
    state = {
        name: "",
        url: "",
    };
    render() {
        return (
            <>
                <div className="survey-div">
                    <div className="survey-box">
                        <img className="survey-icon" src={surveyIcon} alt="Survey icon"/>

                    </div>
                </div>
            </>
        );
    }
}