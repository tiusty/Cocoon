// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import Itinerary from "../itinerary/itinerary";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import ItineraryTimeSelector from "./itineraryTimeSelector";

class ClientScheduler extends Component {
    state = {
        id: null,
        loaded: false,
        is_claimed: false,
        is_scheduled: false,
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
         *  Retrieves all the surveys associated with the user
         */
        axios.get(scheduler_endpoints['itinerary'])
            .catch(error => console.log('Bad', error))
            .then(response => {
                    this.setState(
                        this.parseData(response.data)
                    ),
                    this.setState( {loaded: true } )
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
                return <ItineraryTimeSelector/>

            }
        } else {
            return (
                <div>
                    <p>Loading</p>
                </div>
            );
        }
    };

    renderItinerary = () => {
        if (this.state.loaded === true) {
            if (this.state.id) {
                return (
                    <Itinerary
                        id={this.state.id}
                    />
                );
            } else {
                return (
                    <div>
                        <h2>Please create an itinerary!</h2>
                    </div>

                );
            }
        }
        else {
            return <p>Loading</p>
        }
    };

    render() {
        return (
            <React.Fragment>
                <div className='row'>
                    <div className='col-md-4'>
                        <h2>Your Itinerary</h2>
                        {this.renderItinerary()}
                    </div>
                    <div className='col-md-8'>
                        {this.renderTimeSelector()}
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default ClientScheduler