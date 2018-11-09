import React from 'react';
import { Component, Fragment } from 'react';

export default class Amenities extends Component {
    render(){
        return (
            <>
                <div className="survey-question">
                    <h2>Amenity questions <span>here</span>?</h2>
                </div>
                <button className="col-md-12 survey-btn" onClick={this.props.handleNextStep}>
                    Next
                </button>
            </>
        );
    }
}
