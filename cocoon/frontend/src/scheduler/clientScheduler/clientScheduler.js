// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios';

import SelectItineraryImg from '../picture.svg';

// Import Cocoon Components
import Itinerary from "../itinerary/itinerary";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import ItineraryTimeSelector from "./itineraryTimeSelector";
import ItineraryDateSelector from './itineraryDateSelector';

class ClientScheduler extends Component {
    state = {
        id: null,
        loaded: false,
        is_claimed: false,
        is_scheduled: false,

        tour_duration_seconds: 0,
        date: new Date(),
        time_available_seconds: 7200,
        totalHours: Math.floor(7200 / 3600),
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
                    this.setState( {loaded: true } )
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

    setTimeAvailable = (e) => {
        this.setState({
            time_available_seconds: this.convertHoursToSeconds(e.target.value)
        })
        this.convertSecondsToHours(this.convertHoursToSeconds(e.target.value));
    }

    convertHoursToSeconds = (hours) => {
        return 3600 * hours;
    }

    convertSecondsToHours = (seconds) => {
        let hours = Math.floor(seconds / 3600);
        this.setState({
            totalHours: hours
        })
    }

    handleAddDate = () => {
        let daysCopy = [...this.state.days];
        let dateCopy = this.state.date;
        let dayAvailable = {};
        dayAvailable.time_available_seconds = parseInt(this.state.time_available_seconds);
        dayAvailable.date = dateCopy;
        if (daysCopy.length < 10) {
            daysCopy.push(dayAvailable);
            this.setState({
                days: daysCopy,
            }, () => this.updateStartTimes(this.state.id));
            this.setState({
                date: new Date()
            }, () => this.render())
        }
    }

    updateStartTimes = (id) => {
        /**
         *  Updates the tenants start_times when adding new dates
         */

        // axios.put(scheduler_endpoints['itinerary'] + id + '/', {
        //     start_times: this.state.days
        // })
        // .catch(error => console.log('Bad', error))
        // .then(response => {
        //      console.log(response)
        // })
    }

    removeStartTime = (id, index, event) => {
        /**
         *  Removes the tenant start_time on click
         *  Expects to be passed the id, index of the start time to be deleted,
         *  and the element to be removed
         *
         *  Make API call to delete
         */
        let daysCopy = [...this.state.days];
        daysCopy.splice(index, 1);
        this.setState({
            days: daysCopy
        })
    }

    cancelItinerary = () => {
        /**
         *  Deletes and cancels the current itinerary
         */
        axios.delete(scheduler_endpoints['itineraryClient'])
            .catch(err => console.log('BAD', err))
            .then(response => {
                console.log(response)
            })
    }

    renderTimeSelector = () => {

        if (this.state.loaded === true) {
            if (this.state.is_scheduled === true) {
                return (
                    <div>
                        <h2>Your Itinerary is currently is already scheduled so you can't modify it</h2>
                    </div>
                )
            } else if (this.state.is_claimed === true) {
                return (
                    <div>
                        <h2>Your Itinerary is currently being scheduled by one of our agents</h2>
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
                            <ItineraryTimeSelector date={this.state.date} tour_duration_seconds={this.state.tour_duration_seconds} totalHours={this.state.totalHours} setTimeAvailable={this.setTimeAvailable} setTime={this.setTime} />
                        </div>
                        <button className="itinerary-button" onClick={this.handleAddDate}>Add date</button>
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
                            removeStartTime={this.removeStartTime}
                            setEstimatedDuration={this.setEstimatedDuration}
                            cancelItinerary={this.cancelItinerary}
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
