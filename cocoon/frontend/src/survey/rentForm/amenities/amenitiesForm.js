import React from 'react';
import { Component } from 'react';

export default class AmenitiesForm extends Component {

    renderLaundryQuestion() {
        return(
            <div className="survey-question" onChange={(e) => this.props.onInputChange(e, 'boolean')}>
                <h2>How do you like <span>your laundry</span>?</h2>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_laundry_in_unit" value="true"
                           checked={this.props.amenitiesInfo.wants_laundry_in_unit === true}
                           onChange={() => {
                           }}/>
                    <div>In-unit <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_laundry_in_building" value="true"
                           checked={this.props.amenitiesInfo.wants_laundry_in_building === true}
                           onChange={() => {
                           }}/>
                    <div>In-building <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_laundry_nearby" value="true"
                           checked={this.props.amenitiesInfo.wants_laundry_nearby === true}
                           onChange={() => {
                           }}/>
                    <div>Nearby laundromat <i className="material-icons">check</i></div>
                </label>
            </div>
        );
    }

    renderAmenitiesQuestions() {
        return (
            <div className="survey-question">
                <h2>Which of the following <span>amenities</span> do you want?</h2>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_parking" value="wantsParking"
                           onChange={(e) => this.props.onInputChange(e, 'boolean')} checked={this.props.amenitiesInfo.wants_parking}/>
                    <div>Parking spot <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_furnished" value="wantsFurnished"
                           onChange={(e) => this.props.onInputChange(e, 'boolean')} checked={this.props.amenitiesInfo.wants_furnished}/>
                    <div>Furnished <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_dogs" value="wantsDogs" onChange={(e) => this.props.onInputChange(e, 'boolean')}
                           checked={this.props.amenitiesInfo.wants_dogs}/>
                    <div>Dogs welcome <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_cats" value="wantsCats" onChange={(e) => this.props.onInputChange(e, 'boolean')}
                           checked={this.props.amenitiesInfo.wants_cats}/>
                    <div>Cats welcome <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_hardwood_floors" value="wantsHardwood"
                           onChange={(e) => this.props.onInputChange(e, 'boolean')} checked={this.props.amenitiesInfo.wants_hardwood_floors}/>
                    <div>Hardwood floors <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_AC" value="wantsAC" onChange={(e) => this.props.onInputChange(e, 'boolean')}
                           checked={this.props.amenitiesInfo.wants_AC}/>
                    <div>Air conditioning <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_dishwasher" value="wantsDishWasher"
                           onChange={(e) => this.props.onInputChange(e, 'boolean')} checked={this.props.amenitiesInfo.wants_dishwasher}/>
                    <div>Dishwasher <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_patio" value="wantsPatio"
                           onChange={(e) => this.props.onInputChange(e, 'boolean')} checked={this.props.amenitiesInfo.wants_patio}/>
                    <div>Patio/Balcony <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_pool" value="wantsPool" onChange={(e) => this.props.onInputChange(e, 'boolean')}
                           checked={this.props.amenitiesInfo.wants_pool}/>
                    <div>Pool/Hot tub <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_gym" value="wantsGym" onChange={(e) => this.props.onInputChange(e, 'boolean')}
                           checked={this.props.amenitiesInfo.wants_gym}/>
                    <div>Gym in building <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_storage" value="wantsStorage"
                           onChange={(e) => this.props.onInputChange(e, 'boolean')} checked={this.props.amenitiesInfo.wants_storage}/>
                    <div>Storage unit in building <i className="material-icons">check</i></div>
                </label>
            </div>
        );
    }

    renderParkingFollowUp() {
        if (this.props.amenitiesInfo.wants_parking) {
            return (
                <div className="survey-question">
                    <h3>How many <span>cars</span> do you have?</h3>
                    <input className="col-md-12 survey-input" type="number" name="number_of_cars"
                           placeholder="Number of cars"
                           value={this.props.amenitiesInfo.number_of_cars !== 0 ? this.props.amenitiesInfo.number_of_cars : ''} onChange={(e) => {
                        this.props.onInputChange(e, 'number');
                    }}/>
                </div>
            );
        } else {
            return null
        }
    }

    renderFurnishedFollowUp() {
        if (this.props.amenitiesInfo.wants_furnished) {
            return (
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you need it to be <span>furnished</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="furnished_weight" value="1" checked={this.props.amenitiesInfo.furnished_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="furnished_weight" value="2" checked={this.props.amenitiesInfo.furnished_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="furnished_weight" value="3" checked={this.props.amenitiesInfo.furnished_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderDogFollowup() {
        if(this.props.amenitiesInfo.wants_dogs) {
            return (
                <>
                    <div className="survey-question">
                        <h2>How many <span>dogs</span>?</h2>
                        <input className="col-md-12 survey-input" type="number" name="number_of_dogs"
                               placeholder="Number of dogs"
                               value={this.props.amenitiesInfo.number_of_dogs !== 0 ? this.props.amenitiesInfo.number_of_dogs : ''}
                               onChange={(e) => {
                                   this.props.onInputChange(e, 'number');
                               }}/>
                    </div>

                    <div className="survey-question"
                         onChange={(e) => {
                             this.props.onInputChange(e, 'boolean');
                         }}>
                        <h2>{this.props.amenitiesInfo.number_of_dogs > 1 ? 'Are the dogs registered service dogs' : 'Is the dog a registered service dog'}?</h2>
                        <label className="col-md-6 survey-label survey-checkbox">
                            <input type="radio" name="service_dogs" value="yes"
                                   checked={this.props.amenitiesInfo.service_dogs === true} onChange={() => {
                            }}/>
                            <div>Yes</div>
                        </label>
                        <label className="col-md-6 survey-label survey-checkbox">
                            <input type="radio" name="service_dogs" value="no"
                                   checked={this.props.amenitiesInfo.service_dogs === false} onChange={() => {
                            }}/>
                            <div>No</div>
                        </label>
                    </div>

                    <div className="survey-question">
                        <h2>What <span>{this.props.amenitiesInfo.number_of_dogs > 1 ? 'breeds' : 'breed'}</span>?</h2>
                        <input className="col-md-12 survey-input" type="text" name="breed_of_dogs"
                               placeholder={`Enter breed of ${this.props.amenitiesInfo.number_of_dogs > 1 ? 'dogs' : 'dog'}`}
                               value={this.props.amenitiesInfo.breed_of_dogs || ''} onChange={(e) => {
                            this.props.onInputChange(e, 'string');
                        }}/>
                    </div>

                    <div className="survey-question"
                         onChange={(e) => {
                             this.props.onInputChange(e, 'string');
                         }}>
                        <h2>Does your {this.props.amenitiesInfo.number_of_dogs > 1 ? 'dogs' : 'dog'} <span>weigh more or less than 25 lbs</span>?
                        </h2>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name="dog_size" value="more-than-25"
                                   checked={this.props.amenitiesInfo.dog_size === 'more-than-25'} onChange={() => {
                            }}/>
                            <div>More than</div>
                        </label>
                        <label className="col-md-6 survey-label">
                            <input type="radio" name="dog_size" value="less-than-25"
                                   checked={this.props.amenitiesInfo.dog_size === 'less-than-25'} onChange={() => {
                            }}/>
                            <div>Less than</div>
                        </label>
                    </div>
                </>
            );
        } else {
            return null
        }
    }

    render() {
        return(
            <>
                {this.renderLaundryQuestion()}
                {this.renderAmenitiesQuestions()}
                {this.renderParkingFollowUp()}
                {this.renderFurnishedFollowUp()}
                {this.renderDogFollowup()}
            </>
        );
    }
}
