// Import React Components
import React from 'react'
import { Component } from 'react';

// Import Cocoon Components
import ItineraryDaySelector from "./itineraryDaySelector";
import moment from 'moment';

export default class ItineraryTimeSelector extends Component {
    state = {
        num_days: 7,
        days: [],
    };

    componentDidMount() {
        let days = [];
        for(let i=0; i<this.state.num_days; i++) {
            let day = {};
            day.index = i;
            day.moment = moment().add(i, 'days');
            day.counter = 0;
            day.time_ranges = [];
            days.push(day)
        }

        this.setState({days})

    }

    handleDeleteTimeRange = (time_range_index, day_index) =>  {
        let days = this.state.days.filter(d => d.index !== day_index);
        let day = this.state.days.filter(d => d.index === day_index);
        day.time_ranges = day.time_ranges.filter(t => t.index !== time_range_index);
        days.push(day);
        this.setState({days})
    };

    handleAddTimeRange = (day_index) => {
        let days = this.state.days.filter(d => d.index !== day_index);

        let day = this.state.days.filter(d => d.index === day_index);
        let time_range = {
            start_time: undefined,
            end_time: undefined,
            index: day.counter,
        };
        day.time_ranges.push(time_range);
        day.counter++;
        days.push(day);

        this.setState({days})
    };

    render() {
        return(
            <>
                {this.state.days.map(t =>
                    <ItineraryDaySelector
                        key={t.index}
                        day={t}
                        onDeleteTimeRange={this.handleDeleteTimeRange}
                        onAddTimeRange={this.handleAddTimeRange}
                    />
                )}
            </>
        );
    }
}
