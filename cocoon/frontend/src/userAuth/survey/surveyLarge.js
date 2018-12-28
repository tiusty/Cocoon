// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveyLarge.css'
import closingIcon from './closing.png'
import HomeTile from "../../common/homeTile/homeTile";
import survey_endpoints from "../../endpoints/survey_endpoints";
import signature_endpoints from "../../endpoints/signatures_endpoints"
import CSRFToken from '../../common/csrftoken';

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// Import Pop-up button components
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css'


export default class SurveyLarge extends Component {
    state = {
        name: "",
        url: "",
        price: 0,

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
                this.setState({
                    name: response.data.name,
                    favorites: response.data.favorites,
                    curr_favorites: response.data.favorites,
                    visit_list: response.data.visit_list,
                    url: response.data.url,
                }),
            )
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
                {this.state.favorites.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={this.inFavorites(home)}
                        visit={this.state.visit_list.filter(c => c.id === home.id).length >0}
                        onVisitClick={this.handleVisitClick}
                        onFavoriteClick={this.handleFavoriteClick}
                        show_heart={true}
                        show_score={false}
                        show_visit={true}
                    />
                )}
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
                {this.state.visit_list.map(home =>
                    <div key={home.id}>
                        <HomeTile
                            key={home.id}
                            home={home}
                            favorite={this.inFavorites(home)}
                            visit={this.inVisitList(home)}
                            onVisitClick={this.handleVisitClick}
                            onFavoriteClick={this.handleFavoriteClick}
                            show_score={false}
                            show_heart={true}
                            show_visit={true}
                        />
                    </div>
                )}
            </div>
        );
    };

    handleFavoriteClick = (home) => {
        /**
         * This function handles when the user clicks the heart to favorite or unfavorite a home
         *
         * Note: This function updates the curr_favorites so that the loaded favorites don't disappear
         *  and therefore the user has a chance to refavorite the home if they want
         * @type {string} The home that is being toggled
         */

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

    handleVisitClick = (home) => {
        /**
         *  Function handles when the user wants to add or remove a home from the visit list
         *
         *  The home that is being toggled is passed to the backend and then the updated state is
         *      returned and the new visit list is passed to the state
         * @type {string} The home that is being toggled
         */

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

    inFavorites(home) {
        /**
         * Tests whether a particular home is currently favorited
         */
        // Checks to see if the home exists within the favorites list
        return this.state.curr_favorites.filter(c => c.id === home.id).length > 0;
    }

    inVisitList(home) {
        /**
         * Tests if a particular home is currently in the visit list
         */
        // Checks to see if the home exists within the visit_list
        return this.state.visit_list.filter(c => c.id === home.id).length >0;
    }

    scheduleButtonMessages() {
        if(!this.props.pre_tour_signed) {
            return 'Please sign pre tour docs'
        } else {
            return 'You are read to schedule!'
        }
    }

    scheduleButton() {
        if(!this.props.pre_tour_signed) {
            return (
                    <a style={{width: '115px'}} className="btn btn-success btn-sm survey-large-tour-summary-button" role="button"
                       href={signature_endpoints['signaturePage']}
                       > Sign Documents </a>
            );
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
                    <img onClick={() => this.props.onLargeSurveyClose()} className="survey-large-icon" src={closingIcon} alt="Closing icon"/>
                    <p className="survey-large-title">{this.state.name}</p>
                    <button onClick={this.handleDelete} className="btn btn-danger btn-sm m-2 survey-large-delete-button">Delete</button>
                </div>
                <div className="survey-large-info-div">
                    <div  className="survey-large-snapshot">
                        <p className="survey-large-snapshot-title">Survey Snapshot</p>
                        <p className="survey-large-snapshot-price">Desired price: $2000</p>
                        <p className="survey-large-snapshot-bedrooms">Number of bedrooms: 2</p>
                    </div>
                    <div className="survey-large-tour-summary">
                        <p className="survey-large-tour-summary-title">Tour Summary</p>
                        <p className="survey-large-tour-summary-estimate-duration">Estimated duration: 1 hour 5 minutes</p>
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
