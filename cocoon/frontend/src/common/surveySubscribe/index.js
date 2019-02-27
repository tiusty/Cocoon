import React, { Component } from 'react';
import './surveySubscribe.css';

export default class SurveySubscribe extends Component {

    state = {
        is_subscribed: false
    }

    toggleSubscribe = () => {
        this.setState({
            is_subscribed: !this.state.is_subscribed
        })
    }

    renderCheckbox = () => {
        let checkbox = 'check_box_outline_blank';
        if (this.state.is_subscribed) {
            checkbox = 'check_box';
        }
        return checkbox;
    }

    renderOptions = () => {
        if (this.state.is_subscribed) {
            return (
                <div className="subscribe-options">
                    Send me an email when
                    <input type="number" defaultValue={50} />
                    homes have a score of at least
                    <input type="number" defaultValue={70} />
                </div>
            );
        }
    }

    render() {
        return (
            <div className="subscribe-wrapper">
                    <div className="subscribe-checkbox" onClick={this.toggleSubscribe}>
                        <i className="material-icons">{this.renderCheckbox()}</i>
                        I want to stay updated with this survey!
                    </div>
                    {this.renderOptions()}
                </div>
        );
    }
}