// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveyLarge.css'
import closingIcon from './closing.png'

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// Import Pop-up button components
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css'


export default class SurveyLarge extends Component {

    handleDelete = () => {
        /**
         Opens a confirmation page first before the survey is deleted.
         If the user clicks yes then the survey gets deleted, if
         no then nothing happens
         */
        confirmAlert({
            title: 'Confirmation',
            message: "Are you sure you want to delete " + this.props.name + "?",
            buttons: [
                {
                    label: 'yes',
                    onClick: () => this.props.onDelete(this.props.id)
                },
                {
                    label: 'No',
                }
            ]
        })
    };

    generateLoadUrl() {
        return ''
    }

    render() {
        return (
            <div className="survey-large-div">
                <div className="survey-large-header">
                    <img className="survey-large-icon" src={closingIcon} alt="Closing icon"/>
                    <p className="survey-large-title">{this.props.name}</p>
                    <button onClick={this.handleDelete} className="btn btn-danger btn-sm m-2 survey-large-delete-button">Delete</button>
                </div>
                <div className="row survey-large-info-div">
                    <div  className="survey-large-snapshot">
                        <p className="survey-large-snapshot-title">Survey Snapshot</p>
                        <p className="survey-large-snapshot-price">Desired price: $2000</p>
                        <p className="survey-large-snapshot-bedrooms">Number of bedrooms: 2</p>
                    </div>
                    <div className="survey-large-gap"></div>
                    <div className="survey-large-tour-summary">
                        <p className="survey-large-tour-summary-title">Tour Summary</p>
                        <p className="survey-large-tour-summary-estimate-duration">Estimated duration: 1 hour 5 minutes</p>
                        <p className="survey-large-tour-summary-message">You are ready to schedule!</p>
                        <a  href={this.generateLoadUrl()}
                            className="btn btn-primary survey-large-tour-summary-button">Schedule</a>
                    </div>
                </div>
                <div className="row survey-large-homes-div">
                    <div className="col-md-4 col-md-offset-1 survey-large-favorites-div">
                        <p className='survey-large-favorites-title'>Favorite Home</p>
                    </div>
                    <div className="col-md-4 col-md-offset-2 survey-large-visit-list-div">
                        <p className='survey-large-favorites-title'>Visit List</p>
                    </div>
                </div>
            </div>
        );
    }
}
