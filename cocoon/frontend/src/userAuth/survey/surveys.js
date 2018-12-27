// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveys.css'
import SurveySmall from "./surveySmall";
import SurveyLarge from "./surveyLarge"
import signature_endpoints from "../../endpoints/signatures_endpoints";
import survey_endpoints from "../../endpoints/survey_endpoints";

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class Surveys extends Component {

    state = {
        survey_clicked_id: undefined,
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
                this.setState( {
                    surveys: response.data,
                    survey_clicked_id: undefined
                })
            });
    };


    renderPage() {
        if(this.state.loading_clicked) {
            return <p> Loading page </p>
        } else {
            if(this.state.survey_clicked_id === undefined) {
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

                        <div className="row">
                            {this.state.surveys.map(survey =>
                                <div key={survey.id} className="col-md-3 survey">
                                    <SurveySmall
                                        key={survey.id}
                                        id={survey.id}
                                        name={survey.name}
                                        url={survey.url}
                                        favorites={survey.favorites}
                                        visit_list={survey.visit_list}
                                        onLoadingClicked={this.setLoadingClick}
                                        onClickSurvey={this.handleClickSurvey}
                                    />
                                </div>
                            )}
                            <div className="col-md-3 survey">
                                <SurveySmall
                                    default_survey={true}
                                    onClickSurvey={this.handleClickSurvey}
                                />
                            </div>
                        </div>
                    </>
                );
            } else {
                let survey = this.state.surveys.filter(s => s.id === this.state.survey_clicked_id)[0];
                return (
                    <div className="col-md-12 survey-large">
                        <SurveyLarge
                            id = {survey.id}
                            name={survey.name}
                            large_survey={true}
                            favorites={survey.favorites}
                            visit_list={survey.visit_list}
                            onDelete={this.handleDelete}
                            onLargeSurveyClose={this.handleLargeSurveyClose}
                        />
                    </div>
                );
            }
        }
    }

    setLoadingClick = () => {
        this.setState({loading_clicked: true})
    };

    handleLargeSurveyClose = () => {
        this.setState({survey_clicked_id:undefined})
    }

    handleClickSurvey = (id) => {
        if(id !== undefined) {
            this.setState({survey_clicked_id: id})
        } else {
            console.log("default clicked")
        }
    };


    render() {
        return (
            <>
                    {this.renderPage()}
            </>
        );
    }
}
