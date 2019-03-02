import React, { Component } from 'react';
import PropTypes from 'prop-types';
import './cocoonModal.css';

export default class CocoonModal extends Component {

    static defaultProps = {
        confirmText: 'Confirm',
        closeModalText: 'Go Back'
    }

    componentDidMount() {
        document.querySelector('body').style.position = 'relative';
        document.querySelector('#siteWrapper').style.display = 'none';
    }

    componentWillUnmount() {
        document.querySelector('body').style.position = 'static';
        document.querySelector('#siteWrapper').style.display = 'block';
    }

    render() {
        return (
            <div className="cocoon-modal-wrapper">
                <div className="cocoon-modal-container">
                    <h1>{this.props.headline}</h1>
                    <p>{this.props.subHeadline}</p>
                    <div className="modal-button-wrapper">
                        <button onClick={this.props.closeModalOnClick} className="modal-button modal-button_close">{this.props.closeModalText}</button>
                        <button onClick={this.props.confirmOnClick} className="modal-button modal-button_confirm">{this.props.confirmText}</button>
                    </div>
                </div>
            </div>
        );
    }
}

CocoonModal.propTypes = {
    headline: PropTypes.string.isRequired,
    subHeadline: PropTypes.any.isRequired,
    data: PropTypes.any,
    confirmText: PropTypes.string,
    confirmOnClick: PropTypes.func.isRequired,
    closeModalText: PropTypes.string,
    closeModalOnClick: PropTypes.func.isRequired,
}