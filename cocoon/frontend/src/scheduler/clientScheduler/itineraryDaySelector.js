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
        time_range_counter: 0,
        time_ranges: [],

    };

    handleDeleteTimeRangeSelector = (id) => {
        let update_time_ranges = this.state.time_ranges.filter(t => t.id !== id)
        this.setState({time_ranges: update_time_ranges})
    };

    addTimeRangeSelector = () => {
        /**
         * Adds another time range selector to the current day
         * @type {{id: number}}
         */
        let new_time_range = {
            id: this.state.time_range_counter
        };

        this.setState({
            time_range_counter: this.state.time_range_counter+1,
            time_ranges: [...this.state.time_ranges, new_time_range],
        })
    };

    render() {
        return(
            <>
                <h4>{this.props.dayOfWeek.format('dddd')}</h4>
                {this.state.time_ranges.map(t =>
                    <ItineraryTimeRangeSelector
                        key={t.id}
                        id={t.id}
                        onDelete={this.handleDeleteTimeRangeSelector}
                    />
                )}
                <button className="btn btn-sm" onClick={this.addTimeRangeSelector}>Add time</button>
            </>
        );
    }
}
