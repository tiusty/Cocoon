import React from 'react';
import { Component } from 'react';
import axios from "axios";
import InputRange from 'react-input-range';
import DayPickerInput from 'react-day-picker/DayPickerInput';

import houseDatabase_endpoints from "../../../endpoints/houseDatabase_endpoints";

export default class GeneralForm extends Component {
    state = {
        home_type_options: [],
        value: {
            min: 1000,
            max: 3000,
        }
    };

    componentDidMount = () => {
        // Retrieve all the home types
        axios.get(houseDatabase_endpoints['home_types'])
            .then(res => {
                const home_type_options = res.data;
                this.setState({ home_type_options });
            });
    };

    handleValidation = () => {
        let valid = true;
        valid = valid && this.handleNameValidation();
        console.log(valid)
        valid = valid && this.handleHomeTypeValidation();
        console.log(valid)
        valid = valid && this.handlePriceValidation();
        console.log(valid)
        valid = valid && this.handleMoveAsapValidation();
        console.log(valid)
        valid = valid && this.handleDatePickerValidation();
        console.log(valid)
        valid = valid && this.handleUrgencyValidation();
        valid = valid && this.handleBedroomValidation()
        return valid
    };

    handleNameValidation() {
        let valid = true;
        if (this.props.tenants.length < this.props.number_of_tenants) {
            valid = false
        } else {
            for(let i=0; i<this.props.number_of_tenants; i++) {
                if(!this.props.tenants[i].first_name || !this.props.tenants[i].last_name) {
                    valid = false
                }
            }
        }
        return valid
    }

    handleHomeTypeValidation() {
        let valid = true;
        if (this.props.generalInfo.home_type.length === 0) {
            valid = false
        }
        return valid
    }

    handlePriceValidation() {
        let valid = true;
        if (this.props.desired_price < 0) {
            valid = false
        }
        if (this.props.max_price < 0) {
            valid = false
        }
        if (this.props.price_weight < 0) {
            valid = false
        }
        return valid
    }

    handleMoveAsapValidation() {
        let valid = true;
        if (!this.props.generalInfo.is_move_asap === 'no' || !this.props.generalInfo.is_move_asap === 'yes') {
            valid = false
        }
        return valid
    }

    handleDatePickerValidation() {
        let valid = true;
        if (this.props.generalInfo.is_move_asap !== 'yes') {
            if (this.props.generalInfo.earliest_move_in === undefined ||
            this.props.generalInfo.latest_move_in === undefined) {
                valid  = false
            }
        }
        return valid
    }

    handleUrgencyValidation() {
        let valid = true;
        if (this.props.generalInfo.move_weight < 0) {
            valid = false
        }
        return valid
    }

    handleBedroomValidation() {
        let valid = true;
        if (this.props.generalInfo.num_bedrooms === undefined){
            valid = false
        } else {
            if (this.props.generalInfo.num_bedrooms < 0) {
                valid = false
            }
        }
        return valid
    }

    renderNumberOfPeopleQuestion() {
        return (
            <div className="survey-question" onChange={(e) => this.props.onInputChange(e, 'number')}>
                <h2>How many people are you <span>searching with</span>?</h2>
                <span className="col-md-12 survey-error-message" id="number_of_tenants_error">You must select the number of people.</span>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="1" checked={this.props.number_of_tenants === 1} onChange={() => {}} />
                    <div>Just Me</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="2" checked={this.props.number_of_tenants === 2} onChange={() => {}} />
                    <div>Me + 1 other</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="3" checked={this.props.number_of_tenants === 3} onChange={() => {}} />
                    <div>Me + 2 others</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="4" checked={this.props.number_of_tenants === 4} onChange={() => {}} />
                    <div>Me + 3 others</div>
                </label>
            </div>
        );
    }

