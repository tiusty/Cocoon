// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios';

import SelectItineraryImg from '../picture.svg';
import SavedItineraryImg from '../newspaper.svg';
import ClaimedItineraryImg from '../pin.svg';

// Import Cocoon Components
import Itinerary from "../itinerary/itinerary";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import userAuth_endpoints from "../../endpoints/userAuth_endpoints";
import ItineraryTimeSelector from "./itineraryTimeSelector";
import ItineraryDateSelector from './itineraryDateSelector';

class ClientScheduler extends Component {
    state = {
        id: null,
        loaded: false,
        is_claimed: false,
        is_scheduled: false,

        is_canceling: false,
        tour_duration_seconds: 0,
        date: new Date(),
        time_available_seconds: 0,
        days: []
    };

    parseData(data) {
        /**
         * Parses data returned from the endpoint and returns it in a nicer format for react
         *
         * Expects to be passed data a list of surveys from the backend and then returns a list
         *  of the survey ids.
         * @type {Array}: A list of surveys
         */
        let itinerary_ids = [];

        // For each survey just push the id for that itinerary to the list
        // Note there should only be one
        data.map(c =>
            itinerary_ids.push( { id: c.id,
                is_claimed: c.is_claimed,
                is_scheduled: c.is_scheduled} )
        );

        return itinerary_ids[0]
    }

