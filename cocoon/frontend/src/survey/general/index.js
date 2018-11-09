import React from 'react';
import { Component, Fragment } from 'react';

export default class General extends Component {

    constructor(props) {
        super(props);
        this.state = {
            number_of_tenants: 1
        }
    }

    render(){
        return (
            <>
                <div className="survey-question">
                    <h2>How many people are you <span>searching with</span>?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="1" />
                        <div>Just Me</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="2" />
                        <div>Me + 1 other</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="3" />
                        <div>Me + 2 others</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="4" />
                            <div>Me + 3 others</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="5" />
                        <div>Me + 4 others</div>
                    </label>
                </div>
                <button className="col-md-12 survey-btn" onClick={this.props.handleNextStep}>
                    Next
                </button>
            </>
        );
    }
}
