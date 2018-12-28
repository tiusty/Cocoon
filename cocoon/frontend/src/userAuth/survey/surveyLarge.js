// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import './surveyLarge.css'
import closingIcon from './closing.png'
import HomeTile from "../../common/homeTile/homeTile";

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// Import Pop-up button components
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css'


export default class SurveyLarge extends Component {
    state = {
        curr_favorites: this.props.favorites
    };

    componentDidUpdate = (prevProps, prevState, snapshot) => {
        if(this.props.favorites !== prevProps.favorites) {
            this.setState({curr_favorites: this.props.favorites})
        }
    }

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

    renderFavorites() {
        /**
         * Renders the favorite homes
         */
        if (this.props.favorites.length === 0) return <h3 className="survey-large-no-homes">Go favorite some homes!</h3>
        return (
            <div>
                {this.props.favorites.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={this.inFavorites(home)}
                        visit={this.state.visit_list.filter(c => c.id === home.id).length >0}
                        onVisitClick={this.handleVisitClick}
                        onFavoriteClick={this.handleFavoriteClick}
                        show_heart={true}
                        show_score={false}
                        show_visit={true}
                    />
                )}
            </div>
        );
    };

    renderVisitList() {
        /**
         * Renders the visit list homes
         */
        if (this.props.visit_list.length === 0) return <h3 className="survey-large-no-homes">Please add homes to your visit list!</h3>;
        return (
            <div>
                {this.props.visit_list.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={this.inFavorites(home)}
                        visit={this.inVisitList(home)}
                        onVisitClick={this.handleVisitClick}
                        onFavoriteClick={this.handleFavoriteClick}
                        show_score={false}
                        show_heart={true}
                        show_visit={true}
                    />
                )}
            </div>
        );
    };

    inFavorites(home) {
        /**
         * Tests whether a particular home is currently favorited
         */
        // Checks to see if the home exists within the favorites list
        return this.state.curr_favorites.filter(c => c.id === home.id).length > 0;
    }

    inVisitList(home) {
        /**
         * Tests if a particular home is currently in the visit list
         */
        // Checks to see if the home exists within the visit_list
        return this.props.visit_list.filter(c => c.id === home.id).length >0;
    }

    render() {
        return (
            <div className="survey-large-div">
                <div className="survey-large-header">
                    <img onClick={() => this.props.onLargeSurveyClose()} className="survey-large-icon" src={closingIcon} alt="Closing icon"/>
                    <p className="survey-large-title">{this.props.name}</p>
                    <button onClick={this.handleDelete} className="btn btn-danger btn-sm m-2 survey-large-delete-button">Delete</button>
                </div>
                <div className="survey-large-info-div">
                    <div  className="survey-large-snapshot">
                        <p className="survey-large-snapshot-title">Survey Snapshot</p>
                        <p className="survey-large-snapshot-price">Desired price: $2000</p>
                        <p className="survey-large-snapshot-bedrooms">Number of bedrooms: 2</p>
                    </div>
                    <div className="survey-large-tour-summary">
                        <p className="survey-large-tour-summary-title">Tour Summary</p>
                        <p className="survey-large-tour-summary-estimate-duration">Estimated duration: 1 hour 5 minutes</p>
                        <p className="survey-large-tour-summary-message">You are ready to schedule!</p>
                        <button name="submit-button" disabled={!this.props.pre_tour_signed}
                            className="btn btn-success btn-sm m-2 survey-large-tour-summary-button"
                            value={this.props.id} type="submit">Schedule!</button>
                    </div>
                </div>
                <div className="survey-large-homes-div">
                    <div className="survey-large-favorites-div">
                        <p className='survey-large-favorites-title'>Favorite Home</p>
                        {this.renderFavorites()}
                    </div>
                    <div className="survey-large-visit-list-div">
                        <p className='survey-large-favorites-title'>Visit List</p>
                        {this.renderVisitList()}
                    </div>
                </div>
            </div>
        );
    }
}
