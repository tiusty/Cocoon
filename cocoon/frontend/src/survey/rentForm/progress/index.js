import React from 'react';
import { Component, Fragment } from 'react';

export default class Progress extends Component {

    handleStepClick = (step) => {
        console.log(step)
        if (step <= this.props.maxStep) {
            this.props.goToStep(step);
        }
    }

    handleCursorStyle = (step) => {
        if (step <= this.props.maxStep) {
            return 'pointer';
        } else {
            return 'not-allowed';
        }
    }

    render(){
        return (
            <div className="survey-progress-bar">
                <span style={{cursor: this.handleCursorStyle(1)}} className={`progress-bar-step ${this.props.step >= 1 ? 'progress-bar-step_active' : ''}`} onClick={() => this.handleStepClick(1)}>General Info</span>
                <span className={this.props.step === 1 ? 'progress-bar-step_active' : ''}>></span>
                <span style={{cursor: this.handleCursorStyle(2)}} className={`progress-bar-step ${this.props.step >= 2 ? 'progress-bar-step_active' : ''}`} onClick={() => this.handleStepClick(2)}>Tenant Info</span>
                <span className={this.props.step === 2 ? 'progress-bar-step_active' : ''}>></span>
                <span style={{cursor: this.handleCursorStyle(3)}} className={`progress-bar-step ${this.props.step >= 3 ? 'progress-bar-step_active' : ''}`} onClick={() => this.handleStepClick(3)}>Amenities</span>
                <span className={this.props.step === 3 ? 'progress-bar-step_active' : ''}>></span>
                <span style={{cursor: this.handleCursorStyle(4)}} className={`progress-bar-step ${this.props.step >= 4 ? 'progress-bar-step_active' : ''}`} onClick={() => this.handleStepClick(4)}>Details</span>
            </div>
        );
    }
}
