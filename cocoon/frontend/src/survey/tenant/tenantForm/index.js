import React from 'react';
import { Component, Fragment } from 'react';
import Autocomplete from 'react-google-autocomplete';

export default class TenantForm extends Component {

    constructor(props){
        super(props);
        this.state = {
            isActive: false,
            isValid: false,
            occupation_type: null,
            other_occupation_reason: null,
            commute_type: null
        }
    }

    toggleQuestions = () => {
        this.setState({
            isActive: !this.state.isActive
        });
    }

    handleOccupation = (occupation_type,) => {
        this.setState({occupation_type: occupation_type});
    }

    handleOtherOccupation = (other_occupation_reason) => {
        this.setState({other_occupation_reason: other_occupation_reason});
    }

    handleCommuteType = (tenantId, commute_type) => {
        this.setState({commute_type:commute_type.commute_type}, () => this.props.setCommuteType(tenantId, commute_type));
    }

    handleValidation = (el) => {
        const q = Array.from(document.getElementById(el).querySelectorAll('.survey-question'));
        let visibleQuestions = q.filter(i => i.style.display !== 'none');
        for(let i = 0; i < visibleQuestions.length; i++) {
            if(visibleQuestions[i].querySelector('input').type === 'radio') {
                if(this.validateRadioButton(visibleQuestions[i].querySelector('input').name)) {
                    this.setState({
                        isValid: true
                    }, () => this.props.isTenantValid(this.props.index, this.state.isValid) );
                } else {
                    this.setState({
                        isValid: false
                    }, () => this.props.isTenantValid(this.props.index, this.state.isValid) );
                }
            } else {
                if(this.validateInputText(visibleQuestions[i].querySelector('input').value)) {
                    this.setState({
                        isValid: true
                    }, () => this.props.isTenantValid(this.props.index, this.state.isValid) );
                } else {
                    this.setState({
                        isValid: false
                    }, () => this.props.isTenantValid(this.props.index, this.state.isValid) );
                }
            }
        }
    }

    validateRadioButton = (el) => {
        const inputs = document.querySelectorAll(`input[name=${el}]`);
        for (let i = 0; i < inputs.length; i++) {
            if(inputs[i].checked) {
                return true;
            }
        }
        return false;
    }

    validateInputText = (val) => {
        if(val !== '') {
            return true;
        } else {
            return false;
        }
    }

