import React from 'react';
import { Component, Fragment } from 'react';

export default class Amenities extends Component {

    constructor(props) {
        super(props);
        this.state = {
            wantsParking: false,
            wantsFurnished: false,
            wantsDogs: false,
            wantsCats: false,
            wantsHardwood: false,
            wantsAC: false,
            wantsDishWasher: false,
            wantsPatio: false,
            wantsPool: false,
            wantsGym: false,
            wantsStorage: false
        }
    }

    componentDidMount = () => {
        if(this.props.allAmenitiesInfo) {
            this.setState(this.props.allAmenitiesInfo)
        }
    }

    handleCheckbox = (e) => {
        const { name, value } = e.target;
        this.setState({
            [value]: !this.state[value]
        }, () => this.setSurveyState(name, this.state[value]));
    }

    handleLaundry = (e) => {
        if(e.target.checked) {
            this.setState({
                [e.target.name]: true
            })
        } else {
            this.setState({
                [e.target.name]: false
            })
        }
    }

    handleInputChange = (e, type) => {
        const { name, value } = e.target;
        if(type === 'number') {
            this.setState({
                [name]: parseInt(value)
            });
        } else {
            this.setState({
                [name]: value
            });
        }
    }

    setSurveyState = (state, value) => {
        this.setState({
            [state]: value
        })
    }

