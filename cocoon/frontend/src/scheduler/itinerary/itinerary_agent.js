// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'
import moment from 'moment';
import _ from 'lodash';

// Import Cocoon Components
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import HomeTile from "../../common/homeTile/homeTile";
import '../../common/styles/variables.css';
import "./itinerary_agent.css";

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class ItineraryAgent extends Component {
    state = {
        client: null,
        agent: null,
        homes: [],
        selected_start_time: null,
        tour_duration_seconds: null,
        start_times: [],
        refreshing: false,
    };

    updateItinerary() {
        this.setState({
            refreshing: true,
        });
        axios.get(scheduler_endpoints['itinerary'] + this.props.id + '/')
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    agent: response.data.agent,
                    client: response.data.client,
                    homes: response.data.homes,
                    selected_start_time: response.data.selected_start_time,
                    tour_duration_seconds: response.data.tour_duration_seconds_rounded,
                    start_times: response.data.start_times,
                })
                this.setState({
                    refreshing: false,
                });
            })
    }


    componentDidUpdate(prevProps) {
        // If the hash of the itinerary changes then make sure to update the itinerary cus there are changes to the data
        if (prevProps.hash !== this.props.hash) {
            this.updateItinerary()
        }
        if (prevProps.is_pending !== this.props.is_pending) {
            this.updateItinerary();
        }
    }

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        this.updateItinerary();
    }

    selectTime = (iso_time_string) => {
        /**
         * Schedules a claimed itinerary by selecting a start time
         */
        this.setState({'refreshing': true});
        let endpoint = scheduler_endpoints['itineraryAgent'] + this.props.id + '/';
        axios.put(endpoint, {
            type: 'schedule',
            iso_str: iso_time_string,
        })
        .catch(error => {
            this.setState({
                refreshing: false,
            });
            console.log('Bad', error)
        })
        .then(response => {
            if (response.data.result) {
                this.props.refreshItineraries()
            } else {
                alert(response.data.reason);
                this.updateItinerary()
            }
            this.setState({refreshing: false});
        });
    };

    selectTimeButton(iso_time_string) {
        if (!this.state.refreshing) {
            return this.selectTime(iso_time_string)
        } else {
            return null
        }
    }

    formatTimeAvailable = (time) => {
        let hours = Math.floor(time / 3600);
        let minuteDivisor = time % 3600;
        let minutes = Math.ceil((Math.floor(minuteDivisor / 60)) / 15) * 15;
        if (minutes === 0) {
            return `${hours}hrs`;
        } else {
            return `${hours}hrs ${minutes}min`;
        }
    }

    renderClientInfo = () => {
        if (this.state.client === null || this.state.tour_duration_seconds === null) {
            return null;
        }

        return (
            <div className="itinerary-section">
                <div className="itinerary-section-item first-item">
                    Client Information
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Name:</span>
                    <span className="item-right-text">{_.isUndefined(this.state.client.full_name) ? "Loading" : this.state.client.full_name}</span>
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Phone:</span>
                    <span className="item-right-text">{_.isUndefined(this.state.client.phone_number) ? "Loading" : this.state.client.phone_number}</span>
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Email:</span>
                    <span className="item-right-text">{_.isUndefined(this.state.client.email) ? "Loading" : this.state.client.email}</span>
                </div>
                <div className="itinerary-section-item last-item">
                    <span className="item-left-text">Duration:</span>
                    <span className="item-right-text">{_.isUndefined(this.state.tour_duration_seconds) ? "Loading" : this.formatTimeAvailable(this.state.tour_duration_seconds) }</span>
                </div>
            </div>
        );
    }

    renderApartmentInformation = (home, index) => {
        return (
            <div key={index} className="itinerary-section">
                <div className="itinerary-section-item home-item">
                    {home.full_address}
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Listing No.</span>
                    <span className="item-right-text">{home.listing_number}</span>
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Listing Agent</span>
                    <span className="item-right-text">{home.listing_agent}</span>
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Listing Office</span>
                    <span className="item-right-text">{home.listing_office}</span>
                </div>
            </div>
        );
    }

    renderTourHomes = () => {
        return (
            <div className="itinerary-section-wrapper tour-homes-wrapper">
                {this.state.homes.map((home, index) => this.renderApartmentInformation(home, index))}
            </div>
        );
    }

    generateTimeDivs = () => {
        let time_list = []
        for (let i = 0; i < this.state.start_times.length; i++) {
            if (i == this.state.start_times.length - 1) {
                let time = <div key={i} className="itinerary-section-item last-item">
                    <span>{moment(this.state.start_times[i].time).format('MMMM Do')} @ </span>
                <span>{moment(this.state.start_times[i].time).format('h:mm')} - {moment(this.state.start_times[i].time).add(this.state.start_times[i].time_available_seconds, 'seconds').format('h:mm')}</span>
                </div>
                time_list.push(time)
            } else {
                let time = <div key={i} className="itinerary-section-item">
                    <span>{moment(this.state.start_times[i].time).format('MMMM Do')} @ </span>
                <span>{moment(this.state.start_times[i].time).format('h:mm')} - {moment(this.state.start_times[i].time).add(this.state.start_times[i].time_available_seconds, 'seconds').format('h:mm')}</span>
                </div>
                time_list.push(time)
            }
        }
        return time_list;
    }

    getValidStartTimes = () => {
        let valid_start_times = [];
        for (let i=0; i<this.state.start_times.length; i++) {
            let time_available = this.state.start_times[i].time_available_seconds;
            let time = new moment(this.state.start_times[i].time);
            let buffer = parseInt(time_available) - parseInt(this.state.tour_duration_seconds);
            while (buffer >= 0) {
                let unix_moment = moment(time).valueOf();
                if (!valid_start_times.includes(unix_moment)) {
                    valid_start_times.push(unix_moment);
                }
                buffer -= 15 * 60;
                time.add(15, 'minutes');
            }
        }
        return valid_start_times;
    }

    renderSelectTime = (unix_time) => {
             return (<button onClick={() => {this.selectTimeButton(moment(unix_time).toISOString())}} className="select-time-button">
                 {this.state.refreshing ? "..." : "select"}
             </button>);
    }

    renderSchedulingInformation = () => {
        if (this.props.viewType === "itineraryAgentUnscheduled") {
            return (
                <div className="itinerary-section">
                    <div className="itinerary-section-item first-item">Client Openings</div>
                    {this.getValidStartTimes().map((unix_time, index) => {
                        let start_time = moment(unix_time)
                        return (
                            <div key={index} className="itinerary-section-item">
                                <span>{start_time.format('MMMM Do')} @ </span>
                                <span>{start_time.format('h:mm')} - {start_time.add(this.state.tour_duration_seconds, 'seconds').format('h:mm')}</span>
                                <span className="item-right-text">
                                    {this.renderSelectTime(unix_time)}
                                </span>
                            </div>
                        );
                    })}
                </div>
            );

        } else if (this.props.viewType === "itineraryAgentScheduled") {
            return (
                <div className="itinerary-section">
                    <div className="itinerary-section-item first-item">Selected Start Time</div>
                    <div className="itinerary-section-item last-item">
                        <span>{moment(this.state.selected_start_time).format('MMMM Do')} @ </span>
                        <span>{moment(this.state.selected_start_time).format('h:mm')} - {moment(this.state.selected_start_time).add(this.state.tour_duration_seconds, 'seconds').format('h:mm')}</span>
                    </div>
                </div>
            );
        }

        return (
            <div className="itinerary-section">
                <div className="itinerary-section-item first-item">Client Openings</div>
                {this.generateTimeDivs()}
            </div>
        );
    }

    render() {
        return (
            <>
                {this.renderClientInfo()}
                {this.renderTourHomes()}
                {this.renderSchedulingInformation()}
            </>
        );
    }
}

export default ItineraryAgent
