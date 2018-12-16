import React from 'react';
import { Component } from 'react';

export default class GeneralForm extends Component {

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
        if(this.props.tenants.length > id && (this.props.tenants[id].first_name || this.props.tenants[id].last_name)) {
            let first_name = '';
            if(this.props.tenants[id].first_name) {
                first_name = this.props.tenants[id].first_name
            }
            let last_name = ''
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

    render() {
        return (
            <>
                {this.renderNumberOfPeopleQuestion()}
                {this.renderNameQuestion()}
            </>
        );
    }
}
