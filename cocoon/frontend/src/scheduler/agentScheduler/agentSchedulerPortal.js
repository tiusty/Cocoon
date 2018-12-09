// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'

// Import Cocoon Components
import Itinerary from "../itinerary/itinerary";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";

import "./agentScheduler.css"

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class AgentSchedulerPortal extends Component {

    state = {
        scheduled_loaded: false,
        unscheduled_loaded: false,
        marketplace_loaded: false,
        unscheduled_itineraries: [],
        scheduled_itineraries: [],
    };

    parseData(data) {
        /**
         * Parses data returned from the endpoint and returns it in a nicer format for react
         *
         * Expects to be passed data a list of itineraries from the backend and then returns a list
         *  of the of each itinerary with appropriate information.
         * @type {Array}: A list of surveys
         */
        let itinerary_ids = [];

        // For each itinerary just push the id for that itinerary to the list
        data.map(c =>
            itinerary_ids.push({
                id: c.id,
                is_claimed: c.is_claimed,
                is_scheduled: c.is_scheduled,
                hash: c.hash,
            })
        );

        return itinerary_ids
    }

    componentDidMount() {
        /**
         *  Retrieves all the agent's unscheduled itineraries
         */

        this.refreshItineraries()
    }

    refreshItineraries = () => {

        // retrieve list of claimed, unscheduled itineraries
        axios.get(scheduler_endpoints['itineraryAgent'], {params: {type: 'unscheduled'}})
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({unscheduled_itineraries: this.parseData(response.data)});
                this.setState({unscheduled_loaded: true});
            })

        // retrieve list of claimed, scheduled itineraries
        axios.get(scheduler_endpoints['itineraryAgent'], {params: {type: 'scheduled'}})
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({scheduled_itineraries: this.parseData(response.data)});
                this.setState({scheduled_loaded: true});
            })

    }

    claimItinerary = (id) => {
        let formData = new FormData();
        formData.set('itinerary_id', id);

        axios({
            method: 'post',
            url: scheduler_endpoints['claimItinerary'],
            data: formData,
            config: {headers: {'Content-Type': 'multipart/form-data'}}
        })
            .catch(error => console.log('Bad', error))
            .then(response => {
                if (response.data.result === "0") {
                    this.setState({
                        showClaim: false,
                    });
                    this.refreshItineraries()

                } else if (response.data.result === "1") {
                    alert("This itinerary has been claimed")
                    this.refreshItineraries()
                } else {
                    alert(response.data.result)
                    this.refreshItineraries()
                }
            });
    };

    renderItinerary = (itinerary, key, showTimes, canClaim, canSelect, viewType) => {
        let claimButton = canClaim ?
            <button key={"claim" + key} onClick={() => this.claimItinerary(itinerary.id)}>claim</button> : null
        return (
            <div key={key} className='single-itinerary'>
                <Itinerary
                    id={itinerary.id}
                    key={"itinerary" + key}
                    hash={itinerary.hash}
                    showTimes={showTimes}
                    canSelect={canSelect}
                    brokerRequest
                    viewType={viewType}
                />
                {claimButton}
            </div>
        );
    };

    renderUnscheduledItineraries = () => {
        if (this.state.unscheduled_loaded) {

            if (this.state.unscheduled_itineraries.length <= 0) {
                return <p> There is no unscheduled itineraries </p>
            } else {
                return (
                    <div className='unscheduled-wrapper'>
                        {this.state.unscheduled_itineraries.map((itn, i) => this.renderItinerary(itn, i, true, false, true, "itineraryAgent"))}
                    </div>
                );
            }
        }
    };

    renderScheduledItineraries = () => {
        if (this.state.scheduled_loaded) {
            if (this.state.scheduled_itineraries.length <= 0) {
                return <div> There is no scheduled itineraries </div>
            } else {
                return (
                    <div className='scheduled-wrapper'>
                        {this.state.scheduled_itineraries.map((itn, i) => this.renderItinerary(itn, i, false, false, false, "itineraryAgent"))}
                    </div>
                )
            }
        }
    };

    render() {
        return (
            <React.Fragment>
                <div className="agent-scheduler-wrapper">
                    <button onClick={this.refreshItineraries}>Refresh itineraries</button>
                    <div className='itinerary-wrapper row'>
                        <div className="col-md-4">
                            <h2>Unscheduled Itineraries</h2>
                            {this.renderUnscheduledItineraries()}
                        </div>
                        <div className="col-md-4">
                            <h2>Scheduled Itineraries</h2>
                            {this.renderScheduledItineraries()}
                        </div>
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default AgentSchedulerPortal