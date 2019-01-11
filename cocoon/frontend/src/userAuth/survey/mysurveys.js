// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'

// Import styling
import './mysurveys.css'

export default class MySurveys extends Component {
    render() {
        return (
            <div className="row">
                <div className="col-md-8">
                    <div className="surveys-div">
                        <h2 className="surveys-title">My Surveys</h2>
                        <p className='surveys-title-text'>When you are ready please follow the steps on the right side of the screen to
                            sign your documents so you can schedule a tour</p>
                    </div>
                    <div className="surveys-main">
                        <p>hi</p>
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="tour-summary">
                    </div>
                </div>
            </div>
        );
    }
}