// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveySmall.css'
import surveyIcon from './Questionnaire_dragon-512.png';
import survey_endpoints from '../../endpoints/survey_endpoints'

export default class SurveySmall extends Component {
    state = {
        name: "",
        url: "",
        load_click: false,
    };

    generateLoadUrl = () => {
        /**
         * Generates the URl so that the user can load a survey and it directs them to the survey results page for that
         *  survey
         */
        return survey_endpoints['rentSurveyResult'] + this.state.url + "/";
    };

    handleOnClick() {
            console.log('click')
    }

    render() {
        return (
            <>
                <div>
                    <div className="survey-small-box" onClick={() => this.handleOnClick()}>
                        <img className="survey-small-icon" src={surveyIcon} alt="Survey icon"/>
                        {/*<button className="btn btn-primary survey-small-load-button">Load</button>*/}
                        <a  onClick={() => this.props.onLoadingClicked()} className="btn btn-primary survey-small-load-button">Load</a>
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