    render(){
        let number_of_dogs = 1;
        if(this.state.wantsDogs) {
            number_of_dogs = document.querySelector('input[name=number_of_dogs').value;
        }
        return (
            <>
                <div className="survey-question" onChange={this.handleLaundry}>
                    <h2>How do you like <span>your laundry</span>?</h2>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="laundry_in_unit" value="true" checked={this.state.laundry_in_unit && this.state.laundry_in_unit === true} onChange={() => {}} />
                        <div>In-unit <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="laundry_in_building" value="true" checked={this.state.laundry_in_building && this.state.laundry_in_building === true} onChange={() => {}} />
                        <div>In-building <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="laundry_nearby_laundromat" value="true" checked={this.state.laundry_nearby_laundromat && this.state.laundry_nearby_laundromat === true} onChange={() => {}} />
                        <div>Nearby laundromat <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="laundry_no_preference" value="true" checked={this.state.laundry_no_preference && this.state.laundry_no_preference === true} onChange={() => {}} />
                        <div>Don't care <i className="material-icons">check</i></div>
                    </label>
                </div>

                <div className="survey-question">
                    <h2>Which of the following <span>amenities</span> do you want?</h2>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_parking" value="wantsParking" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsParking} />
                        <div>Parking spot <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_furnished" value="wantsFurnished" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsFurnished} />
                        <div>Furnished <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_dogs" value="wantsDogs" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsDogs} />
                        <div>Dogs welcome <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_cats" value="wantsCats" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsCats} />
                        <div>Cats welcome <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_hardwood_floors" value="wantsHardwood" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsHardwood} />
                        <div>Hardwood floors <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_ac" value="wantsAC" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsAC} />
                        <div>Air conditioning <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_dishwasher" value="wantsDishWasher" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsDishWasher} />
                        <div>Dishwasher <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_patio" value="wantsPatio" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsPatio} />
                        <div>Patio/Balcony <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_pool" value="wantsPool" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsPool} />
                        <div>Pool/Hot tub <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_gym" value="wantsGym" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsGym} />
                        <div>Gym in building <i className="material-icons">check</i></div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="checkbox" name="wants_storage" value="wantsStorage" onChange={(e) => this.handleCheckbox(e)} checked={this.state.wantsStorage} />
                        <div>Storage unit in building <i className="material-icons">check</i></div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS PARKING*/}
                <div className="survey-question" style={{display: `${this.state.wantsParking ? 'block' : 'none'}`}} >
                    <h2>How many <span>cars</span> do you have?</h2>
                    <input className="col-md-12 survey-input" type="number" name="number_of_cars" placeholder="Number of cars" value={this.state.number_of_cars || ''} onChange={(e) => {this.handleInputChange(e, 'number');}}/>
                </div>

                <div className="survey-question" style={{display: `${this.state.wantsParking ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you need <span>off street parking</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="parking_spot" value="1" checked={this.state.parking_spot === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="parking_spot" value="2" checked={this.state.parking_spot === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="parking_spot" value="3" checked={this.state.parking_spot === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS FURNISHED*/}
                <div className="survey-question" style={{display: `${this.state.wantsFurnished ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you need it to be <span>furnished</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="furnished" value="1" checked={this.state.furnished === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="furnished" value="2" checked={this.state.furnished === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="furnished" value="3" checked={this.state.furnished === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS DOGS*/}
                <div className="survey-question" style={{display: `${this.state.wantsDogs ? 'block' : 'none'}`}}>
                    <h2>How many <span>dogs</span>?</h2>
                    <input className="col-md-12 survey-input" type="number" name="number_of_dogs" placeholder="Number of dogs" value={this.state.number_of_dogs || ''} onChange={(e) => {this.handleInputChange(e, 'number');}}/>
                </div>

                <div className="survey-question" style={{display: `${this.state.wantsDogs ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'string');}}>
                    <h2>{number_of_dogs > 1 ? 'Are the dogs registered service dogs' : 'Is the dog a registered service dog'}?</h2>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="radio" name="service_dogs" value="yes" checked={this.state.service_dogs === 'yes'} onChange={() => {}} />
                        <div>Yes</div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="radio" name="service_dogs" value="no" checked={this.state.service_dogs === 'no'} onChange={() => {}} />
                        <div>No</div>
                    </label>
                </div>

                <div className="survey-question" style={{display: `${this.state.wantsDogs ? 'block' : 'none'}`}}>
                    <h2>What <span>{number_of_dogs > 1 ? 'breeds' : 'breed'}</span>?</h2>
                    <input className="col-md-12 survey-input" type="text" name="breed_of_dogs" placeholder={`Enter breed of ${number_of_dogs > 1 ? 'dogs' : 'dog'}`} value={this.state.breed_of_dogs || ''} onChange={(e) => {this.handleInputChange(e, 'string');}}/>
                </div>

                <div className="survey-question" style={{display: `${this.state.wantsDogs ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'string');}}>
                    <h2>Does your {number_of_dogs > 1 ? 'dogs' : 'dog'} <span>weigh more or less than 25 lbs</span>?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="dog_size" value="more-than-25" checked={this.state.dog_size === 'more-than-25'} onChange={() => {}} />
                        <div>More than</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="dog_size" value="less-than-25" checked={this.state.dog_size === 'less-than-25'} onChange={() => {}} />
                        <div>Less than</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS CATS*/}
                <div className="survey-question" style={{display: `${this.state.wantsCats ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want <span>cats</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="cats" value="1" checked={this.state.cats === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="cats" value="2" checked={this.state.cats === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="cats" value="3" checked={this.state.cats === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS HARDWOOD FLOORS*/}
                <div className="survey-question" style={{display: `${this.state.wantsHardwood ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want <span>hardwood floors</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="hardwood_floors" value="1" checked={this.state.hardwood_floors === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="hardwood_floors" value="2" checked={this.state.hardwood_floors === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="hardwood_floors" value="3" checked={this.state.hardwood_floors === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS AC*/}
                <div className="survey-question" style={{display: `${this.state.wantsAC ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want <span>air conditioning</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="air_condition" value="1" checked={this.state.air_condition === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="air_condition" value="2" checked={this.state.air_condition === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="air_condition" value="3" checked={this.state.air_condition === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS DISHWASHER*/}
                <div className="survey-question" style={{display: `${this.state.wantsDishWasher ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>dishwasher</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="dishwasher" value="1" checked={this.state.dishwasher === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="dishwasher" value="2" checked={this.state.dishwasher === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="dishwasher" value="3" checked={this.state.dishwasher === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS PATIO*/}
                <div className="survey-question" style={{display: `${this.state.wantsPatio ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>patio/balcony</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="patio" value="1" checked={this.state.patio === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="patio" value="2" checked={this.state.patio === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="patio" value="3" checked={this.state.patio === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS POOL*/}
                <div className="survey-question" style={{display: `${this.state.wantsPool ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>pool/hot tub</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="pool" value="1" checked={this.state.pool === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="pool" value="2" checked={this.state.pool === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="pool" value="3" checked={this.state.pool === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS GYM*/}
                <div className="survey-question" style={{display: `${this.state.wantsGym ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>gym</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="gym" value="1" checked={this.state.gym === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="gym" value="2" checked={this.state.gym === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="gym" value="3" checked={this.state.gym === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS STORAGE UNIT*/}
                <div className="survey-question" style={{display: `${this.state.wantsStorage ? 'block' : 'none'}`}} onChange={(e) => {this.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>storage unit</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="storage_unit" value="1" checked={this.state.storage_unit === 1} onChange={() => {}} />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="storage_unit" value="2" checked={this.state.storage_unit === 2} onChange={() => {}} />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="storage_unit" value="3" checked={this.state.storage_unit === 3} onChange={() => {}} />
                        <div>Need it</div>
                    </label>
                </div>

                <div className="row survey-btn-wrapper">
                    <div className="col-sm-6 col-xs-12">
                        <button className="col-sm-12 survey-btn survey-btn_back" style={{marginTop: '30px'}} onClick={(e) => { ( this.props.saveAmenitiesInfo(this.state), this.props.handlePrevStep(e))}}>
                            Back
                        </button>
                    </div>
                    <div className="col-sm-6 col-xs-12">
                        <button className="col-sm-12 survey-btn" onClick={(e) => { this.props.saveAmenitiesInfo(this.state); this.props.handleNextStep(e) }}>
                            Next
                        </button>
                    </div>
                </div>

            </>
        );
    }
}
