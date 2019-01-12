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
            period: undefined,
        }
    }

    componentDidMount = () => {
        this.setInitialTime(this.state.time);
    }

    componentDidUpdate = (prevProps) => {
        if (this.props.date !== prevProps.date) {
            this.setInitialTime(this.state.time);
        }
    }

    setInitialTime = (time) => {
        this.setState({
            hour: ((time.getHours() + 11) % 12 + 1),
            minute: (Math.ceil(time.getMinutes() / 15) * 15) === 60 ? 45 : Math.ceil(time.getMinutes() / 15) * 15,
            period: time.getHours() >= 12 ? 'PM' : 'AM'
        }, () => {
            this.props.setTime(this.state.hour, this.state.minute, this.state.period)
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

    renderAvailableOptions = () => {
        let hours = Math.floor(this.props.tour_duration_seconds / 3600);
        let minuteDivisor = this.props.tour_duration_seconds % 3600;
        let minutes = Math.ceil((Math.floor(minuteDivisor / 60)) / 15) * 15;
        let minTime = parseFloat(hours + (minutes / 60));
        let maxTime = parseInt(hours + 6);

        let options = [];
        for (let i = minTime; i < maxTime; i+= .25) {
            options.push(i);
        }

        return (
            <select id="picker_available" onChange={this.props.setTimeAvailable}>
                {options.map(o => (
                    <option value={o} key={o}>{o} hours</option>
                ))}
            </select>
        );

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
                    <p>How long are you free for?</p>
                    {this.renderAvailableOptions()}
                    {/*<p className="time-available-error">NOTE: Cannot be shorter than {this.props.formatTimeAvailable(this.props.tour_duration_seconds)}</p>*/}
                </div>

            </div>
        );
    }
}