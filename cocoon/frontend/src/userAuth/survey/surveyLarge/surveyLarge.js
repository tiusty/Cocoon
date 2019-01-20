// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveyLarge.css'
import HomeTiles from "../../../common/homeTile/homeTiles";
import survey_endpoints from "../../../endpoints/survey_endpoints";
import scheduler_endpoints from"../../../endpoints/scheduler_endpoints"

// Import Pop-up button components
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css'

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
                        url: response.data.url,
                        desired_price: response.data.desired_price,
                        num_bedrooms: response.data.num_bedrooms,
                    })
                }
            );

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

    generateLoadUrl = () => {
        /**
         * Generates the URl so that the user can load a survey and it directs them to the survey results page for that
         *  survey
         */
        return survey_endpoints['rentSurveyResult'] + this.state.url + "/";
    };

    renderFavoriteHomes() {
        if (this.generateFavoriteHomes().length <=0) {
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
                    <h2 className="survey-large-title">Want to favorite more homes?</h2>
                    <a  href={this.generateLoadUrl()} onClick={() => this.props.onLoadingClicked()}
                        className="btn btn-primary survey-small-load-button">Load survey</a>
                    <h2 className="survey-large-title">Below are your favorite homes</h2>
                    <div className="survey-large-home">
                        <HomeTiles
                            homes={this.generateFavoriteHomes()}
                            visit_list={this.props.visit_list}
                            favorites={this.props.favorites}
                            onVisitClick={this.props.onHandleVisitListClicked}
                            onFavoriteClick={this.handleFavoriteClick}
                            canVisit={true}
                            canFavorite={true}
                        />
                    </div>
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

        confirmAlert({
            title: 'Are you sure you want to unfavorite this home?',
            message: "This home will not longer appear unless you find it again in the survey",
            buttons: [
                {
                    label: 'yes',
                    onClick: () => this.props.onHandleFavoriteListClicked(home)
                },
                {
                    label: 'No',
                }
            ]
        });

    };

    handleDelete = () => {
        /**
         Opens a confirmation page first before the survey is deleted.
         If the user clicks yes then the survey gets deleted, if
         no then nothing happens
         */
        confirmAlert({
            title: 'Confirmation',
            message: "Are you sure you want to delete " + this.state.name + "?",
            buttons: [
                {
                    label: 'yes',
                    onClick: () => this.props.onDelete(this.props.id)
                },
                {
                    label: 'No',
                }
            ]
        })
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
                                <TenantEdit/>
                            <div className="survey-large-snapshot-section">
                                <p className="survey-large-text">Don't want this survey anymore?</p>
                                <button className="btn btn-danger" onClick={this.handleDelete}>Delete Survey</button>
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

class TenantEdit extends Component {
    state = {
        number_of_tenants: 4,
        tenants: [],
    }

    render() {
        return (
            <div className="survey-large-snapshot-section">
                <h2 className="survey-large-title">Tenants</h2>
                <form>
                    <p className="survey-large-text">Your Info</p>
                    <div className="row">
                        <div className="col-sm-6">
                            <input className="tenant-input" disabled={true} type="text" name="your_info"
                                   placeholder="First Name" autoCapitalize={'words'} data-tenantkey={0}
                            />
                        </div>
                        <div className="col-sm-6">
                            <input className="tenant-input" disabled={true} type="text" name="your_info"
                                   placeholder="Last Name" autoCapitalize={'words'} data-tenantkey={0}
                            />
                        </div>
                    </div>
                    {this.state.number_of_tenants > 1 && Array.from(Array(this.state.number_of_tenants - 1)).map((t, i) => {
                        return (
                            <>
                                <p key={i} className="survey-large-text">Roommate #1</p>
                                <div className="row">
                                    <div className="col-sm-6">
                                        <input className="tenant-input" type="text"
                                               name={'roommate_name_' + (i + 1)} autoCapitalize={'words'}
                                               data-tenantkey={i + 1} placeholder="First Name"
                                               key={i}/>
                                    </div>
                                    <div className="col-sm-6">
                                        <input className="tenant-input" type="text"
                                               name={'roommate_name_' + (i + 1)} autoCapitalize={'words'}
                                               data-tenantkey={i + 1} placeholder="Last Name"
                                               key={i}/>
                                    </div>
                                </div>
                            </>
                        );
                    })}
                </form>
            </div>
        );

    }
}