    setNameOnField(id) {
        // Display the name if the tenant exists and either a first or last name exists
        if(this.props.tenants.length > id && (this.props.tenants[id].first_name || this.props.tenants[id].last_name)) {
            let first_name = '';
            if(this.props.tenants[id].first_name) {
                first_name = this.props.tenants[id].first_name
            }
            let last_name = '';
            if(this.props.tenants[id].last_name) {
                last_name = this.props.tenants[id].last_name
            }
            return first_name + ' ' + last_name
        } else {
            return ''
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

    renderNameQuestion() {
        return (
            <div className="survey-question" id="tenant_names">
                <h2>What <span>{this.props.number_of_tenants <= 1 ? ' is your name' : ' are your names'}</span>?</h2>
                <span className="col-md-12 survey-error-message" id="name_of_tenants_error">Enter first and last name separated by a space.</span>
                <input className="col-md-12 survey-input" type="text" name="tenant_name"
                       placeholder="First and Last Name" autoCapitalize={'words'} data-tenantkey={0}
                       value={this.setNameOnField(0)} onChange={this.props.onHandleTenantName}/>
                {this.props.number_of_tenants > 1 && Array.from(Array(this.props.number_of_tenants - 1)).map((t, i) => {
                    return <input className="col-md-12 survey-input" type="text" name={'roommate_name_' + (i + 1)}
                                  autoCapitalize={'words'} data-tenantkey={i + 1} placeholder="First and Last Name"
                                  value={this.setNameOnField(i+1)} onChange={this.props.onHandleTenantName}
                                  key={i}/>
                })}
            </div>
        );
    }

    renderHomeTypeQuestion() {
        if(this.state.home_type_options) {
            return (
                <div className="survey-question" onChange={this.validateHomeType}>
                    <h2>What <span>kind of home</span> do you want?</h2>
                    <span className="col-md-12 survey-error-message" id="home_type_error">You must select at least one type of home.</span>
                    {this.state.home_type_options.map((o, index) => (
                        <label className="col-md-6 survey-label survey-checkbox" key={index} onChange={(e) => this.props.setHomeTypes(e, index, o.id)}>
                            <input type="checkbox" name="home_type" value={o.id} checked={this.props.generalInfo.home_type.length && this.props.generalInfo.home_type.some(i => i === o.id)} onChange={() => {}} />
                            <div>{o.home_type} <i className="material-icons">check</i></div>
                        </label>
                    ))}
                </div>

            );
        }
    }

    renderPriceQuestion() {
        return(
            <div className="survey-question">
                <h2>How much rent do you <span>want to pay</span>?</h2>
                <InputRange
                    draggableTrack
                    maxValue={this.getMaxPrice(this.props.number_of_tenants)}
                    minValue={0}
                    step={50}
                    value={this.state.value}
                    onChange={value => {this.setState({value});this.props.setPrice(this.state.value.min, this.state.value.max);}}
                    formatLabel={value => `$${value}`} />
            </div>
        );
    }

    renderPriceWeightQuestion() {
        return (
            <div className="survey-question" onChange={(e) =>this.props.onGeneralInputChange(e, 'number')}>
                <h2>How <span>important is the price</span>?</h2>
                <span className="col-md-12 survey-error-message" id="price_weight_error">You must choose how much you care about the price.</span>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="0" checked={this.props.generalInfo.price_weight === 0} onChange={() => {}} />
                    <div>Don’t care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="1" checked={this.props.generalInfo.price_weight === 1} onChange={() => {}} />
                    <div>Slightly care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="2" checked={this.props.generalInfo.price_weight === 2} onChange={() => {}} />
                    <div>Cares</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="3" checked={this.props.generalInfo.price_weight === 3} onChange={() => {}} />
                    <div>Really care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="4" checked={this.props.generalInfo.price_weight === 4} onChange={() => {}} />
                    <div>Super important</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="5" checked={this.props.generalInfo.price_weight === 5} onChange={() => {}} />
                    <div>Top priority!</div>
                </label>
            </div>
        );
    }

    renderMoveAsapQuestion() {
        return (
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'string')}>
                <h2>Are you looking to move in <span>as soon as possible?</span></h2>
                <span className="col-md-12 survey-error-message" id="date_error">You must select an answer.</span>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="is_move_asap" value="yes" checked={this.props.generalInfo.is_move_asap === 'yes'} onChange={() => {}} />
                    <div>Yes</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="is_move_asap" value="no" checked={this.props.generalInfo.is_move_asap === 'no'} onChange={() => {}} />
                    <div>No</div>
                </label>
            </div>
        );
    }

