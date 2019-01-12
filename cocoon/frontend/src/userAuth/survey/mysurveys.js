// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'
import LoadingScreen from 'react-loading-screen';

// Import Cocoon Components
import SurveySmall from "./surveySmall/surveySmall";
import SurveyLarge from "./surveyLarge/surveyLarge"
import signature_endpoints from "../../endpoints/signatures_endpoints";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import survey_endpoints from "../../endpoints/survey_endpoints";
import TourSummary from "./tourSummary/tourSummary";

// Import icons
import surveyIcon from './survey_icon.png';

// Import styling
import './mysurveys.css'

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class MySurveys extends Component {

    state = {
        // State regarding the document
        hunter_doc_manager_id: null,
        pre_tour_template_id: null,
        is_pre_tour_signed: false,
        refreshing_document_status: false,
        pre_tour_forms_created: false,

        // Handles opening a large survey
        survey_clicked_id: undefined,
        visit_list: [],

        loading_clicked: false,
        // Stores the ids of all the surveys associated with the user
        surveys: [],
        loaded: false,

        // Itinerary information
        itinerary_exists: false,

        // Stores information regarding the state of signing documents

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
                visit_list: c.visit_list,
                favorites: c.favorites,
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
        data.map(i => {
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
                    pre_tour_forms_created: response.data[0].pre_tour_forms_created,
                    is_pre_tour_signed: response.data[0].is_pre_tour_signed,
                })
            });

        /**
         * Retrieves the hunter doc template id for the pre tour forms
         */
        axios.get(signature_endpoints['hunterDocTemplate'], {params: {type: 'pre_tour'}})
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({pre_tour_template_id: response.data[0].id})
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
                    is_pre_tour_signed: response.data.is_pre_tour_signed,
                    pre_tour_forms_created: response.data.pre_tour_forms_created,
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

    createDocument = () => {
        /**
         * Sends an API request to create the document specified by the template type
         */
        this.setState({
            refreshing_document_status: true,
        });
        let endpoint = signature_endpoints['hunterDoc'];
        axios.post(endpoint,
            {
                template_type_id: this.state.pre_tour_template_id,
            })
            .catch(error => {
                this.setState({
                    refreshing_document_status: false,
                });
                console.log('Bad', error)
            })
            .then(response =>
                this.setState({
                    id: response.data.id,
                    is_signed: response.data.is_signed,
                    pre_tour_forms_created: true,
                    refreshing_document_status: false,
                })
            );
    };

    refreshDocumentStatus = () => {
        /**
         * Sends an API request to update the status of the current document
         */
        this.setState({
            refreshing_document_status: true,
        });
        let endpoint = signature_endpoints['hunterDoc'] + this.state.pre_tour_template_id + '/';
        axios.put(endpoint,
            {
                'type': 'update'
            })
            .catch(error => {
                this.setState({
                    refreshing_document_status: false,
                });
                console.log('Bad', error)
            })
            .then(response =>
                this.setState({
                    id: response.data.id,
                    is_signed: response.data.is_signed,
                    refreshing_document_status: false,
                })
            );
    };

    resendDocument = () => {
        /**
         * Sends an API request to resend the current document
         */
        this.setState({
            refreshing_document_status: true,
        });
        let endpoint = signature_endpoints['hunterDoc'] + this.state.pre_tour_template_id + '/';
        axios.put(endpoint,
            {
                'type': 'resend'
            })
            .catch(error => {
                this.setState({
                    refreshing_document_status: false,
                });
                console.log('Bad', error)
            })
            .then(response =>
                this.setState({
                    id: response.data.id,
                    is_signed: response.data.is_signed,
                    created: true,
                    refreshing_document_status: false,
                })
            );
    };

    handleOnClickRefreshDocument = () => {
        if (this.state.refreshing_document_status) {
            return false
        } else {
            this.refreshDocumentStatus()
        }
    };


    handleOnClickCreateDocument = () => {
        if (this.state.refreshing_document_status) {
            return false
        } else {
            this.createDocument()
        }
    };

    handleOnClickResendDocument = () => {
        if (this.state.refreshing_document_status) {
            return false
        } else {
            this.resendDocument()
        }
    }

    handleClickSurvey = (id) => {
        /**
         * Handles click on the expand button for a survey
         *
         * After the survey id is set, it will retrieve the visit list for that survey
         */
        this.setState({survey_clicked_id: id}, () => this.retrieveVisitList());
    };

    handleLargeSurveyClose = () => {
        /**
         * Handles closing the large survey.
         *
         * Since information can be modified on the large tile, when the user closes
         * it then the data on the page needs to be updated. Also, the clicked survey value
         * should go back to undefined so the small survey tiles load again
         */
        this.setState({survey_clicked_id: undefined, visit_list: []});

        // See if any of the data changed
        axios.get(this.state.survey_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({surveys: this.parseData(response.data)})
            });
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
        let endpoint = survey_endpoints['rentSurvey'] + this.state.survey_clicked_id + "/";
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

    retrieveVisitList = () => {
        let endpoint = survey_endpoints['rentSurvey'] + this.state.survey_clicked_id;
        axios.get(endpoint)
            .catch(error => console.log('BAD', error))
            .then(response => {
                    this.setState({
                        visit_list: response.data.visit_list,
                    })
                }
            )
    };


    renderSurveysBlock() {
        // If there are no surveys then render a take survey page
        if (this.state.surveys.length <= 0) {
            return (
                <div className="my-surveys-none-div">
                    <h2>You have no surveys!</h2>
                    <p>Please click below to take a survey so we can find you your perfect home!</p>
                    <a href={survey_endpoints['rentingSurvey']} className="btn btn-success"
                       onClick={this.setLoadingClick}>Take Survey</a>
                </div>
            );
        // If no survey is selected then render the small tiles
        } else if (this.state.survey_clicked_id === undefined) {
            return (
                <>
                    {this.state.surveys.map(survey =>
                        <div key={survey.id} className="survey-small">
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
                </>
            );
        }
        // If a survey is clicked then render the large survey
        else {
            let survey = this.state.surveys.filter(s => s.id === this.state.survey_clicked_id)[0];
            return (
                <div className="survey-large">
                    <SurveyLarge
                        id={survey.id}
                        visit_list={this.state.visit_list}
                        onDelete={this.handleDelete}
                        onLargeSurveyClose={this.handleLargeSurveyClose}
                        onLoadingClicked={this.setLoadingClick}
                        onHandleVisitListClicked={this.handleVisitClick}
                    />
                </div>
            );

        }
    }

    setLoadingClick = () => {
        /**
         * Sets loading_clicked to true
         */
        this.setState({loading_clicked: true})
    };

    renderMySurveysMessages() {
        if (!this.state.loaded) {
            return <p className='surveys-title-text'>Loading</p>
        } else if (!this.state.is_pre_tour_signed) {
            return (
                <>
                    <p className="surveys-title-text-semi-bold">Here you can load and view your past surveys for your
                        different roommate groups!</p>
                    <p className="surveys-title-text">When you are ready please follow the steps in the Tour Summary
                        column on the right to sign your documents so you can schedule a tour!</p>
                </>
            );
        } else if (!this.state.itinerary_exists && this.state.survey_clicked_id === undefined) {
            return (
                <>
                    <p className="surveys-title-text-semi-bold">Lets schedule a tour for you so you can find your
                        perfect home!</p>
                    <p className='surveys-title-text'>Please expand a survey to add homes to the tour. Remember you can only
                    schedule one tour at a time, therefore you cannot schedule a tour for two different roommate groups at once</p>
                </>
            );
        } else if (!this.state.itinerary_exists && this.state.survey_clicked_id !== undefined) {
            return (
                <>
                    <p className="surveys-title-text-semi-bold">Please add homes to your tour!</p>
                    <p className='surveys-title-text'>Add homes from your favorites by clicking on the check mark on the home, you can
                    view more info about the home by clicking on the home box. If you want to add more homes you can click load survey at the
                    bottom of where your favorite homes are located</p>
                </>
            );
        } else if (this.state.itinerary_exists) {
            return (
                <>
                    <p className="surveys-title-text-semi-bold">You already have a tour scheduled!</p>
                    <p className='surveys-title-text'>You can view more information about your tour in the tour summary column</p>
                </>
            );
        }
    }

    render() {
        if (this.state.loading_clicked || !this.state.loaded) {
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
            return (
                <div className="row">
                    <div className="col-md-8">
                        <div className="surveys-div">
                            <h2 className="surveys-title">My Surveys</h2>
                            {this.renderMySurveysMessages()}
                        </div>
                        <div className="surveys-main">
                            {this.renderSurveysBlock()}
                        </div>
                    </div>
                    <div className="col-md-4">
                        <TourSummary
                            loaded={this.state.loaded}
                            visit_list={this.state.visit_list}
                            survey_id={this.state.survey_clicked_id}
                            is_pre_tour_signed={this.state.is_pre_tour_signed}
                            pre_tour_forms_created={this.state.pre_tour_forms_created}
                            itinerary_scheduled={this.state.itinerary_exists}
                            refreshing_document_status={this.state.refreshing_document_status}
                            onHandleOnClickCreateDocument={this.handleOnClickCreateDocument}
                            onHandleOnClickRefreshDocument={this.handleOnClickRefreshDocument}
                            onHandleOnClickResendDocument={this.handleOnClickResendDocument}
                            onHandleVisitListClicked={this.handleVisitClick}
                            onLoadingClick={this.setLoadingClick}
                        />
                    </div>
                </div>
            );
        }

    }
}