// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveyLarge.css'
import deleteIcon from './delete_icon.png'
import HomeTiles from "../../../common/homeTile/homeTiles";
import survey_endpoints from "../../../endpoints/survey_endpoints";
import signature_endpoints from "../../../endpoints/signatures_endpoints"
import scheduler_endpoints from"../../../endpoints/scheduler_endpoints"
import CSRFToken from '../../../common/csrftoken';

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// Import Pop-up button components
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css'


export default class SurveyLarge extends Component {
    /**
     * This component loads a large survey which has extra info for that one survey.
     *
     * Props:
     *  this.props.id: (int) -> The survey id
     *  this.pre_tour_signed: (boolean) -> True: The pre tour documents are signed
     *                                     False: The pre tour documents are not signed
     *  this.props.onDelete: (function(int)) (int-survey id)-> Handles when the delete button is pressed.
     *  this.props.onLargeSurveyClose: (function()): -> Handles when the close button is pressed
     */
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
                    console.log(response.data),
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

    componentDidUpdate(prevProps, prevState) {
        if (prevState.visit_list !== this.state.visit_list) {
            let endpoint = scheduler_endpoints['itineraryDuration'] + this.props.id;
            this.setState({
                refresh_duration: true,
            });
            axios.get(endpoint)
                .catch(error => {
                    console.log('BAD', error);
                    this.setState({
                        refresh_duration: false,
                    })
                })
                .then(response => {
                        this.setState({
                            duration: response.data.duration,
                            refresh_duration: false,
                        })
                    },
                )
        }
    }

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

    renderFavorites() {
        /**
         * Renders the favorite homes
         */
        if (this.state.favorites.length === 0) return <h3 className="survey-large-no-homes">Go favorite some homes!</h3>
        return (
            <div className="survey-large-home">
                <HomeTiles
                    homes={this.state.favorites}
                    visit_list={this.state.visit_list}
                    curr_favorites={this.state.curr_favorites}
                    onVisitClick={this.handleVisitClick}
                    onFavoriteClick={this.handleFavoriteClick}
                />
            </div>
        );
    };

    renderVisitList() {
        /**
         * Renders the visit list homes
         */
        if (this.state.visit_list.length === 0) return <h3 className="survey-large-no-homes">Please add homes to your visit list!</h3>;
        return (
            <div className="survey-large-home">
                <HomeTiles
                    homes={this.state.visit_list}
                    visit_list={this.state.visit_list}
                    curr_favorites={this.state.curr_favorites}
                    onVisitClick={this.handleVisitClick}
                    onFavoriteClick={this.handleFavoriteClick}
                />
            </div>
        );
    };

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

    handleVisitClick = (home, e) => {
        /**
         *  Function handles when the user wants to add or remove a home from the visit list
         *
         *  The home that is being toggled is passed to the backend and then the updated state is
         *      returned and the new visit list is passed to the state
         * @type {string} The home that is being toggled
         */

        // Prevents the onclick on the tile from triggering
        e.stopPropagation();

        // The survey id is passed to the put request to update the state of that particular survey
        let endpoint = survey_endpoints['rentSurvey'] + this.props.id + "/";
        axios.put(endpoint,
            {
                home_id: home.id,
                type: 'visit_toggle'

            })
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    visit_list: response.data.visit_list
                })
            );
    };


    scheduleButtonMessages() {
        /**
         * Generates the message for the tour summary page
         */
        if(!this.props.pre_tour_signed) {
            return 'Please sign pre tour docs'
        } else {
            return 'You are read to schedule!'
        }
    }

    scheduleButton() {
        /**
         * Generates the button for the tour summary based on the state of the user
         */
        // If the pre tour documents are not signed then generate a sign document button
        if(!this.props.pre_tour_signed) {
            return (
                    <a style={{width: '115px'}} className="btn btn-success btn-sm survey-large-tour-summary-button" role="button"
                       href={signature_endpoints['signaturePage']}
                       > Sign Documents </a>
            );
        // If the pre tour documents are signed then generate the tour summary button
        } else {
            return(
                <form method="post" style={{marginTop: '10px'}}>
                    <CSRFToken/>
                    <button name="submit-button" disabled={!this.props.pre_tour_signed}
                            className="btn btn-success btn-sm m-2 survey-large-tour-summary-button"
                            value={this.props.id} type="submit">Schedule!
                    </button>
                </form>
            );
        }

    }

    render() {
        return (
            <div className="survey-large-div">
                <div className="survey-large-header">
                    <span onClick={() => this.props.onLargeSurveyClose()} className="survey-large-icon glyphicon glyphicon-resize-small"/>
                    <p className="survey-large-title">{this.state.name}</p>
                    <img className="survey-large-delete-button" onClick={() => this.handleDelete()} src={deleteIcon} alt="Delete Button"/>
                </div>
                <div className="survey-large-info-div">
                    <div  className="survey-large-snapshot">
                        <p className="survey-large-snapshot-title">Survey Snapshot</p>
                        <p className="survey-large-snapshot-price">Desired price: ${this.state.desired_price}</p>
                        <p className="survey-large-snapshot-bedrooms">Number of bedrooms: {this.state.num_bedrooms}</p>
                    </div>
                    <div className="survey-large-tour-summary">
                        <p className="survey-large-tour-summary-title">Tour Summary</p>
                        <p className="survey-large-tour-summary-estimate-duration">Estimated duration: {this.state.refresh_duration ? 'Loading' : Math.round(this.state.duration/60) + ' mins'}</p>
                        <p className="survey-large-tour-summary-message">{this.scheduleButtonMessages()}</p>
                        {this.scheduleButton()}
                    </div>
                </div>
                <div className="survey-large-homes-div">
                    <div className="survey-large-favorites-div">
                        <p className='survey-large-favorites-title'>Favorite Home</p>
                        {this.renderFavorites()}
                    </div>
                    <div className="survey-large-visit-list-div">
                        <p className='survey-large-favorites-title'>Visit List</p>
                        {this.renderVisitList()}
                    </div>
                </div>
            </div>
        );
    }
}
