// Import React Components
import React from 'react'
import { Component } from 'react';

import TimeRange from 'react-time-range';
import moment from 'moment';

class ItineraryTimeRangeSelector extends Component {
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
            <div className="row">
                <div className="col-md-6">
                    <TimeRange
                        sameIsValid={false}
                        startMoment={this.state.startTime}
                        endMoment={this.state.endTime}
                        onChange={this.returnFunction}
                    />
                </div>
                <div className="col-md-4">
                    <button className="btn btn-sm" onClick={() => this.props.onDelete(this.props.id)}>-</button>
                </div>
            </div>
        );
    }

}

export default ItineraryTimeRangeSelector