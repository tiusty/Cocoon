// Import React Components
import React from 'react'
import { Component } from 'react';

// Import Cocoon Components
import ItineraryTimeRangeSelector from "./itineraryTimeRangeSelector";
import moment from 'moment';

export default class ItineraryDaySelector extends Component {
    /**
     * Props:
     *  this.props.dayOfWeek (moment) -> The day of the week that this
     *      date corresponds to
     * @returns {*}
     */
    state = {
      num_time_ranges: 0,
    };

    addTimeRangeSelector = () => {
        this.setState({
            num_time_ranges: this.state.num_time_ranges+1
        })
    };

    render() {
        let selectors = [];
        for (let i=0; i<this.state.num_time_ranges; i++) {
            selectors.push(
                <ItineraryTimeRangeSelector
                    key={i}
                />
            )
        }

        return(
            <>
                <h4>{this.props.dayOfWeek.format('dddd')}</h4>
                {selectors}
                <button className="btn btn-sm" onClick={this.addTimeRangeSelector}>Add time</button>
            </>
        );
    }
}
