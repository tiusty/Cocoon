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
                <div>
                    <div className="survey-small-box">
                        <img className="survey-small-icon" src={surveyIcon} alt="Survey icon"/>
                        <button className="btn btn-primary survey-small-load-button">Load</button>
                        <p className="survey-small-title">Tyler, Alex, and Tomas</p>
                        <p className="survey-small-favorites">Number of favorites: 5</p>
                        <p className="survey-small-visit-list">Number of visit list: 3</p>
                        <p className="survey-small-help-text">Click box to open</p>
                    </div>
                </div>
            </>
        );
    }
}