    render(){
        const name = this.props.tenantInfo.first_name;
        const toggleName = this.props.index === 0 ? 'you' : this.props.tenantInfo.first_name;
        const tenantNumber = `tenants-${this.props.index}`;
        return (
            <>
                <div className="tenant-panel" onClick={() => {this.handleValidation(`tenants-${this.props.index}-questions`); this.toggleQuestions(); }} style={{borderBottom: this.state.isActive ? 'none': '1px solid var(--borderColor)'}}>
                    <div className="tenant-panel-left">
                        <i className="material-icons" style={{color: `${!this.state.isValid ? 'var(--red)' : 'var(--teal)'}`}}>
                            {!this.state.isValid ? 'error_outline' : 'check_circle_outline'}
                        </i>
                        <span>{this.props.index + 1}. {name}'s Info</span>
                    </div>
                    <span><i className="material-icons">{this.state.isActive ? 'remove' : 'add'}</i></span>
                </div>
                <div id={`tenants-${this.props.index}-questions`} onChange={(e) => this.handleValidation(`tenants-${this.props.index}-questions`)} className="tenant-questions" style={{display: this.state.isActive ? 'flex': 'none', borderBottom: this.state.isActive ? '1px solid var(--borderColor)': 'none'}}>
                    <div className="survey-question" onChange={(e) => {this.props.handleInputChange(e, 'string'); this.handleOccupation(e.target.value)}}>
                        <h2>{this.props.index === 0 ? 'Are' : 'Is'} <span>{toggleName}</span> working, studying, or other?</h2>
                        <span className="col-md-12 survey-error-message" id={`tenant-${this.props.index}_occupation_error`}>You must select the number of people.</span>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-occupation`} value="working" required />
                            <div>Working</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-occupation`} value="studying" />
                            <div>Studying</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-occupation`} value="other" />
                            <div>Other</div>
                        </label>
                    </div>

                    {/*SHOWS ONLY OTHER OCCUPATION*/}
                    <div className="survey-question" id={`${tenantNumber}-other-occupation-question`} style={{display: `${this.state.occupation_type === 'other' ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'string'); this.handleOtherOccupation(e.target.value)}}>
                        <h2>What's that <span>other</span>?</h2>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-other_reason`} value="unemployed" required />
                            <div>Unemployed</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-other_reason`} value="new-job" />
                            <div>New job</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-other_reason`} value="seeking-work" />
                            <div>Seeking work</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-other_reason`} value="not-working" />
                            <div>Not working</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-other_reason`} value="disability" />
                            <div>Disability</div>
                        </label>
                    </div>

                    {/*SHOWS ONLY IF UNEMPLOYED*/}
                    <div className="survey-question" id={`${tenantNumber}-unemployed-follow-up-question`} style={{display: `${this.state.other_occupation_reason === 'unemployed' ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'string');}}>
                        <h2>Will {toggleName} be <span>paying rent or receiving assistance</span> from a cosigner?</h2>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-unemployed_follow_up`} value="paying-solo" required />
                            <div>Paying solo</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-unemployed_follow_up`} value="paying-with-help" />
                            <div>Getting help</div>
                        </label>
                    </div>

                    {this.props.commute_type_options &&
                        <div className="survey-question" id={`${tenantNumber}commute_type-question`}>
                            <h2>How {this.props.index === 0 ? 'do' : 'does'} {toggleName} <span>commute</span>?</h2>
                            {this.props.commute_type_options.map((o, index) => (
                            <label className="col-md-6 survey-label" key={index} onChange={(e) => this.handleCommuteType(tenantNumber, this.props.commute_type_options[index])}>
                                <input type="radio" name={`${tenantNumber}-commute_type`} value={o.id} />
                                <div>{o.commute_type}</div>
                            </label>
                        ))}
                        </div>
                    }

                    <div className="survey-question" id={`${tenantNumber}-other-occupation-question`} style={{display: `${this.state.occupation_type === 'other' && this.state.commute_type !== 'Work From Home' ? 'block' : 'none'}`}}>
                        <h2>Is there somewhere {toggleName} <span>{this.props.index === 0 ? 'visit' : 'visits'} regularly</span>?</h2>
                        <Autocomplete
                            className="col-md-12 survey-input"
                            onPlaceSelected={(place) => { this.props.setCommuteAddress(`${tenantNumber}-`, place) }}
                            types={['address']}
                            name={`${tenantNumber}-commute_address`}
                            placeholder={'Street Address'}
                        />
                    </div>

                    {/*SHOWS ONLY ON STUDYING OCCUPATION*/}
                    <div className="survey-question" id={`${tenantNumber}-other-occupation-question`} style={{display: `${this.state.occupation_type === 'studying' && this.state.commute_type !== 'Work From Home' ? 'block' : 'none'}`}}>
                        <h2>What's the <span>address of the campus</span> {toggleName} {this.props.index === 0 ? 'attend' : 'attends'}?</h2>
                        <Autocomplete
                            className="col-md-12 survey-input"
                            onPlaceSelected={(place) => { this.props.setCommuteAddress(`${tenantNumber}-`, place) }}
                            types={['address']}
                            name={`${tenantNumber}-commute_address`}
                            placeholder={'School Address'}
                        />
                    </div>

                    {/*SHOWS ONLY ON WORKING OCCUPATION*/}
                    <div className="survey-question" id={`${tenantNumber}-other-occupation-question`} style={{display: `${this.state.occupation_type === 'working' && this.state.commute_type !== 'Work From Home' ? 'block' : 'none'}`}}>
                        <h2>What's the <span>work address</span> for {toggleName}?</h2>
                        <Autocomplete
                            className="col-md-12 survey-input"
                            onPlaceSelected={(place) => { this.props.setCommuteAddress(`${tenantNumber}-`, place) }}
                            types={['address']}
                            name={`${tenantNumber}-commute_address`}
                            placeholder={'Work Address'}
                        />
                    </div>

                    {/*SHOWS ONLY ON DRIVING COMMUTE_TYPE*/}
                    <div className="survey-question" id={`${tenantNumber}-driving-follow-up-question`} style={{display: `${this.state.commute_type === 'Driving' ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'string');}}>
                        <h2>What are the <span>driving options</span>?</h2>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-driving_condition`} value="with-traffic" required />
                            <div>With traffic</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-driving_condition`} value="without-traffic" />
                            <div>Without traffic</div>
                        </label>
                    </div>

                    {/*SHOWS ONLY ON TRANSIT COMMUTE_TYPE*/}
                    <div className="survey-question" id={`${tenantNumber}-transit-follow-up-question`} style={{display: `${this.state.commute_type === 'Transit' ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'string');}}>
                        <h2>What form of <span>transit</span>?</h2>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-transit_type`} value="bus" required />
                            <div>Bus</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-transit_type`} value="train" />
                            <div>Train</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-transit_type`} value="commuter-rail" />
                            <div>Commuter rail</div>
                        </label>
                    </div>

                    <div className="survey-question" id={`${tenantNumber}-desired_commute-question`} style={{display: `${this.state.commute_type !== 'Work From Home' ? 'block' : 'none'}`}} onBlur={(e) => {this.props.handleInputChange(e, 'number');}}>
                        <h2>How <span>long of a commute</span> {this.props.index === 0 ? 'do' : 'does'} {toggleName} want?</h2>
                        <input className="col-md-12 survey-input" type="number" name={`${tenantNumber}-desired_commute`} placeholder="Time in minutes" />
                    </div>

                    <div className="survey-question" id={`${tenantNumber}-commute_weight-question`} style={{display: `${this.state.commute_type !== 'Work From Home' ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'string');}}>
                        <h2>How <span>important is commute</span> to {toggleName}?</h2>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-commute_weight`} value="0" required />
                            <div>0</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-commute_weight`} value="1" />
                            <div>1</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-commute_weight`} value="2" />
                            <div>2</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-commute_weight`} value="3" />
                            <div>3</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-commute_weight`} value="4" />
                            <div>4</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-commute_weight`} value="5" />
                            <div>5</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-commute_weight`} value="6" />
                            <div>6</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-commute_weight`} value="7" />
                            <div>7</div>
                        </label>
                    </div>

                    <div className="survey-question" id={`${tenantNumber}-income-question`} onBlur={(e) => {this.props.handleInputChange(e, 'number');}}>
                        <h2>What is {this.props.index === 0 ? 'your' : `${toggleName}'s`} <span>approximate income</span>?</h2>
                        <input className="col-md-12 survey-input" type="number" name={`${tenantNumber}-income`} placeholder="Yearly salary" step="1000"/>
                    </div>

                    <div className="survey-question" id={`${tenantNumber}-credit_score-question`} onChange={(e) => {this.props.handleInputChange(e, 'string');}}>
                        <h2>What is {this.props.index === 0 ? 'your' : `${toggleName}'s`} <span>approximate credit score</span>?</h2>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-credit_score`} value="less than 500" required />
                            <div>&lt; 500</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-credit_score`} value="500 - 550" />
                            <div>500 - 550</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-credit_score`} value="551 - 600" />
                            <div>551 - 600</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-credit_score`} value="601 - 650" />
                            <div>601 - 650</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-credit_score`} value="651 - 700" />
                            <div>651 - 700</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-credit_score`} value="701 - 750" />
                            <div>701 - 750</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-credit_score`} value="751 - 800" />
                            <div>751 - 800</div>
                        </label>
                        <label className="col-md-3 col-xs-6 survey-label">
                            <input type="radio" name={`${tenantNumber}-credit_score`} value="801 - 850" />
                            <div>801 - 850</div>
                        </label>
                    </div>

                </div>
            </>
        );
    }
}
