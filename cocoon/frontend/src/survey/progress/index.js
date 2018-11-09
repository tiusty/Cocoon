import React from 'react';
import { Component, Fragment } from 'react';

export default class Progress extends Component {
    render(){
        return (
            <div className="survey-progress-bar">
                <span className={`progress-bar-step ${this.props.step === 1 ? 'progress-bar-step_active' : ''}`}>General Info</span>
                <span className={this.props.step === 1 ? 'progress-bar-step_active' : ''}>></span>
                <span className={`progress-bar-step ${this.props.step === 2 ? 'progress-bar-step_active' : ''}`}>Tenant Info</span>
                <span className={this.props.step === 2 ? 'progress-bar-step_active' : ''}>></span>
                <span className={`progress-bar-step ${this.props.step === 3 ? 'progress-bar-step_active' : ''}`}>Amenities</span>
                <span className={this.props.step === 3 ? 'progress-bar-step_active' : ''}>></span>
                <span className={`progress-bar-step ${this.props.step === 4 ? 'progress-bar-step_active' : ''}`}>Details</span>
            </div>
        );
    }
}
