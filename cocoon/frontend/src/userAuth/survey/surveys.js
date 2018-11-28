// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import Survey from "./survey";
import userAuth_endpoints from "../../endpoints/userAuth_endpoints"
import signature_endpoints from "../../endpoints/signatures_endpoints";

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class Surveys extends Component {
    state = {
        // Stores the ids of all the surveys associated with the user
        surveys: [],
        loaded: false,

        // Stores information regarding the state of signing documents
        hunter_doc_manager_id: null,
        pre_tour_signed: false,

        // Stores the survey_endpoint needed for this Component
        survey_endpoint: userAuth_endpoints['userSurveys'],
        signature_endpoint: signature_endpoints['hunterDocManager'],
    };

    parseData(data) {
        /**
         * Parses data returned from the survey_endpoint and returns it in a nicer format for react
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
        axios.get(this.state.survey_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState( {surveys: this.parseData(response.data)})
            });

        /**
            Retrieves the users HunterDocManager
         */
        axios.get(this.state.signature_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState( {
                    hunter_doc_manager_id: response.data[0].id,
                    pre_tour_signed: response.data[0].is_pre_tour_signed,
                })
            });

        /**
         * Updates the users pre_tour_docs and checks to see if it is signed
         */
        let endPoint = this.state.signature_endpoint + this.state.hunter_doc_manager_id + '/';
        axios.put(endPoint,
            {
                type: 'pre_tour_check',
            })
            .catch(error => console.log('BAD', error))
            .then(response => {
                this.setState({
                    pre_tour_signed: response.data.is_pre_tour_signed
                })
            });

        this.setState({
            loaded: true,
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

        // The survey id is appended to the survey_endpoint since the put request expects the survey id as
        //  part of the url
        let endpoint = this.state.survey_endpoint + survey_id + "/";

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

    renderMessages = () => {
        if (!this.state.loaded) {
            return (
                <div>
                    <h1>Loading</h1>
                </div>
            );
        }

        let scheduler_message = "";
        if (!this.state.pre_tour_signed) {
            const pStyle = {
                textAlign: 'center',
                marginBottom: 0,
            };
            scheduler_message = (
                <div className="alert alert-info alert-dismissable" role="alert" style={pStyle}>
                    <button type="button" className="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    Please sign the pre tour doc to schedule your homes
                    <a className="btn btn-secondary btn-sm" role="button"
                       href={signature_endpoints['signaturePage']}
                       aria-disabled={true} style={{marginLeft: '10px'}}> Sign Documents </a>
                </div>
            );
        }

        return (
            <div>
                {scheduler_message}
            </div>
        );
    };

    render() {
        /**
         * Renders all the surveys
         */
        return (
            <React.Fragment>
                {this.renderMessages()}
                { this.state.surveys.map(survey =>
                    <Survey
                        key={survey.id}
                        onDelete={this.handleDelete}
                        survey_id={survey.id}
                        endpoint={this.state.survey_endpoint}
                        pre_tour_signed={this.state.pre_tour_signed}
                    />

                )}
            </React.Fragment>
        );
    }
}
export default Surveys

