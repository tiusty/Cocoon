// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveys.css'
import SurveySmall from "./surveySmall";

export default class Surveys extends Component {

    state = {
        loading_click: true,
    };

    renderPage() {
        if(this.state.loading_clicked) {
            return <p> Loading page </p>
        } else {
            return (
                <div className="row surveys">
                    <div className="col-md-3 survey">
                        <SurveySmall
                            onLoadingClicked={this.setLoadingClick}
                        />
                    </div>
                    <div className="col-md-3 survey">
                        <SurveySmall
                            onLoadingClicked={this.setLoadingClick}
                        />
                    </div>
                    <div className="col-md-3 survey">
                        <SurveySmall
                            onLoadingClicked={this.setLoadingClick}
                        />
                    </div>
                </div>
            );
        }
    }

    setLoadingClick = () => {
        this.setState({loading_clicked: true})
    }


    render() {
        return (
            <>
                <div className="row">
                    <div className="col-md-6 col-md-offset-3">
                        <p className="my-survey-header">Roommate Groups</p>
                    </div>
                    <div className="col-md-1 col-md-offset-2">
                        <button className="btn btn-primary help-button">Help</button>
                    </div>
                </div>

                <div className="row">
                    <div className="col-md-6 col-md-offset-2 search-bar-div">
                        <input type="text" className="input search-bar" placeholder="Search..." />
                        <button className="btn btn-primary search-button">Search</button>
                    </div>
                </div>

                {this.renderPage()}
            </>
        );
    }
}
