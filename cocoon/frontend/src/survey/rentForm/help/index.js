import React, { Component } from 'react';
import PropTypes from 'prop-types';
import './help.css';

export default class Help extends Component {

    /*
    * this.props.helpElement(el) = The html element to toggle.
    *       Pass down using document.getElementById('el')
    *       i.e. <Help helpElement={document.getElementById('number_of_tenant_help')} />
    */

    constructor(props) {
        super(props);
        this.state = {
            viewingHelp: false
        }
    }

    componentDidUpdate(prevState) {
        if (this.state.viewingHelp !== prevState.viewingHelp) {
            this.toggleHelpDiv();
        }
    }

    toggleHelp = () => {
        this.setState({
            viewingHelp: !this.state.viewingHelp
        }, () => console.log('viewingHelp: ' + this.state.viewingHelp))
    }

    toggleHelpDiv = () => {
        if (this.props.helpElement && this.state.viewingHelp) {
            this.props.helpElement.style.display = 'block';
        } else {
            this.props.helpElement.style.display = 'none';
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
    helpElement: PropTypes.any.isRequired
};