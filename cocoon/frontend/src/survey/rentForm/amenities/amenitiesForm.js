import React from 'react';
import { Component } from 'react';

export default class AmenitiesForm extends Component {

    renderLaundryQuestion() {
        return(
            <div className="survey-question" onChange={(e) => this.props.onInputChange(e, 'boolean')}>
                <h2>How do you like <span>your laundry</span>? <span className="checkbox-helper-text">(Select all that apply)</span></h2>
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
            </div>
        );
    }

    renderLaundryInUnitFollowUp() {
        if (this.props.amenitiesInfo.wants_laundry_in_unit) {
            return (
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you want your <span>laundry in unit</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="laundry_in_unit_weight" value="1" checked={this.props.amenitiesInfo.laundry_in_unit_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="laundry_in_unit_weight" value="2" checked={this.props.amenitiesInfo.laundry_in_unit_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="laundry_in_unit_weight" value="3" checked={this.props.amenitiesInfo.laundry_in_unit_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderLaundryInBuldingFollowUp() {
        if (this.props.amenitiesInfo.wants_laundry_in_building) {
            return (
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you want your <span>laundry in your building</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="laundry_in_building_weight" value="1" checked={this.props.amenitiesInfo.laundry_in_building_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="laundry_in_building_weight" value="2" checked={this.props.amenitiesInfo.laundry_in_building_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="laundry_in_building_weight" value="3" checked={this.props.amenitiesInfo.laundry_in_building_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderLaundryNearbyFollowUp() {
        if (this.props.amenitiesInfo.wants_laundry_nearby) {
            return (
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you want your <span>laundry nearby</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="laundry_nearby_weight" value="1" checked={this.props.amenitiesInfo.laundry_nearby_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="laundry_nearby_weight" value="2" checked={this.props.amenitiesInfo.laundry_nearby_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="laundry_nearby_weight" value="3" checked={this.props.amenitiesInfo.laundry_nearby_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderAmenitiesQuestions() {
        return (
            <div className="survey-question">
                <h2>Which of the following <span>amenities</span> do you want? <span className="checkbox-helper-text">(Select all that apply)</span></h2>
                {/*<label className="col-md-6 survey-label survey-checkbox">*/}
                    {/*<input type="checkbox" name="wants_parking" value="wantsParking"*/}
                           {/*onChange={(e) => this.props.onInputChange(e, 'boolean')} checked={this.props.amenitiesInfo.wants_parking}/>*/}
                    {/*<div>Parking spot <i className="material-icons">check</i></div>*/}
                {/*</label>*/}
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="wants_furnished" value="wantsFurnished"
                           onChange={(e) => this.props.onInputChange(e, 'boolean')} checked={this.props.amenitiesInfo.wants_furnished}/>
                    <div>Furnished <i className="material-icons">check</i></div>
                </label>
                {/*<label className="col-md-6 survey-label survey-checkbox">*/}
                    {/*<input type="checkbox" name="wants_dogs" value="wantsDogs" onChange={(e) => this.props.onInputChange(e, 'boolean')}*/}
                           {/*checked={this.props.amenitiesInfo.wants_dogs}/>*/}
                    {/*<div>Dogs welcome <i className="material-icons">check</i></div>*/}
                {/*</label>*/}
                {/*<label className="col-md-6 survey-label survey-checkbox">*/}
                    {/*<input type="checkbox" name="wants_cats" value="wantsCats" onChange={(e) => this.props.onInputChange(e, 'boolean')}*/}
                           {/*checked={this.props.amenitiesInfo.wants_cats}/>*/}
                    {/*<div>Cats welcome <i className="material-icons">check</i></div>*/}
                {/*</label>*/}
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

    renderCatFollowUp() {
        if (this.props.amenitiesInfo.wants_cats) {
            return (
                <div className="survey-question"
                     onChange={(e) => {
                         this.props.onInputChange(e, 'number');
                     }}>
                    <h2>How badly do you want <span>cats</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="cat_weight" value="1" checked={this.props.amenitiesInfo.cat_weight === 1} onChange={() => {
                        }}/>
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="cat_weight" value="2" checked={this.props.amenitiesInfo.cat_weight === 2} onChange={() => {
                        }}/>
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="cat_weight" value="3" checked={this.props.amenitiesInfo.cat_weight === 3} onChange={() => {
                        }}/>
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderHardwoodFloorFollowUp() {
        if (this.props.amenitiesInfo.wants_hardwood_floors) {
            return (
                <div className="survey-question"
                     onChange={(e) => this.props.onInputChange(e, 'number')}>
                    <h2>How badly do you want <span>hardwood floors</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="hardwood_floors_weight" value="1"
                               checked={this.props.amenitiesInfo.hardwood_floors_weight === 1} onChange={() => {
                        }}/>
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="hardwood_floors_weight" value="2"
                               checked={this.props.amenitiesInfo.hardwood_floors_weight === 2} onChange={() => {
                        }}/>
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="hardwood_floors_weight" value="3"
                               checked={this.props.amenitiesInfo.hardwood_floors_weight === 3} onChange={() => {
                        }}/>
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderACFollowup() {
        if (this.props.amenitiesInfo.wants_AC) {
            return (
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you want <span>air conditioning</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="AC_weight" value="1" checked={this.props.amenitiesInfo.AC_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="AC_weight" value="2" checked={this.props.amenitiesInfo.AC_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="AC_weight" value="3" checked={this.props.amenitiesInfo.AC_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderDishwasherFollowup() {
        if(this.props.amenitiesInfo.wants_dishwasher) {
            return (
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>dishwasher</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="dishwasher_weight" value="1" checked={this.props.amenitiesInfo.dishwasher_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="dishwasher_weight" value="2" checked={this.props.amenitiesInfo.dishwasher_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="dishwasher_weight" value="3" checked={this.props.amenitiesInfo.dishwasher_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderPatioFollowup() {
        if(this.props.amenitiesInfo.wants_patio) {
            return(
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>patio/balcony</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="patio_weight" value="1" checked={this.props.amenitiesInfo.patio_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="patio_weight" value="2" checked={this.props.amenitiesInfo.patio_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="patio_weight" value="3" checked={this.props.amenitiesInfo.patio_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderPoolFollowup() {
        if(this.props.amenitiesInfo.wants_pool) {
            return(
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>pool/hot tub</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="pool_weight" value="1" checked={this.props.amenitiesInfo.pool_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="pool_weight" value="2" checked={this.props.amenitiesInfo.pool_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="pool_weight" value="3" checked={this.props.amenitiesInfo.pool_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderGymFollowup() {
        if(this.props.amenitiesInfo.wants_gym) {
            return (
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>gym</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="gym_weight" value="1" checked={this.props.amenitiesInfo.gym_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="gym_weight" value="2" checked={this.props.amenitiesInfo.gym_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="gym_weight" value="3" checked={this.props.amenitiesInfo.gym_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    renderStorageUnit() {
        if(this.props.amenitiesInfo.wants_storage) {
            return (
                <div className="survey-question" onChange={(e) => {this.props.onInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>storage unit</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="storage_weight" value="1" checked={this.props.amenitiesInfo.storage_weight === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="storage_weight" value="2" checked={this.props.amenitiesInfo.storage_weight === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="storage_weight" value="3" checked={this.props.amenitiesInfo.storage_weight === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>
            );
        } else {
            return null
        }
    }

    render() {
        return(
            <>
                {this.renderLaundryQuestion()}
                {this.renderLaundryInUnitFollowUp()}
                {this.renderLaundryInBuldingFollowUp()}
                {this.renderAmenitiesQuestions()}
                {this.renderParkingFollowUp()}
                {this.renderFurnishedFollowUp()}
                {this.renderDogFollowup()}
                {this.renderCatFollowUp()}
                {this.renderHardwoodFloorFollowUp()}
                {this.renderACFollowup()}
                {this.renderDishwasherFollowup()}
                {this.renderPatioFollowup()}
                {this.renderPoolFollowup()}
                {this.renderGymFollowup()}
                {this.renderStorageUnit()}

                <div className="row survey-btn-wrapper">
                    <div className="col-xs-6">
                        <button className="col-sm-12 survey-btn survey-btn_back" style={{marginTop: '30px'}} onClick={(e) => this.props.handlePrevStep(e)}>
                            Back
                        </button>
                    </div>
                    <div className="col-xs-6">
                        <button className="col-sm-12 survey-btn" onClick={(e) => this.props.handleNextStep(e) }>
                            Next
                        </button>
                    </div>
                </div>
            </>
        );
    }
}
