// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import HomeTile from "../../common/homeTile/homeTile";

class Itinerary extends Component {
    state = {
        agent: null,
        client: null,
        homes: [],
        id: this.props.id,
        selected_start_time: null,
        tour_duration_seconds: null,
    };

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        axios.get(scheduler_endpoints['itinerary'] + this.state.id + '/')
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    agent: response.data.agent,
                    client: response.data.client,
                    homes: response.data.homes,
                    selected_start_time: response.data.selected_start_time,
                    tour_duration_seconds: response.data.tour_duration_seconds,
                })
            })
    }

    renderItinerary = () => {
        let client_div = <div>Not rendered</div>;
        if (this.state.client) {
            client_div = <p>Itinerary: {this.state.client.email}</p>
        }

        let agent_div = <p>Agent: Not assigned</p>;
        if (this.state.agent) {
            agent_div = <p>Agent: {this.state.agent.email}</p>
        }

        let start_time = <p>Start Time: Not Selected</p>;
        if (this.state.selected_start_time) {
            start_time = <p>Start Time: {this.state.selected_start_time}</p>
        }


        return (
            <div>
                {client_div}
                {agent_div}
                <p>Tour Duration = {this.state.tour_duration_seconds}</p>
                {start_time}
                {this.state.homes.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        show_heart={false}
                        show_visit={false}
                    />
                )}
            </div>
        );
    };

    render() {
        return (
            <div>
                {this.renderItinerary()}
            </div>
        );
    }
}

export default Itinerary
