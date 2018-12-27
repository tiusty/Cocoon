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

    render() {
        return (
            <div className="survey-large-div">
                <img className="survey-large-icon" src={closingIcon} alt="Closing icon"/>
                <p className="survey-large-title">{this.props.name}</p>
                <button onClick={this.handleDelete} className="btn btn-danger btn-sm m-2 survey-large-delete-button">Delete</button>
            </div>
        );
    }
}
