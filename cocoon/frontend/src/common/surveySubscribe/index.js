import React, { Component } from 'react';
import './surveySubscribe.css';
import PropTypes from "prop-types";

export default class SurveySubscribe extends Component {

    state = {
        is_subscribed: false,
        email_number_of_homes: 50,
        email_score_of_homes: 70
    }

    subscribe = () => {
        if (this.state.is_subscribed) {
            // subscribes to survey by this.props.survey_id
            console.log('subscribed!');
        } else {
            console.log('unsub?')
        }
    }

    toggleSubscribe = () => {
        this.setState({
            is_subscribed: !this.state.is_subscribed
        }, () => {
            this.subscribe();
        })
    }

    renderCheckbox = () => {
        let checkbox = 'check_box_outline_blank';
        if (this.state.is_subscribed) {
            checkbox = 'check_box';
        }
        return checkbox;
    }

    saveValue = (e) => {
        const { name, value } = e.target;
        this.setState({
            [name]: value
        })
    }

    renderOptions = () => {
        if (this.state.is_subscribed) {
            return (
                <div className="subscribe-options">
                    Send me an email when
                    <input type="number" value={this.state.email_number_of_homes} name="email_number_of_homes" onChange={this.saveValue} onBlur={this.subscribe} />
                    homes have a score of at least
                    <input type="number" value={this.state.email_score_of_homes} name="email_score_of_homes" onChange={this.saveValue} onBlur={this.subscribe} />
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

SurveySubscribe.propTypes = {
    id: PropTypes.number.isRequired
}