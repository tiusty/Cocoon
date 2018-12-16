// Import React Components
import React from 'react'
import { Component } from 'react';

// Import Cocoon Components
import ItineraryDaySelector from "./itineraryDaySelector";
import moment from 'moment';

export default class ItineraryTimeSelector extends Component {
    state = {
        days: 7,
    };

    render() {
        let time_selectors = [];
        for (let i = 0; i < this.state.days; i++) {
            time_selectors.push(
                    <ItineraryDaySelector
                        key={i}
                        dayOfWeek={moment().add(i, 'days')}
                    />
            )
        }
        return(
            <>
                {time_selectors}
            </>
        );
    }
}
