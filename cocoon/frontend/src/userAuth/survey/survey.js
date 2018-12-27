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
    state = {
        name: "",
        url: "",
    };

    componentDidMount() {
        /**
         * Loads the survey data
         * @type {string}
         */

            // The survey id is appended to the get request to get a specific survey
            console.log(this.props.id)
        let endpoint = survey_endpoints['rentSurvey'] + this.props.id;
            console.log(endpoint)
        axios.get(endpoint)
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    name: response.data.name,
                    favorites: response.data.favorites,
                    curr_favorites: response.data.favorites,
                    visit_list: response.data.visit_list,
                    url: response.data.url,
                }),
            )
    }

    render() {
        return <SurveySmall
            url={this.state.url}
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