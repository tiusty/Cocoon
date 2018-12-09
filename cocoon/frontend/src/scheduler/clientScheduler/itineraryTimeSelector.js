// Import React Components
import React from 'react'
import { Component } from 'react';


import TimeRange from 'react-time-range';
import moment from 'moment';

class ItineraryTimeSelector extends Component {
    state = {
        startTime: moment().startOf('day'),
        endTime: moment().endOf('day').subtract(30, 'minutes'),
    };

    returnFunction = (time) => {
        if (time.endTime) {
            this.setState({
                endTime: moment(time.endTime)
            })
        }
        if (time.startTime) {
            this.setState({
                startTime: moment(time.startTime)
            })
        }
    };

    render() {
        return (
            <div>
                <h2>The Time Selector</h2>
                <TimeRange
                    sameIsValid={false}
                    startMoment={this.state.startTime}
                    endMoment={this.state.endTime}
                    onChange={this.returnFunction}
                />
            </div>
        );
    }

}

export default ItineraryTimeSelector