// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './survey.css'
import HomeTile from "../../common/homeTile/homeTile";
import survey_endpoints from '../../endpoints/survey_endpoints'
import CSRFToken from '../../common/csrftoken';

// Import Pop-up button components
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css'

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';


class Survey extends Component {
    // Stores all the data associated with the survey
    state = {
        id: this.props.survey_id,
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
        let endpoint = this.props.endpoint + this.state.id;
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

    handleVisitClick = (home) => {
        /**
         *  Function handles when the user wants to add or remove a home from the visit list
         *
         *  The home that is being toggled is passed to the backend and then the updated state is
         *      returned and the new visit list is passed to the state
         * @type {string} The home that is being toggled
         */

        // The survey id is passed to the put request to update the state of that particular survey
        let endpoint = this.props.endpoint + this.state.id + "/";
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

    handleFavoriteClick = (home) => {
        /**
         * This function handles when the user clicks the heart to favorite or unfavorite a home
         *
         * Note: This function updates the curr_favorites so that the loaded favorites don't disappear
         *  and therefore the user has a chance to refavorite the home if they want
         * @type {string} The home that is being toggled
         */

        // The survey id is passed to the put request to update the state of that particular survey
        let endpoint = this.props.endpoint + this.state.id + "/";
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

    renderFavorites() {
        /**
         * Renders the favorite homes
         */
        if (this.state.favorites.length === 0) return <h3>Please load your survey and add favorite homes</h3>;
        return (
            <div>
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

    renderVisitList() {
        /**
         * Renders the visit list homes
         */
        if (this.state.visit_list.length === 0) return <h3>Please add homes to your visit list!</h3>;
        return (
            <div>
                {this.state.visit_list.map(home =>
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
                )}
            </div>
        );
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
                    onClick: () => this.props.onDelete(this.state.id)
                },
                {
                    label: 'No',
                }
            ]
        })
    };

    generateLoadUrl = () => {
        /**
         * Generates the URl so that the user can load a survey and it directs them to the survey results page for that
         *  survey
         */
        return survey_endpoints['rentSurveyResult'] + this.state.url + "/";
    };

    render(){
        return (
            <div className="Dotted_box">
                <div className="row">
                    <div className="col-md-10">
                        <h1>{this.state.name}</h1>
                    </div>
                    <div className="col-md-2">
                        <a href={this.generateLoadUrl()} className="btn btn-primary">Load</a>
                        <button onClick={this.handleDelete} className="btn btn-danger btn-sm m-2">Delete</button>
                        <form method="post">
                            <CSRFToken/>
                            <button name="submit-button" className="btn btn-success btn-sm m-2" value={this.state.id} type="submit">Schedule Group!</button>
                        </form>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-5">
                        <h2><u>Favorites:</u></h2>
                        {this.renderFavorites()}
                    </div>
                    <div className="col-md-5">
                        <h2><u>Visit List:</u></h2>
                        {this.renderVisitList()}
                    </div>
                </div>
            </div>
        );
    }
}
export default Survey
