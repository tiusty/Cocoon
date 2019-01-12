// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveyLarge.css'
import HomeTiles from "../../../common/homeTile/homeTiles";
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

    generateLoadUrl = () => {
        /**
         * Generates the URl so that the user can load a survey and it directs them to the survey results page for that
         *  survey
         */
        return survey_endpoints['rentSurveyResult'] + this.state.url + "/";
    };

    renderFavoriteHomes() {
        if (this.state.favorites.length <=0) {
            return (
                <>
                    <h2 className="survey-large-title">Please load the survey to favorite homes</h2>
                    <a  href={this.generateLoadUrl()} onClick={() => this.props.onLoadingClicked()}
                        className="btn btn-primary survey-small-load-button">Load survey</a>
                </>
            );
        } else {
            return (
                <>
                    <h2 className="survey-large-title">Below are your favorite homes</h2>
                    <div className="survey-large-home">
                        <HomeTiles
                            homes={this.state.favorites}
                            visit_list={this.props.visit_list}
                            curr_favorites={this.state.curr_favorites}
                            onVisitClick={this.props.onHandleVisitListClicked}
                            onFavoriteClick={this.handleFavoriteClick}
                        />
                    </div>
                    <h2 className="survey-large-title">Want to favorite more homes?</h2>
                    <a  href={this.generateLoadUrl()} onClick={() => this.props.onLoadingClicked()}
                        className="btn btn-primary survey-small-load-button">Load survey</a>
                </>
            );
        }
    }

    handleFavoriteClick = (home, e) => {
        /**
         * This function handles when the user clicks the heart to favorite or unfavorite a home
         *
         * Note: This function updates the curr_favorites so that the loaded favorites don't disappear
         *  and therefore the user has a chance to refavorite the home if they want
         * @type {string} The home that is being toggled
         */

        // Prevents the onclick on the tile from triggering
        e.stopPropagation();

        // The survey id is passed to the put request to update the state of that particular survey
        let endpoint = survey_endpoints['rentSurvey'] + this.props.id + "/";
        axios.put(endpoint,
            {
                home_id: home.id,
                type: 'favorite_toggle',

            })
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    curr_favorites: response.data.favorites
                })
            );
    };

    render() {
        return (
            <div className="survey-large-div">
                <div className="survey-large-close-div">
                    <span onClick={() => this.props.onLargeSurveyClose()}
                          className="survey-large-close-icon glyphicon glyphicon-remove"/>
                </div>
                <div className="survey-large-div-data">
                    <p className="survey-large-title">{this.state.name}</p>
                    <div className="row survey-large-survey-div">
                        <div className="col-md-5 survey-large-snapshot-outer">
                            <div className="survey-large-snapshot">
                                <div className="survey-large-snapshot-section">
                                    <h2 className="survey-large-title">Survey Snapshot</h2>
                                    <p className="survey-large-text">Desired price: ${this.state.desired_price}</p>
                                    <p className="survey-large-text">Number of bedrooms: {this.state.num_bedrooms}</p>
                                </div>
                            <div className="survey-large-snapshot-section">
                                <p className="survey-large-text">Don't want this survey anymore?</p>
                                <button className="btn btn-danger">Delete Survey</button>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-7 survey-large-homes-outer">
                        <div className="survey-large-homes">
                            <div className="survey-large-homes-section">
                                {this.renderFavoriteHomes()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </div>
        );
    }
}