    renderDatePickingQuestion() {
        if (this.props.generalInfo.is_move_asap !== "yes") {
            return (
                <>
                    <h2>When are you wanting to <span>move in</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="date_error">You must select an earliest and latest move in date.</span>
                    <div className="col-md-6 date-wrapper">
                        <DayPickerInput
                            placeholder={'Earliest'}
                            onDayChange={this.props.handleEarliestClick}
                            value={this.props.generalInfo.earliest_move_in} onChange={() => {}} />
                    </div>
                    <div className="col-md-6 date-wrapper">
                        <DayPickerInput
                            placeholder={'Latest'}
                            onDayChange={this.props.handleLatestClick}
                            value={this.props.generalInfo.latest_move_in} onChange={() => {}} />
                    </div>
                </>
            );
        } else {
            return null
        }
    }

    renderUrgencyQuestion() {
        return(
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'number')}>
                <h2>How badly do you <span>need to move</span>?</h2>
                <span className="col-md-12 survey-error-message" id="move_weight_error">You must select an option.</span>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="0" checked={this.props.generalInfo.move_weight === 0} onChange={() => {}} />
                    <div>Just browsing</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="1" checked={this.props.generalInfo.move_weight === 1} onChange={() => {}} />
                    <div>{this.props.number_of_tenants === 1 ? "I've" : "We've"} got some time</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="2" checked={this.props.generalInfo.move_weight === 2} onChange={() => {}} />
                    <div>Moving soon</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="3" checked={this.props.generalInfo.move_weight === 3} onChange={() => {}} />
                    <div>{this.props.number_of_tenants === 1 ? "I" : "We"} gotta move!</div>
                </label>
            </div>
        );
    }

    renderBedroomQuesiton() {
        return(
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'number')}>
                <h2>How many <span>bedrooms</span> do you need?</h2>
                <span className="col-md-12 survey-error-message" id="number_of_rooms_error">You must select the number of rooms.</span>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="num_bedrooms" value="0" checked={this.props.generalInfo.num_bedrooms === 0} onChange={() => {}} />
                    <div>Studio</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="num_bedrooms" value="1" checked={this.props.generalInfo.num_bedrooms === 1} onChange={() => {}} />
                    <div>1 bed</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="num_bedrooms" value="2" checked={this.props.generalInfo.num_bedrooms === 2} onChange={() => {}} />
                    <div>2 beds</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="num_bedrooms" value="3" checked={this.props.generalInfo.num_bedrooms === 3} onChange={() => {}} />
                    <div>3 beds</div>
                </label>
            </div>
        );
    }

    handleNextButtonAction(e) {
        if(this.handleValidation()) {
            this.props.handleNextStep(e)
        }
    }

    render() {
        return (
            <>
                {this.renderNumberOfPeopleQuestion()}
                {this.renderNameQuestion()}
                {this.renderHomeTypeQuestion()}
                {this.renderPriceQuestion()}
                {this.renderPriceWeightQuestion()}
                {this.renderMoveAsapQuestion()}
                {this.renderDatePickingQuestion()}
                {this.renderUrgencyQuestion()}
                {this.renderBedroomQuesiton()}

                <button className="col-md-12 survey-btn" onClick={(e) => this.handleNextButtonAction(e)} >
                    Next
                </button>
            </>
        );
    }
}
