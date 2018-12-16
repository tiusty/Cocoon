import React from 'react';
import { Component, Fragment } from 'react';

export default class AmenitiesForm extends Component {

    renderLaundryQuestion() {
        return(
            <div className="survey-question" onChange={(e) => this.props.onInputChange(e, 'boolean')}>
                <h2>How do you like <span>your laundry</span>?</h2>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wantsLaundryInUnit" value="true"
                           checked={this.props.amenitiesInfo.wantsLaundryInUnit === true}
                           onChange={() => {
                           }}/>
                    <div>In-unit <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wantsLaundryInBuilding" value="true"
                           checked={this.props.amenitiesInfo.wantsLaundryInBuilding === true}
                           onChange={() => {
                           }}/>
                    <div>In-building <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wantsLaundryNearby" value="true"
                           checked={this.props.amenitiesInfo.wantsLaundryNearby === true}
                           onChange={() => {
                           }}/>
                    <div>Nearby laundromat <i className="material-icons">check</i></div>
                </label>
            </div>
        );
    }

    render() {
        return(
            <>
                {this.renderLaundryQuestion()}
            </>
        );
    }
}
