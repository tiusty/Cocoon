import React from 'react';
import { Component, Fragment } from 'react';

export default class Progress extends Component {

    componentDidMount = () => {
        this.handleStepTitle();
    }

    componentDidUpdate = (prevProps) => {
        if (this.props.maxStep !== prevProps.maxStep) {
            this.handleStepTitle();
        }
    }

    handleStepClick = (step) => {
        if (step <= this.props.maxStep) {
            this.props.goToStep(step);
        }
    }

    handleLinkStyle = (step) => {
        let style = null;
        if (step <= this.props.maxStep) {
            style = {
                cursor: 'pointer',
                textDecoration: 'underline'
            }
        } else {
            style = {
                cursor: 'not-allowed',
                textDecoration: 'none'
            }
        }
        return style;
    }

    handleStepTitle = () => {
        const steps = document.querySelectorAll('.progress-bar-step');
        for (let i = 0; i < steps.length; i++) {
            if ((i + 1) > this.props.maxStep) {
                steps[i].setAttribute('title', "Please finish current step before moving ahead.");
            } else {
                steps[i].removeAttribute('title');
            }
        }
    }

    render(){
        return (
            <div className="survey-progress-bar">
                <span
                    style={this.handleLinkStyle(1)}
                    className={`progress-bar-step ${this.props.step >= 1 ? 'progress-bar-step_active' : ''}`}
                    onClick={() => this.handleStepClick(1)}>
                    General Info
                </span>
                <span className={this.props.step === 1 ? 'progress-bar-step_active' : ''}>></span>
                <span
                    style={this.handleLinkStyle(2)}
                    className={`progress-bar-step ${this.props.step >= 2 ? 'progress-bar-step_active' : ''}`}
                    onClick={() => this.handleStepClick(2)}>
                    Tenant Info
                </span>
                <span className={this.props.step === 2 ? 'progress-bar-step_active' : ''}>></span>
                <span
                    style={this.handleLinkStyle(3)}
                    className={`progress-bar-step ${this.props.step >= 3 ? 'progress-bar-step_active' : ''}`}
                    onClick={() => this.handleStepClick(3)}>
                    Amenities
                </span>
                <span className={this.props.step === 3 ? 'progress-bar-step_active' : ''}>></span>
                <span
                    style={this.handleLinkStyle(4)}
                    className={`progress-bar-step ${this.props.step >= 4 ? 'progress-bar-step_active' : ''}`}
                    onClick={() => this.handleStepClick(4)}>
                    Details
                </span>
            </div>
        );
    }
}
