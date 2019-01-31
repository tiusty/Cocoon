// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'
import moment from 'moment';

// Import Cocoon Components
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import HomeTile from "../../common/homeTile/homeTile";
import '../../common/styles/variables.css';
import "./itinerary_agent.css";

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class ItineraryAgent extends Component {
    state = {
        client: null,
        agent: null,
        homes: [],
        selected_start_time: null,
        tour_duration_seconds: null,
        start_times: [],
        refreshing: false,
    };

    updateItinerary() {
        axios.get(scheduler_endpoints['itinerary'] + this.props.id + '/')
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    agent: response.data.agent,
                    client: response.data.client,
                    homes: response.data.homes,
                    selected_start_time: response.data.selected_start_time,
                    tour_duration_seconds: response.data.tour_duration_seconds_rounded,
                    start_times: response.data.start_times,
                })
            })
    }


    componentDidUpdate(prevProps) {
        // If the hash of the itinerary changes then make sure to update the itinerary cus there are changes to the data
        if (prevProps.hash !== this.props.hash) {
            this.updateItinerary()
        }
        if (prevProps.is_pending !== this.props.is_pending) {
            this.updateItinerary();
        }
    }

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        this.updateItinerary();
    }

    selectTime = (iso_time_string) => {
        /**
         * Schedules a claimed itinerary by selecting a start time
         */
        this.setState({'refreshing': true});
        let endpoint = scheduler_endpoints['itineraryAgent'] + this.props.id + '/';
        axios.put(endpoint, {
            type: 'schedule',
            iso_str: iso_time_string,
        })
        .catch(error => {
            this.setState({
                refreshing: false,
            });
            console.log('Bad', error)
        })
        .then(response => {
            if (response.data.result) {
                this.props.refreshItineraries()
            } else {
                alert(response.data.reason);
                this.updateItinerary()
            }
            this.setState({refreshing: false});
        });
    };

    selectTimeButton(iso_time_string) {
        if (!this.state.refreshing) {
            return this.selectTime(iso_time_string)
        } else {
            return null
        }
    }

    // renderStartTimes = () => {
    //     if (this.props.days.length === 0) {
    //         return <div className="side-wrapper-times_empty"><p> No start times chosen</p></div>
    //     } else {
    //         return (
    //             <div className="side-wrapper-times">
    //                 {this.props.days.map((day, index) => {
    //                     let endTime = moment(day.date).add(day.time_available_seconds, 'seconds')
    //                     return (
    //                         <div className="time-item" key={index}>
    //                             <div className="time-item_date">
    //                                 <span>{moment(day.date).format('MMMM Do')} @ </span>
    //                                 <span>{moment(day.date).format('h:mm A')} - {moment(endTime).format('h:mm A')}</span>
    //                             </div>
    //                             <div className="time-item_delete" onClick={(event) => this.props.removeStartTime(this.props.id, index, event)}>
    //                                 <i className="material-icons">add_circle</i>
    //                             </div>
    //                         </div>
    //                     )
    //                     })}
    //             </div>
    //         );
    //     }
    // };

    // renderSavedStartTimes = () => (
    //     <div className="side-wrapper-times">
    //         {this.state.start_times.map((day, index) => {
    //             let endTime = moment(day.time).add(day.time_available_seconds, 'seconds')
    //             return (
    //                 <div className="time-item" key={index}>
    //                     <div className="time-item_date">
    //                         <span>{moment(day.time).format('MMMM Do')} @ </span>
    //                         <span>{moment(day.time).format('h:mm A')} - {moment(endTime).format('h:mm A')}</span>
    //                     </div>
    //                 </div>
    //             )
    //         })}
    //     </div>
    // );

    // renderCancelButton = () => {
    //     if (!this.props.is_canceling) {
    //         return <p id="cancel-itinerary-btn" onClick={this.props.toggleIsCanceling}>Cancel Itinerary</p>
    //     } else {
    //         return (
    //             <p id="cancel-itinerary-btn_confirm">
    //                 Are you sure?
    //                 <span onClick={this.props.confirmCancelItinerary}>Yes</span>
    //                 or
    //                 <span onClick={this.props.toggleIsCanceling}>No</span>
    //             </p>
    //         );
    //     }
    // };

    // renderItinerary = ()=> {
    //     return (
    //         <>
    //             <div className="side-wrapper-top">
    //                 <p>Your Itinerary</p>
    //                 <p>Estimated Duration: {this.props.formatTimeAvailable(this.state.tour_duration_seconds)}</p>
    //             </div>
    //             {this.props.is_pending ? this.renderStartTimes() : this.renderSavedStartTimes()}
    //         </>
    //     );
    // };

    // render() {
    //     return (
    //         <>
    //             <div className="itinerary-side-wrapper">
    //                 {this.renderItinerary()}
    //             </div>
    //             {this.renderCancelButton()}
    //         </>
    //     );
    // }

    renderClientInfo = () => {
        return (
            <div className="itinerary-section">
                <div className="itinerary-section-item first-item">
                    Client Information
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Name:</span>
                    <span className="item-right-text">Sean Rayment</span>
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Email:</span>
                    <span className="item-right-text">sar5498@gmail.com</span>
                </div>
                <div className="itinerary-section-item last-item">
                    <span className="item-left-text">Duration:</span>
                    <span className="item-right-text">3 hr. 15 min.</span>
                </div>
            </div>
        );
    }

    renderApartmentInformation = (home, index) => {
        return (
            <div key={index} className="itinerary-section">
                <div className="itinerary-section-item home-item">
                    {home.full_address}
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Listing No.</span>
                    <span className="item-right-text">{home.listing_number}</span>
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Listing Agent</span>
                    <span className="item-right-text">{home.listing_agent}</span>
                </div>
                <div className="itinerary-section-item">
                    <span className="item-left-text">Listing Office</span>
                    <span className="item-right-text">{home.listing_office}</span>
                </div>
            </div>
        );
    }

    renderTourHomes = () => {
        return (
            <div className="itinerary-section-wrapper tour-homes-wrapper">
                {this.state.homes.map((home, index) => this.renderApartmentInformation(home, index))}
            </div>
        );
    }

    renderSavedStartTimes = () => (
        <div className="side-wrapper-times">
            {this.state.start_times.map((day, index) => {
                let endTime = moment(day.time).add(day.time_available_seconds, 'seconds')
                return (
                    <div className="time-item" key={index}>
                        <div className="time-item_date">
                            <span>{moment(day.time).format('MMMM Do')} @ </span>
                            <span>{moment(day.time).format('h:mm A')} - {moment(endTime).format('h:mm A')}</span>
                        </div>
                    </div>
                )
            })}
        </div>
    );

    formatTimeAvailable = (time) => {
        let hours = Math.floor(time / 3600);
        let minuteDivisor = time % 3600;
        let minutes = Math.ceil((Math.floor(minuteDivisor / 60)) / 15) * 15;
        if (minutes === 0) {
            return `${hours}hrs`;
        } else {
            return `${hours}hrs ${minutes}min`;
        }
    }

    generateTimeDivs = () => {
        let time_list = []
        for (let i = 0; i < this.state.start_times.length; i++) {
            if (i == this.state.start_times.length - 1) {
                let time = <div key={i} className="itinerary-section-item last-item">{this.state.start_times[i].time}</div>
                time_list.push(time)
            } else {
                let time = <div key={i} className="itinerary-section-item">{this.state.start_times[i].time}</div>
                time_list.push(time)
            }
        }
        return time_list;
    }

    getValidStartTimes = () => {
        let valid_start_times = [];
        for (let i=0; i<this.state.start_times.length; i++) {
            let time_available = this.state.start_times[i].time_available_seconds;
            let time = new moment(this.state.start_times[i].time);
            console.log(time)
            let buffer = parseInt(time_available) - parseInt(this.state.tour_duration_seconds);
            while (buffer >= 0) {
                let unix_moment = moment(time).valueOf();
                console.log(moment(unix_moment))
                if (!valid_start_times.includes(unix_moment)) {
                    valid_start_times.push(unix_moment);
                }
                buffer -= 15 * 60;
                time.add(15, 'minutes');
            }
        }
        return valid_start_times;
    }

    renderSchedulingInformation = () => {
        if (this.props.showTimes) {
            return (
                <div className="itinerary-section">
                    <div className="itinerary-section-item first-item">Available Start Times</div>
                    {this.getValidStartTimes().map((unix_time, index) => {
                        let start_time = moment(unix_time)
                        return (
                            <div key={index} className="itinerary-section-item">
                                <span>{start_time.format('MMMM Do')} @ </span>
                                <span>{start_time.format('h:mm')} - {start_time.add(this.state.tour_duration_seconds, 'seconds').format('h:mm')}</span>
                                <span className="item-right-text">
                                    <button onClick={() => {this.selectTimeButton(moment(unix_time).toISOString())}} className="select-time-button">select</button>
                                </span>
                            </div>
                        );
                    })}
                </div>
            );

        }

        return (
            <div className="itinerary-section">
                <div className="itinerary-section-item first-item">Available Start Times</div>
                {this.generateTimeDivs()}
            </div>
        );


        // return (
        //     <div className="itinerary-section">
        //         <div className="itinerary-section-item first-item">
        //             Schedule Tour
        //         </div>
        //         <div className="itinerary-section-item">
        //             <span className="item-left-text">Jan 1. 4:15 - 7pm</span>
        //             <span className="item-right-text">
        //                 <button className="schedule-button">schedule</button>
        //             </span>
        //         </div>
        //     </div>
        // );
    }

    render() {
        return (
            <>
                {this.renderClientInfo()}
                {this.renderTourHomes()}
                {this.renderSchedulingInformation()}
            </>
        );
    }
}

export default ItineraryAgent
