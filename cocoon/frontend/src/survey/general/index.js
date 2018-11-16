import React from 'react';
import { Component, Fragment } from 'react';
import InputRange from 'react-input-range';
import DayPickerInput from 'react-day-picker/DayPickerInput';
import 'react-day-picker/lib/style.css';

export default class General extends Component {

    constructor(props) {
        super(props);
        this.state = {
            value: {
                min: 1000,
                max: 3000
            },
            selectedDayEarliest: undefined,
            selectedDayLatest: undefined
        }
    }

    componentWillUnmount = () => {
        this.props.setFinalTenants();
    }

    // Splits name inputs into first and last names
    handleTenantName = (e) => {
        const { name, value } = e.target;
        const first_name = value.split(' ').slice(0, -1).join(' ');
        const last_name = value.split(' ').slice(-1).join(' ');
        const index = e.target.dataset.tenantkey;
        if(first_name !== '' && last_name !== '') {
            this.props.setTenants(first_name, last_name, index);
        }
    }

    getMaxPrice = (number_of_tenants) => {
        if(number_of_tenants === 1) {
            return 4000;
        } else if (number_of_tenants < 4) {
            return (number_of_tenants * 3) * 1000;
        } else {
            return 10000;
        }
    }

    handleEarliestClick = (day, { selected }) => {
        this.setState({
            selectedDayEarliest: selected ? undefined : day
        }, () => this.props.setMoveDate('earliest_move_in', this.state.selectedDayEarliest))
    }

    handleLatestClick = (day, { selected }) => {
        this.setState({
            selectedDayLatest: selected  ? undefined : day
        }, () => this.props.setMoveDate('latest_move_in', this.state.selectedDayLatest))
    }

    render(){
        return (
            <>
                <div className="survey-question" onChange={(e) => {this.props.handleRadioChange(e, 'number');}}>
                    <h2>How many people are you <span>searching with</span>?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="1" required />
                        <div>Just Me</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="2" />
                        <div>Me + 1 other</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="3" />
                        <div>Me + 2 others</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="4" />
                            <div>Me + 3 others</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="5" />
                        <div>Me + 4 others</div>
                    </label>
                </div>

                <div className="survey-question">
                    <h2>What's <span>your {this.props.number_of_tenants === 1 ? 'name' : 'names'}</span>?</h2>
                    <input className="col-md-12 survey-input" type="text" name="tenant_name" placeholder="Full Name" required data-tenantkey={0} onBlur={this.handleTenantName}/>
                    {Array.from(Array(this.props.number_of_tenants - 1)).map((t,i) => { 1
                        return <input className="col-md-12 survey-input" type="text" name={'roommate_name_' + (i + 1)} required data-tenantkey={i + 1} placeholder="Roommate Name" onBlur={this.handleTenantName} key={i} />
                    })}
                </div>

                <div className="survey-question">
                    <h2>How much rent do you <span>want to pay</span>?</h2>
                    <InputRange
                        draggableTrack
                        maxValue={this.getMaxPrice(this.props.number_of_tenants)}
                        minValue={0}
                        value={this.state.value}
                        onChange={value => {this.setState({value});this.props.setPrice(this.state.value.min, this.state.value.max);}}
                        formatLabel={value => `$${value}`} />
                </div>

                <div className="survey-question">
                    <h2>When are you wanting to <span>move in</span>?</h2>
                    <div className="col-md-6 date-wrapper">
                        <DayPickerInput
                            placeholder={'Earliest'}
                            onDayChange={this.handleEarliestClick} />
                    </div>
                    <div className="col-md-6 date-wrapper">
                        <DayPickerInput
                            placeholder={'Latest'}
                            onDayChange={this.handleLatestClick} />
                    </div>
                </div>

                <div className="survey-question" onChange={(e) => {this.props.handleRadioChange(e, 'number');}}>
                    <h2>How badly do you <span>need to move</span>?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="move_weight" value="0" required />
                        <div>Just browsing</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="move_weight" value="1" required />
                        <div>Another option</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="move_weight" value="2" required />
                        <div>Third Choice</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="move_weight" value="3" required />
                        <div>I gotta move!</div>
                    </label>
                </div>

                <div className="survey-question" onChange={(e) => {this.props.handleRadioChange(e, 'number');}}>
                    <h2>How many <span>bedrooms</span> do you need?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="num_bedrooms" value="0" required />
                        <div>Studio</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="num_bedrooms" value="1" required />
                        <div>1 bed</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="num_bedrooms" value="2" required />
                        <div>2 beds</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="num_bedrooms" value="3" required />
                        <div>3 beds</div>
                    </label>
                </div>

                <button className="col-md-12 survey-btn" onClick={this.props.handleNextStep}>
                    Next
                </button>
            </>
        );
    }
}
