// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveys.css'
import Survey from "./survey";
import signature_endpoints from "../../endpoints/signatures_endpoints";
import survey_endpoints from "../../endpoints/survey_endpoints";

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class Surveys extends Component {

    state = {
        loading_clicked: false,
        // Stores the ids of all the surveys associated with the user
        surveys: [],
        loaded: false,

        // Stores information regarding the state of signing documents
        hunter_doc_manager_id: null,
        pre_tour_signed: false,

        // Stores the survey_endpoint needed for this Component
        survey_endpoint: survey_endpoints['rentSurvey'],
        signature_endpoint: signature_endpoints['hunterDocManager'],
    };

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        axios.get(this.state.survey_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState( {surveys: response.data})
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
         * Updates the users pre_tour_docs and checks to see if it is signed.
         *  Since the id for the url doesn't matter, null can be passed so the
         *  update function is called
         */
        let endPoint = this.state.signature_endpoint + 'null' + '/';
        axios.put(endPoint,
            {
                type: 'pre_tour_check',
            })
            .catch(error => console.log('BAD', error))
            .then(response => {
                this.setState({
                    loaded: true,
                    pre_tour_signed: response.data.is_pre_tour_signed
                })
            });
    }


    renderPage() {
        if(this.state.loading_clicked) {
            return <p> Loading page </p>
        } else {
            return (
                <>
                    {this.state.surveys.map(survey =>
                        <div key={survey.id} className="col-md-3 survey">
                            <Survey
                                key={survey.id}
                                id={survey.id}
                                name={survey.name}
                                url={survey.url}
                                favorites={survey.favorites}
                                visit_list={survey.visit_list}
                                onLoadingClicked={this.setLoadingClick}
                            />
                        </div>
                    )}
                    <div className="col-md-3 survey">
                        <Survey
                            default_survey={true}
                        />
                    </div>
                </>
            );
        }
    }

    setLoadingClick = () => {
        this.setState({loading_clicked: true})
    };


    render() {
        return (
            <>
                <div className="row">
                    <div className="col-md-6 col-md-offset-3">
                        <p className="my-survey-header">Roommate Groups</p>
                    </div>
                    <div className="col-md-1 col-md-offset-2">
                        <button className="btn btn-primary help-button">Help</button>
                    </div>
                </div>

                <div className="row">
                    <div className="col-md-6 col-md-offset-2 search-bar-div">
                        <input type="text" className="input search-bar" placeholder="Search..." />
                        <button className="btn btn-primary search-button">Search</button>
                    </div>
                </div>

                <div className="row surveys">
                    {this.renderPage()}
                </div>
            </>
        );
    }
}
