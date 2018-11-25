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

    handleCheckbox = (e) => {
        const { name, value } = e.target;
        this.setState({
            [value]: !this.state[value]
        }, () => this.props.setSurveyState(name, this.state[value]));
    }

    render(){
        return (
            <>
                <div className="survey-question"onChange={(e) => {this.props.handleInputChange(e, 'string');}}>
                    <h2>How do you like <span>your laundry</span>?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="preferred_laundry" value="in-unit" />
                        <div>In-unit</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="preferred_laundry" value="in-building" />
                        <div>In-building</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="preferred_laundry" value="nearby" />
                        <div>Nearby laundromat</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="preferred_laundry" value="don't-care" />
                        <div>Don't care</div>
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
                <div className="survey-question" style={{display: `${this.state.wantsParking ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How many <span>cars</span> do you have?</h2>
                    <input className="col-md-12 survey-input" type="number" name="number_of_cars" placeholder="Number of cars" />
                </div>

                <div className="survey-question" style={{display: `${this.state.wantsParking ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How badly do you need <span>off street parking</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="parking_spot" value="1" />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="parking_spot" value="2" />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="parking_spot" value="3" />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS FURNISHED*/}
                <div className="survey-question" style={{display: `${this.state.wantsFurnished ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How badly do you need it to be <span>furnished</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="furnished" value="1" />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="furnished" value="2" />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="furnished" value="3" />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS DOGS*/}
                <div className="survey-question" style={{display: `${this.state.wantsDogs ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How many <span>dogs</span>?</h2>
                    <input className="col-md-12 survey-input" type="number" name="number_of_dogs" placeholder="Number of dogs" />
                </div>

                <div className="survey-question" style={{display: `${this.state.wantsDogs ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'string');}}>
                    <h2>Are the dog(s) <span>registered service dogs</span>?</h2>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="radio" name="service_dogs" value="true" />
                        <div>Yes</div>
                    </label>
                    <label className="col-md-6 survey-label survey-checkbox">
                        <input type="radio" name="service_dogs" value="false" />
                        <div>No</div>
                    </label>
                </div>

                <div className="survey-question" style={{display: `${this.state.wantsDogs ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'string');}}>
                    <h2>What <span>breed(s)</span>?</h2>
                    <input className="col-md-12 survey-input" type="text" name="breed_of_dogs" placeholder="Enter breed of dog(s)" />
                </div>

                <div className="survey-question" style={{display: `${this.state.wantsDogs ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'string');}}>
                    <h2>Does your dog(s) <span>weigh more or less than 25 lbs</span>?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="dog_size" value="more-than-25" />
                        <div>More than</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="dog_size" value="less-than-25" />
                        <div>Less than</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS HARDWOOD FLOORS*/}
                <div className="survey-question" style={{display: `${this.state.wantsHardwood ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want <span>hardwood floors</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="hardwood_floors" value="1" />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="hardwood_floors" value="2" />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="hardwood_floors" value="3" />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS AC*/}
                <div className="survey-question" style={{display: `${this.state.wantsAC ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want <span>air conditioning</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="air_condition" value="1" />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="air_condition" value="2" />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="air_condition" value="3" />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS DISHWASHER*/}
                <div className="survey-question" style={{display: `${this.state.wantsDishWasher ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>dishwasher</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="dishwasher" value="1" />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="dishwasher" value="2" />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="dishwasher" value="3" />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS PATIO*/}
                <div className="survey-question" style={{display: `${this.state.wantsPatio ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>patio/balcony</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="patio" value="1" />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="patio" value="2" />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="patio" value="3" />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS POOL*/}
                <div className="survey-question" style={{display: `${this.state.wantsPool ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>pool/hot tub</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="pool" value="1" />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="pool" value="2" />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="pool" value="3" />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS GYM*/}
                <div className="survey-question" style={{display: `${this.state.wantsGym ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>gym</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="gym" value="1" />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="gym" value="2" />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="gym" value="3" />
                        <div>Need it</div>
                    </label>
                </div>

                {/*SHOWS ONLY IF WANTS STORAGE UNIT*/}
                <div className="survey-question" style={{display: `${this.state.wantsStorage ? 'block' : 'none'}`}} onChange={(e) => {this.props.handleInputChange(e, 'number');}}>
                    <h2>How badly do you want a <span>storage unit</span>?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="storage_unit" value="1" />
                        <div>Kinda want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="storage_unit" value="2" />
                        <div>Really want</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="storage_unit" value="3" />
                        <div>Need it</div>
                    </label>
                </div>

                <button className="col-md-12 survey-btn" onClick={this.props.handleNextStep}>
                    Next
                </button>
            </>
        );
    }
}