    componentDidMount() {
        /**
         *  Retrieves all the itineraries associated with the user
         */
        axios.get(scheduler_endpoints['itineraryClient'])
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState(
                    this.parseData(response.data)
                ),
                this.setState( { loaded: true } );
                if (response.data[0].start_times) {
                    this.setState( { is_scheduled: true } )
                }
            })
    }

    setEstimatedDuration = (time) => {
        this.setState({
            tour_duration_seconds: time
        })
    }

    setDate = (date) => {
        let dateCopy = this.state.date;
        dateCopy.setDate(date.getDate());
        this.setState({
            date: dateCopy
        }, () => this.state.date)
    }

    setTime = (hour, minute, period) => {
        let dateCopy = this.state.date;
        let hours = period === 'AM' ? hour : hour + 12;
        dateCopy.setHours(hours);
        dateCopy.setMinutes(minute);
        this.setState({
            date: dateCopy
        })
    }

    setDefaultTimeAvailable = (time) => {
        let hours = Math.floor(time / 3600);
        let minuteDivisor = time % 3600;
        let minutes = Math.ceil((Math.floor(minuteDivisor / 60)) / 15) * 15;
        let minTime = parseFloat(hours + (minutes / 60));
        this.setState({
            time_available_seconds: this.convertHoursToSeconds(minTime)
        })
    }

    setTimeAvailable = (e) => {
        this.setState({
            time_available_seconds: this.convertHoursToSeconds(e.target.value)
        })
    }

    convertHoursToSeconds = (hours) => {
        return 3600 * hours;
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

    handleAddDate = () => {
        let daysCopy = [...this.state.days];
        let dateCopy = this.state.date;
        let dayAvailable = {};
        let time_id = daysCopy.length;
        dayAvailable.time_available_seconds = parseInt(this.state.time_available_seconds);
        dayAvailable.date = dateCopy;
        dayAvailable.time_id = time_id;
        if (daysCopy.length < 10) {
            daysCopy.push(dayAvailable);
            this.setState({
                days: daysCopy,
            });
            this.setState({
                date: new Date()
            });
        }
    }

    updateStartTimes = () => {
        /**
         *  Updates the tenants start_times when adding new dates
         */
        if (this.state.days.length) {
            let endpoint = scheduler_endpoints['itineraryClient'] + this.state.id + '/';
            axios.put(endpoint, {
                start_times: this.state.days,
                type: 'start_times',
                // set is_scheduled to true
            })
            .catch(error => console.log('Bad', error))
            .then(response => {
                 if (response.data.result) {
                     this.setState({
                         is_scheduled: true
                     })
                 } else {
                     // Some error happens
                 }
            })
        }
    }

    removeStartTime = (id, index, event) => {
        /**
         *  Removes the tenant start_time on click
         *  Expects to be passed the id, index of the start time to be deleted,
         *  and the element to be removed
         * */
        let daysCopy = [...this.state.days];
        daysCopy.splice(index, 1);
        this.setState({
            days: daysCopy
        })
    }

    toggleIsCanceling = () => {
        this.setState({
            is_canceling: !this.state.is_canceling
        })
    }

    confirmCancelItinerary = () => {
        /**
         *  Deletes and cancels the current itinerary
         */
        let endpoint = scheduler_endpoints['itineraryClient'] + this.state.id + '/';
        axios.delete(endpoint)
            .catch(err => console.log('BAD', err))
            .then(response => {
                console.log(response);
                this.setState({
                    id: null,
                    loaded: true,
                    is_claimed: false,
                    is_scheduled: false
                })
            })
    }

    renderTimeSelector = () => {

        if (this.state.loaded === true) {
            if (this.state.is_scheduled === true && !this.state.is_claimed) {
                return (
                    <div className="onboard-wrapper onboard-wrapper_small">
                        <img src={SavedItineraryImg} alt=""/>
                        <h2>Congrats! Your itinerary is saved.</h2>
                        <p>Your Itinerary is currently being scheduled so you can't modify it.</p>
                    </div>
                )
            } else if (this.state.is_claimed === true) {
                return (
                    <div className="onboard-wrapper onboard-wrapper_small">
                        <img src={ClaimedItineraryImg} alt=""/>
                        <h2>Our agents are checking out your Itinerary.</h2>
                        <p>Your Itinerary is currently being scheduled by one of our agents. Please wait to hear back from us.</p>
                    </div>
                )
            } else {
                return (
                    <div className="itinerary-main-wrapper">
                        <div className="itinerary-headline">
                            <h2>Please create an itinerary!</h2>
                            <p>Add up to 10 dates and times that you're available for a tour</p>
                        </div>
                        <div className="itinerary-date-time-wrapper">
                            <ItineraryDateSelector date={this.state.date} setDate={this.setDate} />
                            <ItineraryTimeSelector date={this.state.date} formatTimeAvailable={this.formatTimeAvailable} tour_duration_seconds={this.state.tour_duration_seconds} setTimeAvailable={this.setTimeAvailable} setTime={this.setTime} />
                        </div>
                        <button className="itinerary-button" onClick={this.handleAddDate}>Add date</button>
                        <button className="itinerary-button" onClick={this.updateStartTimes}>Save Itinerary</button>
                    </div>
                )

            }
        } else {
            return (
                <div>
                    <p>Loading</p>
                </div>
            );
        }
    };

    clientSchedulerStatus() {
        if (this.state.loaded) {
            if (this.state.id) {
                return (
                <div className="row">
                    <div className="col-md-8">
                        {this.renderTimeSelector()}
                    </div>
                    <div className="col-md-4">
                        <Itinerary
                            id={this.state.id}
                            days={this.state.days}
                            is_scheduled={this.state.is_scheduled}
                            formatTimeAvailable={this.formatTimeAvailable}
                            removeStartTime={this.removeStartTime}
                            setEstimatedDuration={this.setEstimatedDuration}
                            is_canceling={this.state.is_canceling}
                            toggleIsCanceling={this.toggleIsCanceling}
                            confirmCancelItinerary={this.confirmCancelItinerary}
                            setDefaultTimeAvailable={this.setDefaultTimeAvailable}
                        />
                    </div>
                </div>
                );
            } else {
                return (
                    <div className="onboard-wrapper">
                        <img src={SelectItineraryImg} alt=""/>
                        <h2>Please create an itinerary!</h2>
                        <p>Select the places you'd like to visit.</p>
                        <a href={window.location.origin + userAuth_endpoints['surveys']}>Go to Surveys</a>
                    </div>
                );
            }
        } else {
            return <p>Loading</p>
        }
    }

    render() {
        return (
            <>
                {this.clientSchedulerStatus()}
            </>
        );
    }
}

export default ClientScheduler
