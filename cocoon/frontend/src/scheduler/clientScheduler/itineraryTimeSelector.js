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

    renderEachDay()  {
        let time_selectors = [];
        for (let i =0; i < this.state.days; i++) {
            time_selectors.push(<ItineraryDaySelector
                dayOfWeek={moment().add(i, 'days').format('dddd')}
            />)
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
