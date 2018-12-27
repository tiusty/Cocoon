// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveySmall.css'
import surveyIcon from './Questionnaire_dragon-512.png';
import survey_endpoints from '../../endpoints/survey_endpoints'

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class Survey extends Component {
    render() {
        return <SurveySmall
            onLoadingClicked={this.props.onLoadingClicked}
            default_survey={this.props.default_survey}
            url={this.props.url}
        />
    }
}

class SurveySmall extends Component {

    generateLoadUrl = () => {
        /**
         * Generates the URl so that the user can load a survey and it directs them to the survey results page for that
         *  survey
         */
        return survey_endpoints['rentSurveyResult'] + this.props.url + "/";
    };

    handleOnClick() {
        console.log('click')
    }

    render() {
        if(this.props.default_survey) {
             return (
                <>
                    <div>
                        <div className="survey-small-box" onClick={(e) => this.handleOnClick(e)}>
                            <img className="survey-small-icon" src={surveyIcon} alt="Survey icon"/>
                            <p className="survey-small-default-text">click here to take a survey</p>
                            <p className="survey-small-default-text-bottom">Your future home awaits</p>
                        </div>
                    </div>
                </>
            );
        } else {
            return (
                <>
                    <div>
                        <div className="survey-small-box" onClick={() => this.handleOnClick()}>
                            <img className="survey-small-icon" src={surveyIcon} alt="Survey icon"/>
                            <a  href={this.generateLoadUrl()} onClick={() => this.props.onLoadingClicked()}
                                className="btn btn-primary survey-small-load-button">Load</a>
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

}