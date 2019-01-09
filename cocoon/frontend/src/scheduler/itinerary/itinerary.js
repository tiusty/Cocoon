// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'
import moment from 'moment';

// Import Cocoon Components
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import HomeTile from "../../common/homeTile/homeTile";
import "./itinerary.css"

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class Itinerary extends Component {
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
                }, () => { this.props.setEstimatedDuration(response.data.tour_duration_seconds_rounded); this.props.setDefaultTimeAvailable(response.data.tour_duration_seconds);})
            })
    }


    componentDidUpdate(prevProps) {
        // If the hash of the itinerary changes then make sure to update the itinerary cus there are changes to the data
        if (prevProps.hash !== this.props.hash) {
            this.updateItinerary()
        }
    }

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        this.updateItinerary();
    }

    selectTime = (id) => {
        /**
         * Schedules a claimed itinerary by selecting a start time
         */
        this.setState({'refreshing': true});
        let endpoint = scheduler_endpoints['itineraryAgent'] + this.props.id + '/';
        axios.put(endpoint, {
            type: 'schedule',
            time_id: id,
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

    selectTimeButton(timeObject) {
        if (!this.state.refreshing) {
            return this.selectTime(timeObject.id, timeObject.time)
        } else {
            return null
        }
    }

    renderHomes(homes) {
        if (homes.length <= 0) {
            return <p>There are no homes in this visit list</p>
        } else {
            return (this.state.homes.map(home =>
                <HomeTile
                    key={home.id}
                    home={home}
                    show_heart={false}
                    show_visit={false}
                />
            ));
        }
    }

    renderStartTimes = () => {
        if (this.props.days.length === 0) {
            return <div className="side-wrapper-times_empty"><p> No start times chosen</p></div>
        } else {
            return (
                <div className="side-wrapper-times">
                    {this.props.days.map((day, index) => {
                        let endTime = moment(day.date).add(day.time_available_seconds, 'seconds')
                        return (
                            <div className="time-item" key={index}>
                                <div className="time-item_date">
                                    <span>{moment(day.date).format('MMMM Do')} @ </span>
                                    <span>{moment(day.date).format('h:mm A')} - {moment(endTime).format('h:mm A')}</span>
                                </div>
                                <div className="time-item_delete" onClick={(event) => this.props.removeStartTime(this.props.id, index, event)}>
                                    <i className="material-icons">add_circle</i>
                                </div>
                            </div>
                        )
                        })}
                </div>
            );
        }
    }

    renderSavedStartTimes = () => (
        <div className="side-wrapper-times">
            {this.state.start_times.map((day, index) => {
                let endTime = moment(day.date).add(day.time_available_seconds, 'seconds')
                return (
                    <div className="time-item" key={index}>
                        <div className="time-item_date">
                            <span>{moment(day.date).format('MMMM Do')} @ </span>
                            <span>{moment(day.date).format('h:mm A')} - {moment(endTime).format('h:mm A')}</span>
                        </div>
                    </div>
                )
            })}
        </div>
    );

    renderCancelButton = () => {
        if (!this.props.is_canceling) {
            return <p id="cancel-itinerary-btn" onClick={this.props.toggleIsCanceling}>Cancel Itinerary</p>
        } else {
            return (
                <p id="cancel-itinerary-btn_confirm">
                    Are you sure?
                    <span onClick={this.props.confirmCancelItinerary}>Yes</span>
                    or
                    <span onClick={this.props.toggleIsCanceling}>No</span>
                </p>
            );
        }
    }

    renderItinerary = ()=> {
        return (
            <>
                <div className="side-wrapper-top">
                    <p>Your Itinerary</p>
                    <p>Estimated Duration: {this.props.formatTimeAvailable(this.state.tour_duration_seconds)}</p>
                </div>
                {!this.props.is_scheduled ? this.renderStartTimes() : this.renderSavedStartTimes()}
            </>
        );
    }

    render() {
        return (
            <>
                <div className="itinerary-side-wrapper">
                    {this.renderItinerary()}
                </div>
                {this.renderCancelButton()}
            </>
        );
    }
}

export default Itinerary
