// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import Itinerary from "../itinerary/itinerary";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class AgentScheduler extends Component {

    state = {
        scheduled_loaded: false,
        unscheduled_loaded: false,
        marketplace_loaded: false,
        unscheduled_itineraries: [],
        scheduled_itineraries: [],
        marketplace_itineraries: [],
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

        return itinerary_ids
    }

    componentDidMount() {
        /**
         *  Retrieves all the agent's unscheduled itineraries
         */

        // retrieve list of claimed, unscheduled itineraries
        axios.get(scheduler_endpoints['itineraryAgent'], {params: {type: 'unscheduled'}})
            .catch(error => console.log('Bad', error))
            .then(response => {
                    this.setState({unscheduled_itineraries: this.parseData(response.data)});
                    this.setState({unscheduled_loaded: true });
            })

        // retrieve list of claimed, scheduled itineraries
        axios.get(scheduler_endpoints['itineraryAgent'], {params: {type: 'scheduled'}})
            .catch(error => console.log('Bad', error))
            .then(response => {
                    this.setState({scheduled_itineraries: this.parseData(response.data)});
                    this.setState({scheduled_loaded: true });
            })

        // retrieve list of unclaimed, marketplace itineraries
        axios.get(scheduler_endpoints['itineraryMarket'])
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({marketplace_itineraries: this.parseData(response.data)});
                this.setState( {marketplace_loaded: true});
            })

    }

    renderItinerary = (itinerary, key, showTimes, showClaim) => {
        return (
            <Itinerary
                id={itinerary.id}
                showTimes={showTimes}
                showClaim={showClaim}
                key={key}
            />
        );
    };

    renderUnscheduledItineraries = () => {
        if (this.state.unscheduled_loaded) {
            return (
                <div className='unscheduled-wrapepr'>
                    {this.state.unscheduled_itineraries.map((itn, i) => this.renderItinerary(itn, i, true, false))}
                </div>
            );
        }
    };

    renderScheduledItineraries = () => {
        if (this.state.scheduled_loaded) {
            return (
                <div className='scheduled-wrapper'>
                    {this.state.scheduled_itineraries.map((itn, i) => this.renderItinerary(itn, i, false, false))}
                </div>
            )
        }
    };

    renderMarketplaceItineraries = () => {
        if (this.state.marketplace_loaded) {
            return (
                <div className='marketplace-wrapper'>
                    {this.state.marketplace_itineraries.map((itn, i) => this.renderItinerary(itn, i, true, true))}
                </div>
            )
        }
    }

    render() {
        return (
            <React.Fragment>
                <div className='row'>
                    <div className="col-md-4">
                        <h2>Claimed Itineraries</h2>
                        {this.renderUnscheduledItineraries()}
                    </div>
                    <div className="col-md-4">
                        <h2>Scheduled Itineraries</h2>
                        {this.renderScheduledItineraries()}
                    </div>
                </div>
                <div className='row'>
                    <div className='col-md-8'>
                        <h2>Available unclaimed itineraries</h2>
                        {this.renderMarketplaceItineraries()}
                    </div>
                </div>
            </React.Fragment>
        );
    }

}

export default AgentScheduler