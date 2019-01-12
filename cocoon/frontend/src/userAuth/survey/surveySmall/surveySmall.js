// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveySmall.css'
import surveyIcon from '../survey_icon.png';
import survey_endpoints from '../../../endpoints/survey_endpoints'

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class SurveySmall extends Component {
    /**
     * Props:
     *  this.props.default_survey: (boolean) True -> Loads a default survey that loads the survey
     *                                       False/Blank -> Loads a survey based on the props passed in
     *  this.props.id: (int) -> The id for the survey
     *  this.props.name: (string) -> The name of the survey
     *  this.props.url: (string) -> The url to load the survey
     *  this.props.favorites_length: (int) -> The number of favorite homes for that survey
     *  this.props.visit_list_length: (int) -> The number of visit_list homes
     *  this.props.onClickSurvey: (function(int)) -> Handles when the small tile box is clicked
     */

    generateFavoriteHomes() {
        /**
         * Function checks if any of the homes in the favorites list is in the visit list
         *  If so then the home should not show up in the favorites list
         */
        let favorite_list = [];
        for (let i =0; i < this.props.favorites.length; i++) {
            // Checks to see if the favorite home is in the visit list and if it doesn't, then we want to render
            //  the homes with the favorites list
            if (this.props.visit_list.filter(h => h.id === this.props.favorites[i].id).length === 0) {
                favorite_list.push(this.props.favorites[i])
            }
        }
        return favorite_list
    }

    render() {
        /**
         * If the default survey prop is true then it is the extra survey that loads the survey
         *  Otherwise the small tile should contain information passed down via props
         */
        return (
            <>
                <div>
                    <div className="survey-small-box">
                        <div className="row">
                            <div className="col-sm-6">
                                <img className="survey-small-icon" src={surveyIcon} alt="Survey icon"/>
                            </div>
                        </div>
                        <div className="survey-small-data">
                            <p className="survey-small-title">Roomate Group:</p>
                            <p className="survey-small-title">{this.props.name}</p>
                            <p className="survey-small-favorites">Number of favorites: {this.generateFavoriteHomes().length}</p>
                            <p className="survey-small-visit-list">Number of visit
                                list: {this.props.visit_list.length}</p>
                            <button className="btn btn-primary" onClick={() => this.props.onClickSurvey(this.props.id)}>Expand</button>
                        </div>
                    </div>
                </div>
            </>
        );
    }

}

