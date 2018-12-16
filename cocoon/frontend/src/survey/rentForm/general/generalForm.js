import React from 'react';
import { Component } from 'react';
import axios from "axios";

import houseDatabase_endpoints from "../../../endpoints/houseDatabase_endpoints";

export default class GeneralForm extends Component {
    state = {
        home_type_options: [],
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
        valid = valid && this.handleHomeTypeValidation();
        console.log(valid)
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

    handleNextButtonAction(e) {
        if(this.handleValidation()) {
            // this.props.handleNextStep(e)
        }
    }

    render() {
        return (
            <>
                {this.renderNumberOfPeopleQuestion()}
                {this.renderNameQuestion()}
                {this.renderHomeTypeQuestion()}

                <button className="col-md-12 survey-btn" onClick={(e) => this.handleNextButtonAction(e)} >
                    Next
                </button>
            </>
        );
    }
}
