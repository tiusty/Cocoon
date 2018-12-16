import React from 'react';
import { Component } from 'react';

import './tenantForm.css'

export default class Tenant extends Component {

    constructor(props){
        super(props);
        this.state = {
            // General state information
            tenant_identifier: 'tenant-' + this.props.id,
            is_active: false,

            // Survey questions state
            occupation: null,
            new_job: null,
            other_occupation_reason: null,

            commute_type: null
        }
    }

    componentDidMount = () => {
        if(this.props.id === 0) {
            this.setState({
                is_active: !this.state.is_active
            });
        }
    };

    toggleQuestions = () => {
        this.setState({
            is_active: !this.state.is_active
        });
    };


    // VALIDATION FUNCTIONS //
    handleValidation = () => {
        let valid = true;
        valid = valid && this.handleOccupationValidation();
        valid = valid && this.handleOccupationFollowupValidation();
        return valid
    };

    handleOccupationValidation() {
        let valid = true;
        if (!this.state.occupation) {
            valid = false;
        }
        return valid
    }

    handleOccupationFollowupValidation() {
        let valid = true;
        if (this.state.occupation === 'working') {
            if (!this.state.new_job) {
                valid = false;
            }
        } else if (this.state.occupation === 'other') {
            if (!this.state.other_reason) {
                valid = false
            }
        }
        return valid
    }


    // HANDLE INPUTS //
    handleInputChange = (e, type) => {
        const { name, value } = e.target;
        const nameStripped = name.replace(this.state.tenant_identifier+'-', '');
        if(type === 'number') {
            this.setState({
                [nameStripped]: parseInt(value)
            });
        } else {
            this.setState({
                [nameStripped]: value
            });
        }
    }

    handleTenantPanelClick = () => {
        this.handleValidation();
        this.toggleQuestions();
    };

    handleTenantPanelIcon = () => {
        if (this.handleValidation()) {
            return 'check_circle_outline'
        } else {
            return 'error_outline'
        }
    };

    handleTenantPanelClasses() {
        let classes = "tenant-panel ";
        if (this.state.is_active) {
            classes = classes + ' panel-active';
        }
        return classes
    }

    handleTenantIconClasses = () => {
        let classes = 'material-icons ';
        if (this.handleValidation()) {
            classes = classes + 'valid-panel'
        } else {
            classes = classes + 'invalid-panel'
        }
        return classes
    };

    handleTenantQuestionClasses() {
        let classes = "tenant-questions ";
        if (this.state.is_active) {
            classes = classes + "tenant-questions-active"
        }
        return classes
    }


    // Rendering functions //
    renderOccupation() {
        return (
            <div className="survey-question" onChange={(e) => {this.handleInputChange(e, 'string');}}>
                <h2>{this.props.index === 0 ? 'Are' : 'Is'} <span>{name}</span> working, studying, or other?
                </h2>
                <span className="col-md-12 survey-error-message" id={`${this.state.tenant_identifier}-occupation-error`}>You must select an occupation type.</span>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-occupation`} value="working"
                           checked={this.state.occupation === 'working'}
                           onChange={() => {}}
                    />
                    <div>Working</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-occupation`} value="studying"
                           checked={this.state.occupation === 'studying'}
                           onChange={() => {}}
                    />
                    <div>Studying</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-occupation`} value="other"
                           checked={this.state.occupation === 'other'}
                           onChange={() => {}}
                    />
                    <div>Other</div>
                </label>
            </div>
        );
    }

    renderOccupationFollowupQuestions(name) {
        if (this.state.occupation === 'working') {
            return this.renderWorkingOccupation(name)
        } else if (this.state.occupation === 'other') {
            return this.renderOtherOccupation()
        }
    }

    renderWorkingOccupation = (name) => {
        return (
            <div className="survey-question" id={`${this.state.tenant_identifier}-working-occupation-question`} onChange={(e) => this.handleInputChange(e, 'string')}>
                <h2>{this.props.id === 0 ? 'Have' : 'Has'} {name} been at this <span>job for less than 6 months</span>?</h2>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-new_job`} value={true} checked={this.state.new_job === "true"} onChange={() => {}} />
                    <div>Yes</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-new_job`} value={false} checked={this.state.new_job === "false"} onChange={() => {}} />
                    <div>No</div>
                </label>
            </div>
        );
    };

    renderOtherOccupation = () => {
        return (
            <div className="survey-question" id={`${this.state.tenant_identifier}-other-occupation-question`} onChange={(e) => this.handleInputChange(e, 'string')}>
                <h2>What's that <span>other</span>?</h2>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-other_occupation_reason`} value="unemployed" checked={this.state.other_occupation_reason === 'unemployed'} onChange={() => {}} />
                    <div>Unemployed</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-other_occupation_reason`} value="seeking-work" checked={this.state.other_occupation_reason === 'seeking-work'} onChange={() => {}} />
                    <div>Seeking work</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-other_occupation_reason`} value="not-working" checked={this.state.other_occupation_reason === 'not-working'} onChange={() => {}} />
                    <div>Not working</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-other_occupation_reason`} value="disability" checked={this.state.other_occupation_reason === 'disability'} onChange={() => {}} />
                    <div>Disability</div>
                </label>
            </div>
        );
    };

    render() {
        const name = this.props.tenantInfo.first_name;
        const tenant_identifier = this.state.tenant_identifier;
        return (
            <>
                <div className={this.handleTenantPanelClasses()} onClick={this.handleTenantPanelClick}>
                    <div className="tenant-panel-left">
                        <i className={this.handleTenantIconClasses()}>
                            {this.handleTenantPanelIcon()}
                        </i>
                        <span>{name}'s Info</span>
                    </div>
                    <span><i className="material-icons">{this.state.is_active ? 'remove' : 'add'}</i></span>
                </div>
                <div id={`${tenant_identifier}-questions`} className={this.handleTenantQuestionClasses()}
                     onChange={() => this.handleValidation()}>
                    {this.renderOccupation()}
                    {this.renderOccupationFollowupQuestions(name)}
                </div>
            </>
        );
    }
}