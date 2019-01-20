// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'

// Import Cocoon Components
import CSRFToken from '../../../common/csrftoken'
import HomeTiles from "../../../common/homeTile/homeTiles";
import scheduler_endpoints from"../../../endpoints/scheduler_endpoints"

// Import Styling
import './tourSummary.css'

export default class TourSummary extends Component {

    state = {
        // State for the tour duration
        refresh_duration: true,
        duration: undefined,
    };

    componentDidUpdate(prevProps) {

        // When the visit list changes, updates the tour estimated time
        if (prevProps.visit_list !== this.props.visit_list) {
            // Make sure the survey id is valid and that the visit list is not less than 0
            if (this.props.survey_id !== undefined && this.props.visit_list.length >= 0) {
                let endpoint = scheduler_endpoints['itineraryDuration'] + this.props.survey_id;
                this.setState({
                    refresh_duration: true,
                });
                axios.get(endpoint)
                    .catch(error => {
                        console.log('BAD', error);
                        this.setState({
                            refresh_duration: false,
                        })
                    })
                    .then(response => {
                            this.setState({
                                duration: response.data.duration,
                                refresh_duration: false,
                            })
                        },
                    )
            }
        }
    }

    renderVisitList() {
        /**
         * Renders the visit list homes
         */
        if (this.props.visit_list.length === 0) return <h3 className="tour-summary-h3">No homes in visit list</h3>;
        return (
            <div className="survey-large-home">
                <HomeTiles
                    homes={this.props.visit_list}
                    visit_list={this.props.visit_list}
                    curr_favorites={this.props.visit_list}
                    onVisitClick={this.props.onHandleVisitListClicked}
                    canFavorite={false}
                    canVisit={true}
                />
            </div>
        );
    };

    determineScheduleButtonStatus() {
        if (this.props.visit_list <= 0) {
            return true
        } else {
            return false
        }
    }

    renderPage() {
        if (!this.props.loaded) {
            return <p className="tour-summary-text">Loading</p>
        } else if (this.props.itinerary_scheduled && this.props.survey_id === undefined) {
            return (
                <>
                    <p className="tour-summary-text">To review more details of your tour please click below:</p>
                    <a  href={scheduler_endpoints['clientScheduler']} onClick={this.props.onLoadingClicked}
                        className="btn btn-primary survey-small-load-button">View Tour</a>
                </>
            );
        } else if (this.props.itinerary_scheduled && this.props.survey_id !== undefined) {
            return (
                <>
                    <p className="tour-summary-text">To review more details of your tour please click below:</p>
                    <a  href={scheduler_endpoints['clientScheduler']} onClick={this.props.onLoadingClicked}
                        className="btn btn-primary survey-small-load-button">View Tour</a>
                    <h2 className="tour-summary-semi-bold">For reference, your visit list is below</h2>
                    <p className="tour-summary-text">Remember you cannot schedule another tour until your current tour
                        is completed</p>
                    {this.renderVisitList()}
                </>
            );
        } else if (!this.props.is_pre_tour_signed && !this.props.pre_tour_forms_created) {
            return (
                <>
                    <p className="tour-summary-text">You need to sign the pre tour documents before scheduling a tour</p>
                    <button className="btn btn-primary"
                            onClick={this.props.onHandleOnClickCreateDocument}>{this.props.refreshing_document_status ? 'Loading' : 'Send'}</button>
                </>
            );
        } else if (!this.props.is_pre_tour_signed && this.props.pre_tour_forms_created) {
            return (
                <>
                    <p className="tour-summary-text">Refresh your document status!</p>
                    <button className="btn btn-primary tour-summary-doc-button"
                            onClick={this.props.onHandleOnClickRefreshDocument}>{this.props.refreshing_document_status ? 'Loading' : 'Refresh'}</button>
                    <p className="tour-summary-text">Can't find the email?</p>
                    <button className="btn btn-primary tour-summary-doc-button"
                            onClick={this.props.onHandleOnClickResendDocument}>{this.props.refreshing_document_status ? 'Loading' : 'Resend'}</button>
                </>
            );
        } else if (this.props.is_pre_tour_signed && this.props.pre_tour_forms_created && this.props.survey_id === undefined) {
            return(
                <>
                    <p className="tour-summary-text">Please expand a survey to get started scheduling a tour</p>
                    <p className="tour-summary-text">Remember you may only have one tour scheduled at a time</p>
                </>
            );

        } else if (this.props.is_pre_tour_signed && this.props.pre_tour_forms_created && this.props.survey_id !== undefined) {
            return (
                <>
                    <p className="tour-summary-text">When you are done adding homes that you want to tour, click schedule!</p>
                    <p className="tour-summary-text">Remember you can only have one tour scheduled at a time</p>
                    <p className="tour-summary-text">Estimated duration: {this.state.refresh_duration ? 'Loading' : Math.round(this.state.duration/60) + ' mins'}</p>
                    <form method="post" style={{marginTop: '10px'}}>
                        <CSRFToken/>
                        <button name="submit-button"
                                className="btn btn-success"
                                value={this.props.survey_id}
                                disabled={this.determineScheduleButtonStatus()}
                                type="submit">Schedule!
                        </button>
                    </form>
                    <h2 className="tour-summary-semi-bold">Visit List</h2>
                    {this.renderVisitList()}
                </>
            );

        }
    }

    render() {
        return(
            <div className="tour-summary">
                <h2 className="tour-summary-title">Tour Summary</h2>
                {this.renderPage()}
            </div>
        );
    }
}
