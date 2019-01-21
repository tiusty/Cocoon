// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'
import PropTypes from 'prop-types';

// Import Cocoon Components
import './surveyLarge.css'
import HomeTiles from "../../../common/homeTile/homeTiles";
import survey_endpoints from "../../../endpoints/survey_endpoints";
import scheduler_endpoints from"../../../endpoints/scheduler_endpoints"

// Import Pop-up button components
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css'

export default class SurveyLarge extends Component {
    /**
     * Handles when a survey is clicked and the large survey is displayed
     *
     * Props:
     *  this.props.id: (int) -> The survey id
     *  this.props.favorites: (list(RentDatabase Models)) -> The list of homes in the favorites list
     *  this.props.visit_list: (list(RentDatabase Models)) -> The list of homes in the visit_list
     *  this.props.onLoadingClicked: (func()) -> Handles when the load button is clicked for a survey
     *  this.props.onHandleFavoriteListClicked: (func(home)) {home: The home associated with the home tile} -> Handles
     *      when the favorite button is clicked on a home-tile
     *  this.props.onHandleVisitListClicked: (func(home, e)) {home: Home associated with the home tile,
     *                                                            e: the html pointer} -> Handles when the visit button
*           is clicked on a home-tile
     *  this.props.onLargeSurveyClose: (func()) -> Handles when the close button is clicked for a large survey
     *  this.props.onDelete: (func(id)) {id: survey id} -> Handles when the delete button is clicked for a survey
     */

    state = {
        // Variables associated with the tour
        name: "",
        url: "",
        desired_price: 0,
        num_bedrooms: 0,

        // Variables associated with the tour
        duration: null,
        refresh_duration: true,

        // Favorites contains a lit of the favorites when the data was pulled from the backend
        favorites:  [],

        // The tenants associated with the survey
        tenants: [],
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
                        // Sort the tenants so they always return in the same order
                        tenants: response.data.tenants.sort((a, b) => a.id > b.id),
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

    handleSubmitTenantInfo = (tenants) => {
        /**
         * Handles submitted the tenant information to the backend
         * @type {{}}
         */

        // Put all the variables in the correct format so the django formset can handle
        //  them properly
        let tenantInfo = {};
        for (let i=0; i<tenants.length; i++) {
            for(let key in tenants[i]) {
                tenantInfo['tenants-' + i + '-' + key] = tenants[i][key]
            }
        }

        // Add the management data for the tenants needed by Django
        tenantInfo['tenants-INITIAL_FORMS'] = tenants.length;
        tenantInfo['tenants-MAX_NUM_FORMS'] = 1000;
        tenantInfo['tenants-MIN_NUM_FORMS'] = 0;
        tenantInfo['tenants-TOTAL_FORMS'] = tenants.length;

        let endpoint = survey_endpoints['tenants'] + this.props.id + '/';
        axios.put(endpoint,
            {
                data: tenantInfo,
            })
            .catch(error => console.log('BAD', error))
            .then(response =>
                {
                    this.setState({
                        name: response.data.name,
                        url: response.data.url,
                        desired_price: response.data.desired_price,
                        num_bedrooms: response.data.num_bedrooms,
                        // Sort the tenants so they always return in the same order
                        tenants: response.data.tenants.sort((a, b) => a.id > b.id),
                    })
                }
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
                                <TenantEdit
                                    tenants={this.state.tenants}
                                    onUpdateTenantInfo={this.updateTenantInfo}
                                    onSubmitTenantInfo={this.handleSubmitTenantInfo}
                                />
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

SurveyLarge.propTypes = {
    id: PropTypes.number.isRequired,
    favorites: PropTypes.array.isRequired,
    visit_list: PropTypes.array.isRequired,
    onLoadingClicked: PropTypes.func.isRequired,
    onHandleFavoriteListClicked: PropTypes.func.isRequired,
    onHandleVisitListClicked: PropTypes.func.isRequired,
    onLargeSurveyClose: PropTypes.func.isRequired,
};

class TenantEdit extends Component {
    /**
     * Component handles displaying and updating the tenants names
     *
     * Props:
     *     this.props.tenants: (list(Tenants)) -> The list of tenants corresponding to the survey
     */
    state = {
        curr_tenants: [],
    };


    componentDidUpdate(prevProps) {
        /**
         * Handles if the parent tenants variable changes values.
         * If it does then update the curr_tenants value.
         *
         * This is most common when the user submits the new tenants names for saving
         *  and so this updates the new names saved in the backend
         */
        if (prevProps.tenants !== this.props.tenants) {
            // This does a deep copy because otherwise it is a memory reference and causes issues
            let curr_tenants = JSON.parse(JSON.stringify(this.props.tenants));
            this.setState({curr_tenants})
        }
    }


    updateTenantInfo = (e, type) => {
        /**
         * Handles when the user changes one of the tenants names
         *
         * e: -> The event pointer
         * type: (string) -> determines which part of the name is being edited.
         *              'first' for first name
         *              'last' for last name
         */

            // Retrieve which tenant and the new value for the tenant
        const { value } = e.target;
        const name = value;
        const index = e.target.dataset.tenantkey;
        let tenants = [...this.state.curr_tenants];

        // Determines which part of the name is being edited
        if (type === 'first') {
            tenants[index].first_name = name
        } else {
            tenants[index].last_name = name
        }

        // Save the value to the state
        this.setState({curr_tenants: tenants})
    };

    handleDisableSubmit() {
        /**
         * Determines if the tenants variables are the same. If anything was changed then
         *  allow the user to save the data
         *
         * This assumes the tenants are in the correct order.
         */
        for (let i=0; i<this.state.curr_tenants.length; i++) {
            if (this.state.curr_tenants[i].id !== this.props.tenants[i].id
            || this.state.curr_tenants[i].first_name !== this.props.tenants[i].first_name
            || this.state.curr_tenants[i].last_name !== this.props.tenants[i].last_name) {
                return false
            }
        }

        return true
    }

    render() {
        // let tenants = this.props.tenants;
        let tenants = this.state.curr_tenants;

        if (tenants.length > 0) {
            return (
                <div className="survey-large-snapshot-section">
                    <h2 className="survey-large-title">Tenants</h2>
                        {tenants.length > 0 && Array.from(Array(tenants.length)).map((t, i) => {
                            return (
                                <div key={i}>
                                    <p className="survey-large-text">Roommate #{i + 1}</p>
                                    <div className="row">
                                        <div className="col-sm-6">
                                            <input className="tenant-input" type="text"
                                                   name={'roommate_name_' + i} autoCapitalize={'words'}
                                                   data-tenantkey={i} placeholder="First Name"
                                                   onChange={(e) => this.updateTenantInfo(e, 'first')}
                                                   value={tenants[i].first_name}
                                            />
                                        </div>
                                        <div className="col-sm-6">
                                            <input className="tenant-input" type="text"
                                                   name={'roommate_name_' + i} autoCapitalize={'words'}
                                                   data-tenantkey={i} placeholder="Last Name"
                                                   onChange={(e) => this.updateTenantInfo(e, 'last')}
                                                   value={tenants[i].last_name}
                                            />
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                         <button className="btn btn-success" disabled={this.handleDisableSubmit()} onClick={() => this.props.onSubmitTenantInfo(this.state.curr_tenants)}>Save</button>
                </div>
            );

        } else {
            return <p>Loading</p>
        }
    }
}

TenantEdit.propTypes = {
    tenants: PropTypes.array,
};
