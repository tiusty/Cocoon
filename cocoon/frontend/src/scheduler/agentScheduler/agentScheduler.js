// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import Itinerary from "../itinerary/itinerary";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
// import ItineraryTimeSelector from "./itineraryTimeSelector";

class AgentScheduler extends Component {
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
        axios.get(scheduler_endpoints['itinerary'],
            {
                type: 'unscheduled'
            })
            .catch(error => console.log('Bad', error))
            .then(response => {
                    this.setState(
                        {unscheduled_itineraries: this.parseData(response)}
                    ),
                    this.setState( {unscheduled_loaded: true } )
            })

        axios.get(scheduler_endpoints['itinerary'],
            {
                type: 'scheduled'
            })
            .catch(error => console.log('Bad', error))
            .then(response => {
                    this.setState(
                        {scheduled_itineraries: this.parseData(response)}
                    ),
                    this.setState( {scheduled_loaded: true } )
            })
    }

    // renderTimeSelector = () => {
    //
    //     if (this.state.loaded === true) {
    //         if (this.state.is_scheduled === true) {
    //             return (
    //                 <div>
    //                     <h2>Your Itinerary is currently is already scheduled so you can't modify it</h2>
    //                 </div>
    //             )
    //         } else if (this.state.is_claimed === true) {
    //             return (
    //                 <div>
    //                     <h2>Your Itinerary is currently being scheduled by one of our agents</h2>
    //                 </div>
    //             )
    //         } else {
    //             return <ItineraryTimeSelector/>
    //
    //         }
    //     } else {
    //         return (
    //             <div>
    //                 <p>Loading</p>
    //             </div>
    //         );
    //     }
    // };

    renderItinerary = (itinerary) => {
        return (
            <Itinerary
                id={this.state.id}
            />
        );
    };

    renderUnscheduledItineraries = () => {
        if (this.state.unscheduled_loaded) {
            return (
                <div className='unscheduled-wrapepr'>
                    {this.state.unscheduled_itineraries.map((itn) => this.renderItinerary(itn))}
                </div>
            );
        }
    };

    renderScheduledItineraries = () => {
        if (this.state.scheduled_itineraries) {
            return (
                <div className='scheduled-wrapper'>
                    {this.state.scheduled_itineraries.map((itn) => this.renderItinerary(itn))}
                </div>
            )
        }
    };


    render() {
        return (
            <React.Fragment>
                <div className='row'>
                    <h2>Claimed Itineraries</h2>
                    {this.renderUnscheduledItineraries()}
                </div>

                <div className='row'>
                    <h2>Scheduled Itineraries</h2>
                    {this.renderScheduledItineraries()}
                </div>
            </React.Fragment>
        );
    }
}

export default AgentScheduler