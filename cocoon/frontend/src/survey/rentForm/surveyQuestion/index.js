import React, { Component } from 'react';
import PropTypes from 'prop-types';

import './surveyQuestion.css';

export default class SurveyQuestion extends Component {

    /*
    * this.props.surveyQuestion(string) = Text to be used for Survey question
    * this.props.hasHelp(bool) = if true, renders help icon (?) after question
    * this.props.surveyQuestionHelpText(string) = Text to be used inside of help box
    *
    * this.state.viewingHelp(bool) = used to toggle the help box
    */

    state = {
        viewingHelp: false
    }

    static defaultProps = {
        hasHelp: false
    }

    toggleHelp = () => {
        this.setState({
            viewingHelp: !this.state.viewingHelp
        })
    }

    renderHelp = () => {
        if (this.props.hasHelp === true && this.state.viewingHelp === true) {
            return (
                <div className="help-box">
                    {this.props.surveyQuestionHelpText}
                </div>
            )
        } else {
            return null;
        }
    }

    helpStyle = () => {
        let style = {
            color: 'rgba(59, 72, 82, 0.5)'
        }
        if (this.state.viewingHelp) {
            style = {
                color: 'rgba(59, 72, 82, 0.75)'
            }
        }
        return style;
    }

    renderQuestion = () => {
        return {
            __html: this.props.surveyQuestion
        }
    }

    renderIcon = () => {
        if (this.props.hasHelp && this.props.surveyQuestionHelpText !== '') {
            return (
                <i
                    className="material-icons"
                    style={this.helpStyle()}
                    onClick={this.toggleHelp}>
                    help_outline
                </i>
            );
        } else {
            return null;
        }
    }

    render() {
        return (
            <>
                <div style={{margin: '20px 0 10px'}}>
                    <h2 dangerouslySetInnerHTML={this.renderQuestion()} style={{display: 'inline'}}></h2>
                    {this.renderIcon()}
                </div>
                {this.renderHelp()}
            </>
        );
    }

}

SurveyQuestion.propTypes = {
    surveyQuestion: PropTypes.string.isRequired,
    hasHelp: PropTypes.bool,
    surveyQuestionHelpText: PropTypes.string,
}