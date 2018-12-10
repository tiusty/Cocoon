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
        id: this.props.id,
        client: null,
        agent: null,
        homes: [],
        selected_start_time: null,
        tour_duration_seconds: null,
        start_times: [],
        showTimes: this.props.showTimes,
        showClaim: this.props.showClaim,
    };

    updateItinerary() {
        axios.get(scheduler_endpoints[this.props.viewType] + this.state.id + '/')
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    agent: response.data.agent,
                    client: response.data.client,
                    homes: response.data.homes,
                    selected_start_time: response.data.selected_start_time,
                    tour_duration_seconds: response.data.tour_duration_seconds,
                    start_times: response.data.start_times,
                })
            })
    }


    componentDidUpdate(prevProps) {
        if (prevProps.hash !== this.props.hash) {
            this.updateItinerary()
        }
    }

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */

        this.updateItinerary()
    }

    selectTime = (id, time) => {
        /**
         * Schedules a claimed itinerary by selecting a start time
         */
        let endpoint = scheduler_endpoints['itineraryAgent'] + this.state.id + '/';
        axios.put(endpoint, {
            type: 'schedule',
            time_id: id,
        })
        .catch(error => console.log('Bad', error))
        .then(response => {
            if (response.data.result) {
                this.props.refreshItineraries()
            } else {
                alert(response.data.reason)
                this.updateItinerary()

            }
        });
    }

    renderStartTimes = () => {
        if (this.state.showTimes) {
            if (this.state.start_times.length === 0) {
                return <p> No start times chosen</p>
            } else {
                return (
                    <div className={"available-times-wrapper"}>
                        {this.state.start_times.map((timeObject) => {
                        return (
                            <div key={timeObject.id}>
                                <div>
                                    {moment(timeObject.time).format('MM/DD/YYYY')} @ {moment(timeObject.time).format('HH:mm')}
                                </div>
                            {this.props.canSelect ? <button
                            onClick={() => this.selectTime(timeObject.id, timeObject.time)}>select</button> : null}
                        </div>
                        );
                    })}
                    </div>
                )
            }
        }

        return null
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
            start_time = <p>
                Start Time:
                {moment(this.state.selected_start_time).format('MM/DD/YYYY')}
                &nbsp; @ &nbsp;
                {moment(this.state.selected_start_time).format('HH:mm')}
                </p>
        }


        return (
            <div>
                {client_div}
                {agent_div}
                <p>Tour Duration = {this.state.tour_duration_seconds}</p>
                {start_time}
                {this.renderStartTimes()}
                {this.renderHomes(this.state.homes)}
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
