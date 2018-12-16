// Import React Components
import React from 'react'
import { Component } from 'react';

// Import Cocoon Components
import ItineraryTimeRangeSelector from "./itineraryTimeRangeSelector";

export default class ItineraryDaySelector extends Component {
    /**
     * Props:
     *  this.props.dayOfWeek
     * @returns {*}
     */

    render() {
        return(
            <>
                <h4>{this.props.dayOfWeek}</h4>
                <ItineraryTimeRangeSelector/>
            </>
        );
    }
}
