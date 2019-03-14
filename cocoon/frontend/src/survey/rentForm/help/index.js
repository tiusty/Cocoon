import React, { Component } from 'react';
import { findDOMNode } from 'react-dom';
import PropTypes from 'prop-types';
import './help.css';

export default class Help extends Component {

    /*
    * this.props.helpText(string) = Text to be used inside of help box
    */

    constructor(props) {
        super(props);
        this.state = {
            viewingHelp: false,
            targetElement: undefined
        }
    }

    componentDidMount() {
        let targetElement = findDOMNode(this).parentNode;
        this.setState({
            targetElement: targetElement
        })
    }

    componentDidUpdate(prevState) {
        if (this.state.viewingHelp !== prevState.viewingHelp) {
            this.toggleHelpBlock();
        }
    }

    toggleHelp = () => {
        this.setState({
            viewingHelp: !this.state.viewingHelp
        })
    }

    toggleHelpBlock = () => {
        if (this.state.targetElement && this.state.viewingHelp) {
            this.createHelpBlock();
        } else {
            this.removeHelpBlock();
        }
    }

    createHelpBlock = () => {
        const div = document.createElement("div");
        div.className = 'help-box';
        div.innerText = this.props.helpText;
        this.state.targetElement.parentNode.insertBefore(div, this.state.targetElement.nextSibling);
    }

    removeHelpBlock = () => {
        if (this.state.targetElement.parentNode.querySelector('.help-box')) {
            this.state.targetElement.parentNode.removeChild(this.state.targetElement.parentNode.querySelector('.help-box'));
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

    render() {
        return (
            <i
                className="material-icons"
                style={this.helpStyle()}
                onClick={this.toggleHelp}
            >
                help_outline
            </i>
        )
    }

}

Help.propTypes = {
    helpText: PropTypes.string.isRequired
};