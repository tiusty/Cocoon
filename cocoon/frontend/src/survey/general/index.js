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
        }, () => this.props.setSurveyState('earliest_move_in', this.state.selectedDayEarliest))
    }

    handleLatestClick = (day, { selected }) => {
        this.setState({
            selectedDayLatest: selected  ? undefined : day
        }, () => this.props.setSurveyState('latest_move_in', this.state.selectedDayLatest))
    }

    handleValidation = () => {
        return this.validateRadioButton('number_of_tenants', '#number_of_tenants_error')
            && this.validateTenantNames()
            && this.validateDates()
            && this.validateRadioButton('move_weight', '#move_weight_error')
            && this.validateRadioButton('num_bedrooms', '#number_of_rooms_error');
    }

    validateTenantNames = () => {
        const inputs = Array.from(document.querySelectorAll('#tenant_names input[type=text]'));
        let emptyFields = inputs.filter(i => i.value === '');
        if(emptyFields.length > 0) {
            document.querySelector('#name_of_tenants_error').style.display = 'block';
            document.querySelector('#name_of_tenants_error').parentNode.scrollIntoView(true);
            return false;
        } else {
            document.querySelector('#name_of_tenants_error').style.display = 'none';
            return true;
        }
    }

    validateDates = () => {
        if(this.state.selectedDayEarliest && this.state.selectedDayLatest) {
            document.querySelector('#date_error').style.display = 'none';
            return true;
        } else {
            document.querySelector('#date_error').style.display = 'block';
            document.querySelector('#date_error').parentNode.scrollIntoView(true);
            return false;
        }
    }

    validateRadioButton = (el, err) => {
        const inputs = document.querySelectorAll(`input[name=${el}]`);
                for (let i = 0; i < inputs.length; i++) {
            if(inputs[i].checked) {
                document.querySelector(err).style.display = 'none';
                return true;
            }
        }
        document.querySelector(err).style.display = 'block';
        document.querySelector(err).parentNode.scrollIntoView(true);
        return false;
    }

    render(){
        return (
            <>
                <div className="survey-question" onChange={(e) => {this.props.handleInputChange(e, 'number'); this.validateRadioButton('number_of_tenants', '#number_of_tenants_error');}}>
                    <h2>How many people are you <span>searching with</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="number_of_tenants_error">You must select the number of people.</span>
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

                <div className="survey-question" id="tenant_names">
                    <h2>What's <span>your {this.props.number_of_tenants === 1 ? 'name' : 'names'}</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="name_of_tenants_error">Enter first and last name separated by a space.</span>
                    <input className="col-md-12 survey-input" type="text" name="tenant_name" placeholder="First and Last Name" autoCapitalize={'words'} required data-tenantkey={0} onChange={this.handleTenantName}/>
                    {Array.from(Array(this.props.number_of_tenants - 1)).map((t,i) => { 1
                        return <input className="col-md-12 survey-input" type="text" name={'roommate_name_' + (i + 1)} autoCapitalize={'words'} required data-tenantkey={i + 1} placeholder="First and Last Name" onChange={this.handleTenantName} key={i} />
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
                    <span className="col-md-12 survey-error-message" id="date_error">You must select an earliest and latest move in date.</span>
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

                <div className="survey-question" onChange={(e) => {this.props.handleInputChange(e, 'number'); this.validateRadioButton('move_weight', '#move_weight_error');}}>
                    <h2>How badly do you <span>need to move</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="move_weight_error">You must select an option.</span>
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

                <div className="survey-question" onChange={(e) => {this.props.handleInputChange(e, 'number'); this.validateRadioButton('num_bedrooms', '#number_of_rooms_error');}}>
                    <h2>How many <span>bedrooms</span> do you need?</h2>
                    <span className="col-md-12 survey-error-message" id="number_of_rooms_error">You must select the number of rooms.</span>
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

                <button className="col-md-12 survey-btn" onClick={(e) => this.handleValidation() && this.props.handleNextStep(e)}>
                    Next
                </button>
            </>
        );
    }
}
