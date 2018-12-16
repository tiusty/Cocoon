// Import React Components
import React from 'react'
import { Component } from 'react';

// Import Cocoon Components
import ItineraryDaySelector from "./itineraryDaySelector";

export default class ItineraryTimeSelector extends Component {
    state = {
        days: 6,
    };

    renderEachDay()  {
        let time_selectors = [];
        for (let i =0; i < this.state.days; i++) {
            time_selectors.push(<ItineraryDaySelector/>)
        }
        return time_selectors
    }

    render() {
        return(
            <>
                    {this.renderEachDay().map(d =>
                        <div className="row">
                            {d}
                        </div>
                    )}
            </>
        );
    }
}
