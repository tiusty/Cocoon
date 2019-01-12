// Import React Components
import React from 'react'
import { Component } from 'react';

// Import Cocoon Components
import Calendar from 'react-calendar';

export default class ItineraryDateSelector extends Component {

    constructor(props) {
        super(props);
        this.state = {
            date: this.props.date
        }
    }

    getMaxDate = () => {
        let date = new Date();
        date.setDate(date.getDate() + 10);
        return date;
    }

    handleDate = (date) => {
        this.setState({ date }, () => this.props.setDate(this.state.date));
    }

    render() {
        return (
            <div className="calendar-wrapper">
                <h3>Select a Date</h3>
                <p>Pick a date for your tour</p>
                <Calendar
                    minDetail="month"
                    maxDetail="month"
                    minDate={new Date()}
                    maxDate={this.getMaxDate()}
                    value={this.props.date}
                    onChange={this.handleDate}
                />
            </div>
        );
    }
}