// Import React Components
import React from 'react'
import { Component } from 'react';

export default class ItineraryTimeSelector extends Component {

    constructor(props) {
        super(props);
        this.state = {
            time: this.props.date,
            hour: undefined,
            minute: undefined,
            period: undefined
        }
    }

    componentDidMount = () => {
        this.setInitialTime(this.state.time);
    }

    setInitialTime = (time) => {
        this.setState({
            hour: ((time.getHours() + 11) % 12 + 1),
            minute: (Math.ceil(time.getMinutes() / 15) * 15) === 60 ? 45 : Math.ceil(time.getMinutes() / 15) * 15,
            period: time.getHours() >= 12 ? 'PM' : 'AM'
        });
    }

    handleHour = (hour, direction) => {
        if (direction === 'up' && hour < 12) {
            hour++;
        } else if (direction === 'up' && hour === 12) {
            hour = 1;
        }
        if (direction === 'down' && hour > 1) {
            hour--;
        } else if (direction === 'down' && hour === 1) {
            hour = 12;
        }
        this.setState({
            hour: hour
        }, () => this.props.setTime(this.state.hour, this.state.minute, this.state.period))
    }

    handleMinute = (minute, direction) => {
        if (direction === 'up' && minute < 45) {
            minute += 15;
        } else if (direction === 'up' && minute === 45) {
            minute = 0;
        }
        if (direction === 'down' && minute > 1) {
            minute -= 15;
        } else if (direction === 'down' && minute < 1) {
            minute = 45;
        }
        this.setState({
            minute: minute
        }, () => this.props.setTime(this.state.hour, this.state.minute, this.state.period))
    }

    handlePeriod = (period) => {
        if (period === 'AM') {
            this.setState({
                period: 'PM'
            }, () => this.props.setTime(this.state.hour, this.state.minute, this.state.period))
        } else {
            this.setState({
                period: 'AM'
            }, () => this.props.setTime(this.state.hour, this.state.minute, this.state.period))
        }
    }

    render() {
        return (
            <div className="time-wrapper">
                <div>
                    <h3>Select a Time</h3>
                    <p>Pick a start time for your tour</p>
                    <div className="time-picker">

                        <div id="time-picker_hour">
                            <div className="time-picker-up" onClick={() => this.handleHour(this.state.hour, 'up')}><i className="material-icons">keyboard_arrow_up</i></div>
                            <input type="text" readOnly value={this.state.hour} />
                            <div className="time-picker-down" onClick={() => this.handleHour(this.state.hour, 'down')}><i className="material-icons">keyboard_arrow_down</i></div>
                        </div>

                        <div id="time-picker_min">
                            <div className="time-picker-up" onClick={() => this.handleMinute(this.state.minute, 'up')}><i className="material-icons">keyboard_arrow_up</i></div>
                            <input type="text" readOnly value={(this.state.minute >= 0 && this.state.minute < 10) ? '0' + this.state.minute : this.state.minute} />
                            <div className="time-picker-down" onClick={() => this.handleMinute(this.state.minute, 'down')}><i className="material-icons">keyboard_arrow_down</i></div>
                        </div>

                        <div id="time-picker_period">
                            <div className="time-picker-up" onClick={() => this.handlePeriod(this.state.period)}><i className="material-icons">keyboard_arrow_up</i></div>
                            <input type="text" readOnly value={this.state.period} />
                            <div className="time-picker-down" onClick={() => this.handlePeriod(this.state.period)}><i className="material-icons">keyboard_arrow_down</i></div>
                        </div>

                    </div>
                </div>

                <div className="time-available-wrapper">
                    <p>I'm free for</p>
                    <input type="number" value={this.props.time_available} onChange={this.props.setTimeAvailable} />
                    <p>hours.</p>
                </div>

            </div>
        );
    }
}