import React, {Component} from 'react';
import { createPortal } from 'react-dom';
import moment from 'moment';
import CSRFToken from '../../../common/csrftoken';
import scheduler_endpoints from '../../../endpoints/scheduler_endpoints';

import CocoonModal from '../../../common/cocoonModal';
import axios from "axios";

export default class TourSetupCTA extends Component {

    constructor(props) {
        super(props);
        this.state = {
            has_off_market: false,
            homes_off_market: 0,
            isScheduling: false
        }
    }

    componentDidMount() {
        this.checkIfOffMarket();
    }

    componentDidUpdate(prevProps) {
        if (this.props.visit_list !== prevProps.visit_list) {
            this.checkIfOffMarket();
        }
        if (this.props.survey_id !== prevProps.survey_id) {
            this.setState({
                isScheduling: false,
            })
        }
    }

    checkIfOffMarket = () => {
        let { visit_list } = this.props;
        let error_count = 0;
        for (let i = 0; i < visit_list.length; i++) {
            if (visit_list[i].on_market === false) {
                error_count += 1;
            }
        }
        if (error_count > 0) {
            this.setState({
                has_off_market: true,
                homes_off_market: error_count
            })
        } else {
            this.setState({
                has_off_market: false,
                homes_off_market: 0
            })
        }
    }

    determineScheduleButtonStatus() {
        if (this.props.visit_list.length <= 0 || this.props.visit_list.length > 5 || this.state.has_off_market === true) {
            return true;
        } else {
            return false;
        }
    }

    toggleScheduling = () => {
        this.setState({
            isScheduling: !this.state.isScheduling
        })
    }

    scheduleTour = () => {
        // posts the schedule to backend
        this.setState({loading: true});
        axios.post(scheduler_endpoints['itineraryClient'],
            {
                survey_id: this.props.survey_id,
            })
            .catch(error => {
                console.log('BAD', error);
                this.setState({loading: false})
            })
            .then(response => {
                    // On successful form submit then redirect to survey results page
                    if (response.data.result) {
                        window.location = scheduler_endpoints['clientScheduler'];
                    } else {
                        console.log('error')
                        this.setState({loading: false})
                    }
                }
            );
    }

    loadModal = () => {
        if (this.state.isScheduling && !this.determineScheduleButtonStatus()) {
            return createPortal(
                <CocoonModal
                    headline={'Congrats on scheduling a tour! We just want to let you know of a few things:'}
                    subHeadline={`By scheduling this tour you recognize that you will not be able to schedule another tour until this one is complete. You will need to find blocks of time that will allow for the full duration of the tour. If you believe you will not be free for the full duration of the tour then please remove homes until the tour duration is at a satisfactory level. We look forward to being on the tour with you and hope you find yours with us!`}
                    closeModalText={'Cancel'}
                    confirmText={this.state.loading ? "Loading" : "Confirm"}
                    confirmOnClick={this.state.loading ? null : this.scheduleTour}
                    closeModalOnClick={this.toggleScheduling}
                />, document.querySelector('body')
            );
        } else {
            return null;
        }
    }

    handleErrorMessage = () => {
        if (this.props.visit_list.length <= 0) {
            return <span className="tour-error">You must have at least one home in your visit list.</span>
        } else if (this.props.visit_list.length > 5) {
            return <span className="tour-error">Sorry, you can't schedule more than 5 homes for a tour.</span>
        } else if (this.state.has_off_market === true) {
            return  <span className="tour-error">There are homes in your visit list that are sold. Remove those to schedule your tour.</span>
        } else if (this.props.last_resend_request_pre_tour !== undefined && !this.props.is_pre_tour_signed && this.props.pre_tour_forms_created && !this.props.itinerary_scheduled) {
            return <span className="tour-error">You can't resend the documents until {moment(this.props.last_resend_request_pre_tour).add({minutes: 16}).format("H:mm A")}</span>
        } else {
            return null;
        }
    }

    handleText = () => {
        if (this.props.loaded) {

            if (!this.props.is_pre_tour_signed && !this.props.pre_tour_forms_created && !this.props.itinerary_scheduled) {
                return (
                    <>
                        <h3>Pre-Tour Documents</h3>
                        <button onClick={this.props.onHandleOnClickCreateDocument}>
                            <i className="material-icons">send</i> {this.props.refreshing_document_status === false ? 'Send My Documents' : 'Sending...'}
                        </button>
                    </>
                );
            } else if (!this.props.is_pre_tour_signed && this.props.pre_tour_forms_created && !this.props.itinerary_scheduled) {
                return (
                    <>
                        <h3>Pre-Tour Documents</h3>
                        <span>
                            <span onClick={this.props.onHandleOnClickRefreshDocument}>
                                <i style={{fontSize: 15}} className="material-icons">refresh</i> {this.props.refreshing_document_status === false ? 'Refresh Status' : 'Loading...'}</span>
                                <span onClick={this.props.onHandleOnClickResendDocument} className="helper-link">
                                    {this.props.refreshing_document_status === false ? '(Resend Email)' : '(Loading...)'}
                                </span>
                        </span>
                    </>
                );
            } else if (this.props.is_pre_tour_signed && this.props.pre_tour_forms_created && !this.props.itinerary_scheduled) {
                let style;
                if (this.determineScheduleButtonStatus()) {
                    style = {
                        opacity: .3
                    }
                } else {
                    style = {
                        opacity: 1
                    }
                }
                return (
                    <>
                        <h3>Tour Summary <span className="helper-text">({this.props.visit_list.length} homes in Visit List)</span></h3>
                        <span onClick={this.toggleScheduling} style={style}>
                            <i style={{fontSize: 15}} className="material-icons">schedule</i> Schedule Tour
                        </span>
                        {this.loadModal()}
                        {this.handleErrorMessage()}
                    </>
                );
            } else if (this.props.itinerary_scheduled) {
                return (
                    <>
                        <h3>Tour Summary <span className="helper-text">({this.props.visit_list.length} homes in Visit List)</span></h3>
                        <a href={scheduler_endpoints['clientScheduler']}>
                            <i style={{fontSize: 15}} className="material-icons">place</i> View Tour
                        </a>
                    </>
                );
            }

        }
    }

    render() {
        return (
            <div className="tour-box tour-cta">
                {this.handleText()}
            </div>
        );
    }
}