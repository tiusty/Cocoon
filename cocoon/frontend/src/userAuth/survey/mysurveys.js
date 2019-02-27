// Import React Components
import React from 'react';
import {Component} from 'react';
import axios from 'axios';

// Import Cocoon Components
import signature_endpoints from "../../endpoints/signatures_endpoints";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import survey_endpoints from "../../endpoints/survey_endpoints";

import Preloader from '../../common/preloader';
import TourSetupCTA from './tourSetupCTA';
import SurveyPicker from './surveyPicker';
import TourChecklist from './tourChecklist';
import TourSetupContent from './tourSetupMainContent';

// Import styling
import './mysurveys.css'
import TourSummary from "../survey_old/mysurveys";

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
        last_resend_request_pre_tour: undefined,

        // Handles opening a large survey
        survey_clicked_id: undefined,
        visit_list: [],
        favorites: [],

        // Stores the ids of all the surveys associated with the user
        surveys: [],
        loaded: false,
        // loaded: true,

        // Itinerary information
        itinerary_scheduled: false,

        // Stores information regarding the state of signing documents

        // Stores the survey_endpoint needed for this Component
        survey_endpoint: survey_endpoints['rentSurvey'],
        signature_endpoint: signature_endpoints['hunterDocManager'],

        activeResultsUrl: undefined
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
                survey_name: c.survey_name
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
                this.setState({
                    surveys: this.parseData(response.data)
                }, () => this.loadMostRecentSurvey());
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
                    // loaded: true,
                    is_pre_tour_signed: response.data.is_pre_tour_signed,
                    pre_tour_forms_created: response.data.pre_tour_forms_created,
                })
            });

        // Determines if an itinerary exists yet already or not
        axios.get(scheduler_endpoints['itineraryClient'])
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    itinerary_scheduled: this.determineActiveItinerary(response.data),
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
                    is_pre_tour_signed: response.data.is_signed,
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
                    is_pre_tour_signed: response.data.is_signed,
                    last_resend_request_pre_tour: response.data.last_resend,
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
            .then(response => {
                    this.setState({
                        id: response.data.id,
                        is_pre_tour_signed: response.data.is_signed,
                        last_resend_request_pre_tour: response.data.last_resend,
                        created: true,
                        refreshing_document_status: false,
                    })
                }
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

    loadMostRecentSurvey = () => {
        const recentSurveyId = this.state.surveys[0].id;
        this.handleClickSurvey(recentSurveyId);
    }

    handleClickSurvey = (id) => {
        /**
         * Handles click on the expand button for a survey
         *
         * After the survey id is set, it will retrieve the visit list for that survey
         */
        this.setState({survey_clicked_id: id}, () => {
            this.retrieveHomes();
            this.setActiveResults();
        });
    };

    setActiveResults = () => {
        let activeSurvey = this.state.surveys.find(s => s.id === this.state.survey_clicked_id);
        let url = survey_endpoints['rentSurveyResult'] + activeSurvey.url;
        this.setState({
            activeResultsUrl: url,
            activeSurvey: activeSurvey,
            loaded: true
        })
    }

    handleLargeSurveyClose = () => {
        /**
         * Handles closing the large survey.
         *
         * Since information can be modified on the large tile, when the user closes
         * it then the data on the page needs to be updated. Also, the clicked survey value
         * should go back to undefined so the small survey tiles load again
         */
        this.setState({survey_clicked_id: undefined, visit_list: [], favorites: [],});

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
        // e.stopPropagation();

        // The survey id is passed to the put request to update the state of that particular survey
        let endpoint = survey_endpoints['rentSurvey'] + this.state.survey_clicked_id + "/";
        axios.put(endpoint,
            {
                home_id: home.id,
                type: 'visit_toggle'

            })
            // Though the visit list is being updated, the response includes the favorite list so update
            // the favorite list as well
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    visit_list: response.data.visit_list,
                    favorites: response.data.favorites,
                })
            );
    };


    handleFavoriteClick = (home) => {
        /**
         * This function handles toggles a home to either add or remove from the favorites list
         *
         * The response includes the updated favorite and visit list for the survey
         * @type {string}
         */
        // The survey id is passed to the put request to update the state of that particular survey
        let endpoint = survey_endpoints['rentSurvey'] + this.state.survey_clicked_id + "/";
        axios.put(endpoint,
            {
                home_id: home.id,
                type: 'favorite_toggle',

            })
            .catch(error => console.log('BAD', error))
            // Though the favorites is being updated, the response includes the visit list so update with the
            // latest visit list as well
            .then(response =>
                this.setState({
                    favorites: response.data.favorites,
                    visit_list: response.data.visit_list,
                })
            );
    }

    retrieveHomes = () => {
        let endpoint = survey_endpoints['rentSurvey'] + this.state.survey_clicked_id;
        axios.get(endpoint)
            .catch(error => console.log('BAD', error))
            .then(response => {
                    this.setState({
                        visit_list: response.data.visit_list,
                        favorites: response.data.favorites
                    })
                }
            )
    };

    render() {
        if (this.state.loading_clicked || !this.state.loaded) {
            return (
                <div style={{width: '100%', height: '80vh'}}>
                    <Preloader color='var(--teal)'/>
                </div>
            );
        } else {
            return (
                <div className="tour-setup-container">
                    <div className="tour-setup-sidebar">
                        <TourSetupCTA
                            survey_id={this.state.survey_clicked_id}
                            visit_list={this.state.visit_list}
                            loaded={this.state.loaded}
                            pre_tour_forms_created={this.state.pre_tour_forms_created}
                            is_pre_tour_signed={this.state.is_pre_tour_signed}
                            itinerary_scheduled={this.state.itinerary_scheduled}
                            last_resend_request_pre_tour={this.state.last_resend_request_pre_tour}
                            refreshing_document_status={this.state.refreshing_document_status}
                            onHandleOnClickCreateDocument={this.handleOnClickCreateDocument}
                            onHandleOnClickRefreshDocument={this.handleOnClickRefreshDocument}
                            onHandleOnClickResendDocument={this.handleOnClickResendDocument}
                        />
                        <SurveyPicker
                            survey_id={this.state.survey_clicked_id}
                            surveys={this.state.surveys}
                            handleClickSurvey={this.handleClickSurvey}
                        />
                        <TourChecklist
                            surveys={this.state.surveys}
                            pre_tour_forms_created={this.state.pre_tour_forms_created}
                            is_pre_tour_signed={this.state.is_pre_tour_signed}
                            survey_clicked_id={this.state.survey_clicked_id}
                            visit_list={this.state.visit_list}
                            favorites={this.state.favorites}
                            itinerary_scheduled={this.state.itinerary_scheduled}
                            activeResultsUrl={this.state.activeResultsUrl}
                            onHandleOnClickCreateDocument={this.handleOnClickCreateDocument}
                            onHandleOnClickResendDocument={this.handleOnClickResendDocument}
                        />
                    </div>
                    <div className="tour-box tour-setup-main">
                        <TourSetupContent
                            activeResultsUrl={this.state.activeResultsUrl}
                            activeSurvey={this.state.activeSurvey}
                            favorites={this.state.favorites}
                            survey_clicked_id={this.state.survey_clicked_id}
                            visit_list={this.state.visit_list}
                            handleVisitClick={this.handleVisitClick}
                            handleFavoriteClick={this.handleFavoriteClick}
                        />
                    </div>
                </div>
            );
        }

    }
}