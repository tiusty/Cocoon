// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import Survey from "./survey";
import userAuth_endpoints from "../../endpoints/userAuth_endpoints"

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class Surveys extends Component {
    state = {
        // Stores the ids of all the surveys associated with the user
        surveys: [],

        // Stores the endpoint needed for this Component
        endpoint: userAuth_endpoints['userSurveys'],
    };

    parseData(data) {
        /**
         * Parses data returned from the endpoint and returns it in a nicer format for react
         *
         * Expects to be passed data a list of surveys from the backend and then returns a list
         *  of the survey ids.
         * @type {Array}: A list of surveys
         */
        let survey_ids = [];

        // For each survey just push the id for that survey to the list
        data.map(c =>
            survey_ids.push( { id: c.id} )
        );

        // Return the list of ids
        return survey_ids
    }

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        axios.get(this.state.endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState( {surveys: this.parseData(response.data)})
            })
    }

    handleDelete = (survey_id) => {
        /**
         * When a survey wants to be deleted, it passes it to the backend and then
         *  the list of surveys is returned again and the data is repopulated with the new
         *  list of surveys.
         *
         *  Note: If no data race conditions happen, then the returned list of surveys should
         *      be just the same list of surveys with the deleted one gone.
         * @type {string} The survey id that is being deleted
         */

        // The survey id is appended to the endpoint since the put request expects the survey id as
        //  part of the url
        let endpoint = this.state.endpoint + survey_id + "/";

        // Passes the survey id and the put type to the backend
        axios.put(endpoint,
            {
                survey_id: survey_id,
                type: 'survey_delete',
            })
            .catch(error => console.log('Bad', error))
            .then(response => {
               this.setState( {surveys: this.parseData(response.data)})
            });
    };

    render() {
        /**
         * Renders all the surveys
         */
        return (
            <>
                { this.state.surveys.map(survey =>
                    <Survey
                        key={survey.id}
                        onDelete={this.handleDelete}
                        survey_id={survey.id}
                        endpoint={this.state.endpoint}
                    />

                )}
            </>
        );
    }
}
export default Surveys

