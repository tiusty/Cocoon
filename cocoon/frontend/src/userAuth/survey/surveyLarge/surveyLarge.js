// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveyLarge.css'
import survey_endpoints from "../../../endpoints/survey_endpoints";
import scheduler_endpoints from"../../../endpoints/scheduler_endpoints"

export default class SurveyLarge extends Component {

    state = {
        name: "",
        url: "",
        desired_price: 0,
        num_bedrooms: 0,

        duration: null,
        refresh_duration: true,

        // Favorites contains a lit of the favorites when the data was pulled from the backend
        favorites:  [],
        // Stores the current list of favorites the user has, i.e if he unfavorited a home then
        //  the home will no longer be in this list. This is used so the user can favorite and unfavorite
        //  and the home won't disappear until the page is refreshed
        curr_favorites: [],

        visit_list:  [],
    };

    componentDidMount() {
        /**
         * Loads the survey data
         * @type {string}
         */

            // The survey id is appended to the get request to get a specific survey
        let endpoint = survey_endpoints['rentSurvey'] + this.props.id;
        axios.get(endpoint)
            .catch(error => console.log('BAD', error))
            .then(response =>
                {
                    this.setState({
                        name: response.data.name,
                        favorites: response.data.favorites,
                        curr_favorites: response.data.favorites,
                        visit_list: response.data.visit_list,
                        url: response.data.url,
                        desired_price: response.data.desired_price,
                        num_bedrooms: response.data.num_bedrooms,
                    })
                }
            )

        // Retrieves the current estimated time for the tour
        endpoint = scheduler_endpoints['itineraryDuration'] + this.props.id;
        axios.get(endpoint)
            .catch(error => console.log('BAD', error))
            .then(response => {
                    this.setState({
                        duration: response.data.duration,
                        refresh_duration: false,
                    })
                },
            )
    }

    render() {
        return(
            <div className="survey-large-div">
                <div className="survey-large-close-div">
                    <span onClick={() => this.props.onLargeSurveyClose()} className="survey-large-close-icon glyphicon glyphicon-remove"/>
                </div>
                <div className="survey-large-div-data">
                    <p className="survey-large-title">{this.state.name}</p>
                    <div className="row survey-large-survey-div">
                        <div className="col-md-5 survey-large-snapshot-outer">
                            <div className="survey-large-snapshot">
                                <h2 className="survey-large-title">Survey Snapshot</h2>
                                <p className="survey-large-text">Desired price: ${this.state.desired_price}</p>
                                <p className="survey-large-text">Number of bedrooms: {this.state.num_bedrooms}</p>
                            </div>
                        </div>
                        <div className="col-md-7 survey-large-homes-outer">
                            <div className="survey-large-homes">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
