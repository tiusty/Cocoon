// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveys.css'
import SurveySmall from "./surveySmall/surveySmall";
import SurveyLarge from "./surveyLarge/surveyLarge"
import signature_endpoints from "../../endpoints/signatures_endpoints";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import survey_endpoints from "../../endpoints/survey_endpoints";
import surveyIcon from './survey_icon.png';
import LoadingScreen from 'react-loading-screen';

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class Surveys extends Component {
    /**
     * This component handles displaying all the surveys
     *
     * When the user does not click on a survey all the surveys are displayed as small boxes
     *  When the user clicks on a survey box then that one survey is displayed in large form
     */

    state = {
        survey_clicked_id: undefined,
        loading_clicked: false,
        // Stores the ids of all the surveys associated with the user
        surveys: [],
        loaded: false,

        // Itinerary information
        itinerary_exists: false,

        // Stores information regarding the state of signing documents
        hunter_doc_manager_id: null,
        pre_tour_signed: false,

        // Stores the survey_endpoint needed for this Component
        survey_endpoint: survey_endpoints['rentSurvey'],
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
            survey_ids.push({
                id: c.id,
                visit_list_length: c.visit_list.length,
                favorites_length: c.favorites.length,
                url: c.url,
                name: c.name
            })
        );

        // Return the list of ids
        return survey_ids
    }

    determineActiveItinerary(data) {
        /**
         * Determines if there is an active itinerary are not
         *  An active itinerary is one that finished is not true
         *
         *  Arguments:
         *      data: list(ItinerarySerializer)
         *
         *  return (boolean):
         *      true -> If an unfinished itinerary exists
         *      false -> If there are no unfinished itineraries
         */
        let result = false;

        // Determine if any of the itineraries are not finished
        data.map(i =>
            {
                if (!i.finished) {
                    result = true
                }
            }
        );

        return result
    }

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        axios.get(this.state.survey_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({surveys: this.parseData(response.data)})
            });

        /**
         Retrieves the users HunterDocManager
         */
        axios.get(this.state.signature_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
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

        // Determines if an itinerary exists yet already or not
        axios.get(scheduler_endpoints['itineraryClient'])
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    itinerary_exists: this.determineActiveItinerary(response.data),
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
                this.setState({
                    surveys: this.parseData(response.data),
                    survey_clicked_id: undefined
                })
            });
    };

    handleSearchBarInput() {
        console.log('input changed')
    }


    renderPage() {
        /**
         * Renders the my surveys page depending on the state of the page
         */
        // If something is loading then render the loading page
        if (this.state.loading_clicked) {
            return (
                <LoadingScreen
                    loading={true}
                    bgColor='#f1f1f1'
                    spinnerColor='#9ee5f8'
                    textColor='#676767'
                    logoSrc={surveyIcon}
                    text='Please wait: Loading...'
                >
                    <div>Loadable content</div>
                </LoadingScreen>
            );
        } else {

            // If no survey is selected then render the small tiles
            if (this.state.survey_clicked_id === undefined) {
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

                        {/*<div className="row">*/}
                            {/*<div className="col-md-4 col-md-offset-4 search-bar-div">*/}
                                {/*<input type="text" disabled={true} className="input search-bar"*/}
                                       {/*placeholder="Search..."/>*/}
                                {/*<button className="btn btn-primary search-button">Search</button>*/}
                            {/*</div>*/}
                        {/*</div>*/}

                        <div className="row">
                            {this.state.surveys.map(survey =>
                                <div key={survey.id} className="col-md-3 survey">
                                    <SurveySmall
                                        key={survey.id}
                                        id={survey.id}
                                        name={survey.name}
                                        url={survey.url}
                                        favorites_length={survey.favorites_length}
                                        visit_list_length={survey.visit_list_length}
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
                // If a survey is clicked then render the large survey
            } else {
                let survey = this.state.surveys.filter(s => s.id === this.state.survey_clicked_id)[0];
                return (
                    <div className="col-md-12 survey-large">
                        <SurveyLarge
                            id={survey.id}
                            pre_tour_signed={this.state.pre_tour_signed}
                            onDelete={this.handleDelete}
                            onLargeSurveyClose={this.handleLargeSurveyClose}
                            itinerary_exists={this.state.itinerary_exists}
                        />
                    </div>
                );
            }
        }
    }

    setLoadingClick = () => {
        /**
         * Sets loading_clicked to true
         */
        this.setState({loading_clicked: true})
    };

    handleLargeSurveyClose = () => {
        /**
         * Handles closing the large survey.
         *
         * Since information can be modified on the large tile, when the user closes
         * it then the data on the page needs to be updated. Also, the clicked survey value
         * should go back to undefined so the small survey tiles load again
         */
        this.setState({survey_clicked_id: undefined});

        // See if any of the data changed
        axios.get(this.state.survey_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({surveys: this.parseData(response.data)})
            });
    };

    handleClickSurvey = (id) => {
        /**
         * Handles click on the survey box to load the large survey.
         *
         * If the click is on the extra box then the survey should load
         */
        if (id !== undefined) {
            this.setState({survey_clicked_id: id})
        } else {
            this.setLoadingClick();
            window.location = survey_endpoints['rentingSurvey']
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
