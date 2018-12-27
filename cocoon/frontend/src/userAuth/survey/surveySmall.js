// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveySmall.css'

export default class SurveySmall extends Component {
    state = {
        name: "",
        url: "",
    };
    render() {
        return (
            <>
                <div className="survey-div">
                    <div className="survey-box">

                    </div>
                </div>
            </>
        );
    }
}