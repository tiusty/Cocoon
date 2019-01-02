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
        marketplace_itineraries: [],
        refreshing: false,
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

        // retrieve list of unclaimed, marketplace itineraries
        axios.get(scheduler_endpoints['itineraryMarket'])
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({marketplace_itineraries: this.parseData(response.data)});
                this.setState({marketplace_loaded: true});
            })
    };

    claimItinerary = (id) => {
        this.setState({refreshing: true});
        let endpoint = scheduler_endpoints['itineraryAgent'] + id + '/';
        axios.put(endpoint, {
            type: 'claim',
        })
        .catch(error => {
            this.setState({
                refreshing: false,
            });
            console.log('Bad', error)
        })
        .then(response => {
            if (response.data.result) {
                this.refreshItineraries()
            } else {
                alert(response.data.reason);
                this.refreshItineraries()
            }
            this.setState({refreshing: false});
        });
    };

    claimButtonAction(id) {
        /*
        This function prevents spamming of backend by disabling button once the user clicks it
         */
        if (!this.state.refreshing) {
            return this.claimItinerary(id)
        } else {
            return null
        }
    }

    renderItinerary = (itinerary, key, showTimes, canSelect, viewType) => {
        return (
            <div key={key} className="single-itinerary">
                <Itinerary
                    id={itinerary.id}
                    key={"itinerary" + key}
                    hash={itinerary.hash}
                    showTimes={showTimes}
                    canSelect={canSelect}
                    viewType={viewType}
                />
                <button key={"claim" + key} onClick={() => this.claimButtonAction(itinerary.id)}>
                    {this.state.refreshing ? 'Loading' : 'claim'}
                </button>
            </div>
        );
    };

    renderMarketplaceItineraries = () => {
        if (this.state.marketplace_loaded) {
            if (this.state.marketplace_itineraries.length <= 0) {
                return <div> There is no open itineraries </div>
            } else {
                return (
                    <div className='marketplace-wrapper'>
                        {this.state.marketplace_itineraries.map((itn, i) => this.renderItinerary(itn, i, true, false, "itineraryMarket"))}
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
                    <div className='row'>
                        <div className='col-md-4'>
                            <h2>Available unclaimed itineraries</h2>
                            {this.renderMarketplaceItineraries()}
                        </div>
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default AgentSchedulerPortal