// Import React Components
import React from 'react';
import {Component} from 'react';
import axios from 'axios';

// Import Cocoon Components
import signature_endpoints from "../../endpoints/signatures_endpoints";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import survey_endpoints from "../../endpoints/survey_endpoints";
import user_auth_endpoints from "../../endpoints/userAuth_endpoints"

import Preloader from '../../common/preloader';
import TourSetupCTA from './tourSetupCTA';
import SurveyPicker from './surveyPicker';
import UserPicker from './userPicker';
import TourChecklist from './tourChecklist';
import TourSetupContent from './tourSetupMainContent';

// Import styling
import './myclients.css'

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class MyClients extends Component {

    state = {
        // State regarding the document
        // Commenting out old values so we can easily revert it when we want the pre tour docuemnts back
        // hunter_doc_manager_id: null,
        // pre_tour_template_id: null,
        // is_pre_tour_signed: false,
        // refreshing_document_status: false,
        // pre_tour_forms_created: false,
        // last_resend_request_pre_tour: undefined,
        hunter_doc_manager_id: null,
        pre_tour_template_id: null,
        is_pre_tour_signed: true,
        refreshing_document_status: false,
        pre_tour_forms_created: true,
        last_resend_request_pre_tour: undefined,

        // Handles opening a large survey
        activeSurvey: undefined,
        survey_clicked_id: undefined,
        client_clicked_id: undefined,
        visit_list: [],
        favorites: [],

        // Stores the ids of all the surveys associated with the user
        clients: [],
        surveys: [],
        loaded: false,

        // Itinerary information
        itinerary_scheduled: false,


        // Stores the survey_endpoint needed for this Component
        survey_endpoint: survey_endpoints['rentSurvey'],
        signature_endpoint: signature_endpoints['hunterDocManager'],

        activeResultsUrl: undefined,
        viewing_snapshot: false,
        clicked_home: undefined,
        viewing_home: false,
        survey_url_param: null,
        key_param: null
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

    componentDidMount() {

        /**
         *  Checks the URL for any parameters to determine which survey to load
         */
        this.checkUrl();

        /**
         *  Retrieves all the surveys associated with the user
         */
        axios.get(user_auth_endpoints['agentClients'])
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    clients: response.data
                }, () => this.sortUsers());
            });
    }

    get_client_surveys = (id) => {
        axios.get(survey_endpoints['rentSurveyAgent'] + id + '/')
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    surveys: this.parseData(response.data)
                }, () => this.sortSurveys());
            });
    }

    checkUrl = () => {
        const urlString = window.location.href;
        const url = new URL(urlString);
        if (url.searchParams.get('survey_url')) {
            this.setState({
                survey_url_param: url.searchParams.get('survey_url'),
            })
        }
        if (url.searchParams.get('key') === 'snapshot') {
            this.setState({
                key_param: 'snapshot'
            })
        }
    }

    sortUsers = () => {
        /*
         *  Sorts clients by descending order then determines which to load
        */
        if (this.state.clients.length !== 0) {
            let clientCopy = [...this.state.clients];
            clientCopy.sort((a, b) => b.id - a.id);
            this.setState({
                clients: clientCopy
            }, () => {
                this.loadClients();
            })
        } else {
            this.setState({
                loaded: true
            })
        }
    };

    sortSurveys = () => {
        /*
         *  Sorts surveys by descending order then determines which to load
        */
        if (this.state.surveys.length !== 0) {
            let surveyCopy = [...this.state.surveys];
            surveyCopy.sort((a, b) => b.id - a.id);
            this.setState({
                surveys: surveyCopy
            }, () => {
                this.loadSurvey();
            })
        } else {
            this.setState({
                loaded: true
            })
        }
        this.loadSurvey();
    };

    loadSurvey = () => {
        /*
        * Looks for a param: survey_url to determine which to load
        * Looks for a param: key=snapshot to determine if to load snapshot view
        * If neither exists, loads the most recent survey
        */
        if (this.state.surveys.length > 0) {
            let id;
            if (this.state.survey_url_param) {
                let survey_match = this.state.surveys.find(survey => survey.url === this.state.survey_url_param);
                if (survey_match) {
                    id = survey_match.id
                } else {
                    id = this.state.surveys[0].id
                }
            } else {
                id = this.state.surveys[0].id
            }

            this.handleClickSurvey(id);

            if (this.state.key_param === 'snapshot') {
                this.handleSnapshotClick();
            }
        } else {
            this.setState({
                survey_clicked_id: undefined,
                activeSurvey: undefined,
            })
        }
    }


    clearSurvey() {
    }

    loadClients = () => {
        /*
        * Looks for a param: survey_url to determine which to load
        * Looks for a param: key=snapshot to determine if to load snapshot view
        * If neither exists, loads the most recent survey
        */
        let id;
        id = this.state.clients[0].id;
        this.handleClickClient(id);

        if (this.state.key_param === 'snapshot') {
            this.handleSnapshotClick();
        }

        this.setState({
            loaded:true
        })

    }

    handleClickSurvey = (id) => {
        /**
         * Handles click on the expand button for a survey
         *
         * After the survey id is set, it will retrieve the visit list for that survey
         */
        this.setState({
            survey_clicked_id: id,
            viewing_snapshot: false
        }, () => {
            this.handleCloseHomeTileLarge();
            this.retrieveHomes();
            this.setActiveResults();
        });
    };

    handleClickClient = (id) => {
        /**
         * Handles click on the expand button for a client
         *
         * After the survey id is set, it will retrieve the visit list for that survey
         */
        this.setState({
            client_clicked_id: id,
            viewing_snapshot: false
        }, () => {
            this.handleCloseHomeTileLarge();
            this.get_client_surveys(id);
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

    handleHomeClick = (id) => {
        this.setState({
            clicked_home: id,
            viewing_home: true
        })
    }

    handleCloseHomeTileLarge = () => {
        this.setState({
            clicked_home: undefined,
            viewing_home: false
        })
    }

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

    handleSnapshotClick = () => {
        this.setState({
            viewing_snapshot: !this.state.viewing_snapshot
        })
    }

    checkForSurvey = () => {
        if (this.state.clients.length === 0) {
            return (
                <div className="no-surveys-wrapper">
                    <h1>You haven't taken a survey yet!</h1>
                    <a href={survey_endpoints['rentingSurvey']}>Take one now</a>
                </div>
            );
        } else {
            return (
                <div className="tour-setup-container">
                    <div className="tour-setup-sidebar">
                        {/*<TourSetupCTA*/}
                            {/*survey_id={this.state.survey_clicked_id}*/}
                            {/*activeSurvey={this.state.activeSurvey}*/}
                            {/*visit_list={this.state.visit_list}*/}
                            {/*loaded={this.state.loaded}*/}
                            {/*pre_tour_forms_created={this.state.pre_tour_forms_created}*/}
                            {/*is_pre_tour_signed={this.state.is_pre_tour_signed}*/}
                            {/*itinerary_scheduled={this.state.itinerary_scheduled}*/}
                            {/*last_resend_request_pre_tour={this.state.last_resend_request_pre_tour}*/}
                            {/*refreshing_document_status={this.state.refreshing_document_status}*/}
                            {/*onHandleOnClickCreateDocument={this.handleOnClickCreateDocument}*/}
                            {/*onHandleOnClickRefreshDocument={this.handleOnClickRefreshDocument}*/}
                            {/*onHandleOnClickResendDocument={this.handleOnClickResendDocument}*/}
                        {/*/>*/}
                        <UserPicker
                            client_id={this.state.client_clicked_id}
                            clients={this.state.clients}
                            handleClickClient={this.handleClickClient}
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
                            handleHomeClick={this.handleHomeClick}
                            handleCloseHomeTileLarge={this.handleCloseHomeTileLarge}
                            clicked_home={this.state.clicked_home}
                            viewing_home={this.state.viewing_home}
                            viewing_snapshot={this.state.viewing_snapshot}
                            handleSnapshotClick={this.handleSnapshotClick}
                            deleteSurvey={this.deleteSurvey}
                            key_param={this.state.key_param}
                        />
                    </div>
                </div>
            );
        }
    }

    render() {
        if (!this.state.loaded) {
            return (
                <div style={{width: '100%', height: '80vh'}}>
                    <Preloader color='var(--teal)'/>
                </div>
            );
        } else {
            return (
                <>
                    {this.checkForSurvey()}
                </>
            )
        }

    }
}
