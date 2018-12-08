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
        agent: null,
        client: null,
        homes: [],
        id: this.props.id,
        selected_start_time: null,
        tour_duration_seconds: null,
        start_times: [],
        showTimes: this.props.showTimes,
        showClaim: this.props.showClaim,
    };

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */

        axios.get(scheduler_endpoints[this.props.viewType] + this.state.id + '/')
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    agent: response.data.agent,
                    client: response.data.client,
                    homes: response.data.homes,
                    selected_start_time: response.data.selected_start_time,
                    tour_duration_seconds: response.data.tour_duration_seconds,
                    start_times: response.data.start_times
                })
            })

    }

    selectTime = (id, time) => {
        /**
         * Schedules a claimed itinerary by selecting a start time
         */
        let formData = new FormData();
        formData.set('time_id', id);
        formData.set('itinerary_id', this.state.id);

        axios({
            method: 'post',
            url: scheduler_endpoints['selectStartTime'],
            data: formData,
            config: {headers: {'Content-Type': 'multipart/form-data'}}
        })
            .catch(error => console.log('Bad', error))
            .then(response => {
                if (response.data.result == 0) {
                    this.setState({
                        selected_start_time: time,
                        showTimes: false,
                    });
                }
            });
    }

    renderStartTimes = () => {
        if (this.state.showTimes) {
            return (
                this.state.start_times.map((timeObject) => {
                    return (
                        <div key={timeObject.id}>
                            <div>
                                {moment(timeObject.time).format('MM/DD/YYYY')} @ {moment(timeObject.time).format('HH:mm')}
                            </div>
                            {this.props.canSelect ? <button
                                onClick={() => this.selectTime(timeObject.id, timeObject.time)}>select</button> : null}
                        </div>
                    );
                })
            )
        }

        return null
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
                <div className={"available-times-wrapper"}>{this.renderStartTimes()}</div>
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
