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

    render() {
        return(
            <>
                <h4>{this.props.day.moment.format('dddd')}</h4>
                {this.props.day.time_ranges.map(t =>
                    <ItineraryTimeRangeSelector
                        key={t.index}
                        index={t.index}
                        day_index={this.props.day.index}
                        onDelete={this.props.onDeleteTimeRange}
                    />
                )}
                <button className="btn btn-sm" onClick={() => this.props.onAddTimeRange(this.props.day.index)}>Add time</button>
            </>
        );
    }
}
