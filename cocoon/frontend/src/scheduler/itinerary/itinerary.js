// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";

class Itinerary extends Component {
    state = {
        agent: null,
        client: null,
        homes: [],
        id: null,
        selected_start_time: null,
        tour_duration_seconds: null,
    };

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        axios.get(scheduler_endpoints['itinerary'])
            .catch(error => console.log('Bad', error))
            .then(response => {
                console.log(response.data),
                this.setState({
                    agent: response.data[0].agent,
                    client: response.data[0].client,
                    homes: response.data[0].homes,
                    id: response.data[0].id,
                    selected_start_time: response.data[0].selected_start_time,
                    tour_duration_seconds: response.data[0].tour_duration_seconds,
                })
            })
    }

    render() {
        return <div><h2>Itinerary</h2></div>
    }
}

export default Itinerary
