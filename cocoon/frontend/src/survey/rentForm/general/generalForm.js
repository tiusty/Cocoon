import React from 'react';
import { Component } from 'react';
import axios from "axios";
import InputRange from 'react-input-range';
import DayPickerInput from 'react-day-picker/DayPickerInput';
import 'react-day-picker/lib/style.css';

import { compose, withProps } from "recompose";
import {
  withGoogleMap,
  GoogleMap,
    Polygon,
    withScriptjs,
} from "react-google-maps";
import DrawingManager from "react-google-maps/lib/components/drawing/DrawingManager"

import houseDatabase_endpoints from "../../../endpoints/houseDatabase_endpoints";

export default class GeneralForm extends Component {
    state = {
        home_type_options: [],
        errorMessages: {
            name_error_undefined: 'You must enter the names of the tenants.',
            name_error_format: 'Enter first and last name separated by a space.',
            home_type_error: 'You must select at least one type of home.',
            price_error_range: 'The price must be between $0 and $4000',
            price_error_weight: 'You must choose how much you care about the price.',
            date_error: 'You must select an earliest and latest move in date.',
            num_bedrooms_error_undefined: 'You must choose the number of bedrooms you need.',
            num_bedrooms_error_amount: 'The number of bedrooms cannot be below 0.'
        }
    };

    componentDidMount = () => {
        // Retrieve all the home types
        axios.get(houseDatabase_endpoints['home_types'])
            .then(res => {
                const home_type_options = res.data;
                this.setState({ home_type_options });
            });
    };

    handleValidation = () => {
        let valid = true;
        valid = valid && this.handleNameValidation();
        valid = valid && this.handleHomeTypeValidation();
        valid = valid && this.handlePriceValidation();
        valid = valid && this.handleMoveAsapValidation();
        // valid = valid && this.handleDatePickerValidation();
        valid = valid && this.handleUrgencyValidation();
        valid = valid && this.handleBedroomValidation();
        return valid
    };

    handleNameValidation() {
        let valid = true;
        if (this.props.tenants.length < this.props.number_of_tenants) {
            valid = false
            document.querySelector('#name_of_tenants_error').style.display = 'block';
            document.querySelector('#name_of_tenants_error').innerText = this.state.errorMessages.name_error_undefined;
            document.querySelector('input[name=tenant_name]').parentNode.scrollIntoView(true)
            alert(this.state.errorMessages.name_error_undefined)
        } else {
            for(let i=0; i<this.props.number_of_tenants; i++) {
                if(!this.props.tenants[i].first_name || !this.props.tenants[i].last_name) {
                    valid = false
                    document.querySelector('#name_of_tenants_error').style.display = 'block';
                    document.querySelector('#name_of_tenants_error').innerText = this.state.errorMessages.name_error_format;
                    document.querySelector('input[name=tenant_name]').parentNode.scrollIntoView(true)
                    alert(this.state.errorMessages.name_error_format)
                }
            }
        }
        if(valid) { document.querySelector('#name_of_tenants_error').style.display = 'none'; }
        return valid
    }

    handleHomeTypeValidation() {
        let valid = true;
        if (this.props.generalInfo.home_type.length === 0) {
            document.querySelector('#home_type_error').style.display = 'block';
            document.querySelector('#home_type_error').innerText = this.state.errorMessages.home_type_error;
            document.querySelector('input[name=home_type]').parentNode.scrollIntoView(true);
            alert(this.state.errorMessages.home_type_error);
            valid = false;
        }
        if(valid) { document.querySelector('#home_type_error').style.display = 'none'; }
        return valid
    }

    handlePriceValidation() {
        let valid = true;
        if (this.props.desired_price < 0) {
            document.querySelector('#price_error').style.display = 'block';
            document.querySelector('#price_error').innerText = this.state.errorMessages.price_error_range;
            document.querySelector('.input-range').parentNode.scrollIntoView(true)
            alert(this.state.errorMessages.price_error_range)
            valid = false
        }
        if (this.props.max_price < 0) {
            document.querySelector('#price_error').style.display = 'block';
            document.querySelector('#price_error').innerText = this.state.errorMessages.price_error_range;
            document.querySelector('.input-range').parentNode.scrollIntoView(true)
            alert(this.state.errorMessages.price_error_range)
            valid = false
        }
        if (this.props.price_weight < 0) {
            document.querySelector('#price_weight_error').style.display = 'block';
            document.querySelector('#price_weight_error').innerText = this.state.errorMessages.price_error_weight;
            document.querySelector('input[name=price_weight]').parentNode.scrollIntoView(true)
            alert(this.state.errorMessages.price_error_weight)
            valid = false
        }
        if(valid) { document.querySelector('#price_weight_error').style.display = 'none'; }
        if(valid) { document.querySelector('#price_error').style.display = 'none'; }
        return valid
    }

    handleMoveAsapValidation() {
        let valid = true;
        if (!this.props.generalInfo.is_move_asap === 'no' || !this.props.generalInfo.is_move_asap === 'yes') {
            valid = false
        }
        return valid
    }

    handleDatePickerValidation() {
        let valid = true;
        if (!this.props.generalInfo.is_move_asap) {
            if (this.props.generalInfo.earliest_move_in === undefined ||
            this.props.generalInfo.latest_move_in === undefined) {
                document.querySelector('#date_error').style.display = 'block';
                document.querySelector('#date_error').innerText = this.state.errorMessages.date_error;
                document.querySelector('.date-wrapper').parentNode.scrollIntoView(true)
                alert(this.state.errorMessages.date_error)
                valid  = false
            } else if(valid) { document.querySelector('#date_error').style.display = 'none'; }
        }
        return valid
    }

    handleUrgencyValidation() {
        let valid = true;
        if (this.props.generalInfo.move_weight < 0) {
            valid = false
        }
        return valid
    }

    handleBedroomValidation() {
        let valid = true;
        if (this.props.generalInfo.num_bedrooms === undefined){
            document.querySelector('#number_of_rooms_error').style.display = 'block';
            document.querySelector('#number_of_rooms_error').innerText = this.state.errorMessages.num_bedrooms_error_undefined;
            document.querySelector('input[name=num_bedrooms]').parentNode.scrollIntoView(true);
            alert(this.state.errorMessages.num_bedrooms_error_undefined);
            valid = false
        } else {
            if (this.props.generalInfo.num_bedrooms < 0) {
                document.querySelector('#number_of_rooms_error').style.display = 'block';
                document.querySelector('#number_of_rooms_error').innerText = this.state.errorMessages.num_bedrooms_error_amount;
                document.querySelector('input[name=num_bedrooms]').parentNode.scrollIntoView(true)
                alert(this.state.errorMessages.num_bedrooms_error_amount);
                valid = false
            }
        }
        if(valid) { document.querySelector('#number_of_rooms_error').style.display = 'none'; }
        return valid
    }

    renderNumberOfPeopleQuestion() {
        return (
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'number')}>
                <h2>How many people are you <span>searching with</span>?</h2>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="1" checked={this.props.number_of_tenants === 1} onChange={() => {}} />
                    <div>Just Me</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="2" checked={this.props.number_of_tenants === 2} onChange={() => {}} />
                    <div>Me + 1 other</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="3" checked={this.props.number_of_tenants === 3} onChange={() => {}} />
                    <div>Me + 2 others</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="4" checked={this.props.number_of_tenants === 4} onChange={() => {}} />
                    <div>Me + 3 others</div>
                </label>
            </div>
        );
    }

    setNameOnField(id) {
        // Display the name if the tenant exists and either a first or last name exists
        if(this.props.tenants.length > id && (this.props.tenants[id].first_name || this.props.tenants[id].last_name)) {
            let first_name = '';
            if(this.props.tenants[id].first_name) {
                first_name = this.props.tenants[id].first_name
            }
            let last_name = '';
            if(this.props.tenants[id].last_name) {
                last_name = this.props.tenants[id].last_name
            }
            return first_name + ' ' + last_name
        } else {
            return ''
        }
    }

    getMaxPrice = (number_of_tenants) => {
        if(number_of_tenants === 1) {
            return 4000;
        } else if (number_of_tenants < 4) {
            return (number_of_tenants * 3) * 1000;
        } else {
            return 10000;
        }
    }

    renderNameQuestion() {
        return (
            <div className="survey-question" id="tenant_names">
                <h2>What <span>{this.props.number_of_tenants <= 1 ? ' is your name' : ' are your names'}</span>?</h2>
                <span className="col-md-12 survey-error-message" id="name_of_tenants_error"></span>
                <input className="col-md-12 survey-input" type="text" name="tenant_name"
                       placeholder="First and Last Name" autoCapitalize={'words'} data-tenantkey={0}
                       value={this.setNameOnField(0)} onChange={this.props.onHandleTenantName}/>
                {this.props.number_of_tenants > 1 && Array.from(Array(this.props.number_of_tenants - 1)).map((t, i) => {
                    return <input className="col-md-12 survey-input" type="text" name={'roommate_name_' + (i + 1)}
                                  autoCapitalize={'words'} data-tenantkey={i + 1} placeholder="First and Last Name"
                                  value={this.setNameOnField(i+1)} onChange={this.props.onHandleTenantName}
                                  key={i}/>
                })}
            </div>
        );
    }

    renderHomeTypeQuestion() {
        if(this.state.home_type_options) {
            return (
                <div className="survey-question" onChange={this.validateHomeType}>
                    <h2>What <span>kind of home</span> do you want?</h2>
                    <span className="col-md-12 survey-error-message" id="home_type_error"></span>
                    {this.state.home_type_options.map((o, index) => (
                        <label className="col-md-6 survey-label survey-checkbox" key={index} onChange={(e) => this.props.setHomeTypes(e, index, o.id)}>
                            <input type="checkbox" name="home_type" value={o.id} checked={this.props.generalInfo.home_type.length && this.props.generalInfo.home_type.some(i => i === o.id)} onChange={() => {}} />
                            <div>{o.home_type} <i className="material-icons">check</i></div>
                        </label>
                    ))}
                </div>

            );
        }
    }

    renderPriceQuestion() {
        return(
            <div className="survey-question">
                <h2>How much rent do you <span>want to pay</span>?</h2>
                <small id="priceHelp" className="form-text text-muted">Left dot is what you want to pay, the right one is the maximum price you are willing to spend
                </small>
                <span className="col-md-12 survey-error-message" id="price_error"></span>
                <InputRange
                    draggableTrack
                    maxValue={this.getMaxPrice(this.props.number_of_tenants)}
                    minValue={0}
                    step={50}
                    value={{min: this.props.generalInfo.desired_price, max: this.props.generalInfo.max_price}}
                    onChange={value => {this.setState({value});this.props.setPrice(this.state.value.min, this.state.value.max);}}
                    formatLabel={value => `$${value}`} />
            </div>
        );
    }

    renderPriceWeightQuestion() {
        return (
            <div className="survey-question" onChange={(e) =>this.props.onGeneralInputChange(e, 'number')}>
                <h2>How <span>important is the price</span>?</h2>
                <span className="col-md-12 survey-error-message" id="price_weight_error"></span>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="0" checked={this.props.generalInfo.price_weight === 0} onChange={() => {}} />
                    <div>Don’t care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="1" checked={this.props.generalInfo.price_weight === 1} onChange={() => {}} />
                    <div>Slightly care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="2" checked={this.props.generalInfo.price_weight === 2} onChange={() => {}} />
                    <div>Care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="3" checked={this.props.generalInfo.price_weight === 3} onChange={() => {}} />
                    <div>Really care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="4" checked={this.props.generalInfo.price_weight === 4} onChange={() => {}} />
                    <div>Super important</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="5" checked={this.props.generalInfo.price_weight === 5} onChange={() => {}} />
                    <div>Top priority!</div>
                </label>
            </div>
        );
    }

    renderMoveAsapQuestion() {
        return (
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'boolean')}>
                <h2>Are you looking to move in <span>as soon as possible?</span></h2>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="is_move_asap" value={true} checked={this.props.generalInfo.is_move_asap === true} onChange={() => {}} />
                    <div>Yes</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="is_move_asap" value={false} checked={this.props.generalInfo.is_move_asap === false} onChange={() => {}} />
                    <div>No</div>
                </label>
            </div>
        );
    }

    renderDatePickingQuestion() {
        if (!this.props.generalInfo.is_move_asap) {
            return (
                <div className="survey-question">
                    <h2>When are you wanting to <span>move in</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="date_error"></span>
                    <div className="col-md-6 date-wrapper">
                        <DayPickerInput
                            placeholder={'Earliest'}
                            onDayChange={this.props.handleEarliestClick}
                            value={this.props.generalInfo.earliest_move_in} onChange={() => {}} />
                    </div>
                    <div className="col-md-6 date-wrapper">
                        <DayPickerInput
                            placeholder={'Latest'}
                            onDayChange={this.props.handleLatestClick}
                            value={this.props.generalInfo.latest_move_in} onChange={() => {}} />
                    </div>
                </div>
            );
        } else {
            return null
        }
    }

    renderUrgencyQuestion() {
        return(
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'number')}>
                <h2>How badly do you <span>need to move</span>?</h2>
                <span className="col-md-12 survey-error-message" id="move_weight_error">You must select an option.</span>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="0" checked={this.props.generalInfo.move_weight === 0} onChange={() => {}} />
                    <div>Just browsing</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="1" checked={this.props.generalInfo.move_weight === 1} onChange={() => {}} />
                    <div>{this.props.number_of_tenants === 1 ? "I've" : "We've"} got some time</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="2" checked={this.props.generalInfo.move_weight === 2} onChange={() => {}} />
                    <div>Moving soon</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="3" checked={this.props.generalInfo.move_weight === 3} onChange={() => {}} />
                    <div>{this.props.number_of_tenants === 1 ? "I" : "We"} gotta move!</div>
                </label>
            </div>
        );
    }

    renderBedroomQuestion() {
        return(
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'number')}>
                <h2>How many <span>bedrooms</span> do you need?</h2>
                <span className="col-md-12 survey-error-message" id="number_of_rooms_error"></span>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="num_bedrooms" value="0" checked={this.props.generalInfo.num_bedrooms === 0} onChange={() => {}} />
                    <div>Studio</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="num_bedrooms" value="1" checked={this.props.generalInfo.num_bedrooms === 1} onChange={() => {}} />
                    <div>1 bed</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="num_bedrooms" value="2" checked={this.props.generalInfo.num_bedrooms === 2} onChange={() => {}} />
                    <div>2 beds</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="num_bedrooms" value="3" checked={this.props.generalInfo.num_bedrooms === 3} onChange={() => {}} />
                    <div>3 beds</div>
                </label>
            </div>
        );
    }

    handleNextButtonAction(e) {
        /**
         * Handles pressing the next button to make sure the section is valid
         *  before allowing the user to continue
         */
        if (this.handleValidation()) {
            this.props.handleNextStep(e)
        }
    }

    renderGoogleMaps() {
        /**
         * Renders the correct google map depending on the type of filtering the user wants
         */

        // 1 is draw on map
        if (this.props.generalInfo.polygon_filter_type === 1) {
            return (
                <>
                    <MyMapComponent
                        onCompletePolygon={this.props.onCompletePolygon}
                        polygons={this.props.generalInfo.polygons}
                    />
                    <button className="survey-btn filter-delete-button" onClick={this.props.onDeleteAllPolygons}>Delete all areas</button>
                </>
            );

        // If the user does not want to draw then make the component null
        } else {
            return null;
        }

    }

    renderFilterQuestion() {
        /**
         * Renders the question for the map filter
         */
        return (
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'number')}>
                <h2>Do you have <span>areas</span> where you would like to live?</h2>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="polygon_filter_type" value="1" checked={this.props.generalInfo.polygon_filter_type === 1}
                           onChange={() => {
                           }}/>
                    <div>Draw on map</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="polygon_filter_type" value="0" checked={this.props.generalInfo.polygon_filter_type === 0} />
                    <div>I am looking everywhere</div>
                </label>
            </div>
        );
    }

    renderFilterZones() {
        return (
            <>
                {this.renderFilterQuestion()}
                {this.renderGoogleMaps()}
            </>
        );

    }



    render() {
        return (
            <>
                {!this.props.is_editing ? this.renderNumberOfPeopleQuestion() : null}
                {this.renderNameQuestion()}
                {this.renderHomeTypeQuestion()}
                {this.renderPriceQuestion()}
                {this.renderPriceWeightQuestion()}
                {this.renderMoveAsapQuestion()}
                {/*{this.renderDatePickingQuestion()}*/}
                {this.renderFilterZones()}
                {this.renderUrgencyQuestion()}
                {this.renderBedroomQuestion()}

                <button className="col-md-12 survey-btn" onClick={(e) => this.handleNextButtonAction(e)} >
                    Next
                </button>
            </>
        );
    }
}

const defaultMapOptions = {
    // Disables the other types of maps, i.e satellite etc
    mapTypeControlOptions: {
        mapTypeIds: []
    },

    gestureHandling: 'cooperative',

    // Disables street view
    streetViewControl: false,

    styles: [
            {
                "featureType": "all",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "simplified"
                    },
                    {
                        "color": "#5b6571"
                    },
                    {
                        "lightness": "35"
                    }
                ]
            },
            {
                "featureType": "administrative.neighborhood",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "landscape",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#f3f4f4"
                    }
                ]
            },
            {
                "featureType": "landscape.man_made",
                "elementType": "geometry",
                "stylers": [
                    {
                        "weight": 0.9
                    },
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#83cead"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#fee379"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway.controlled_access",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "simplified"
                    },
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#7fc8ed"
                    }
                ]
            }
        ],
};

const MyMapComponent = compose(
    withProps({
        loadingElement: <div style={{height: `100%`}}/>,
        containerElement: <div style={{height: `400px`}}/>,
        mapElement: <div style={{height: `100%`}}/>,
        googleMapURL: "https://maps.googleapis.com/maps/api/js?key=AIzaSyCayNcf_pxLj5vaOje1oXYEMIQ6H53Jzho&v=3.exp&libraries=geometry,drawing,places",
    }),
    withScriptjs,
    withGoogleMap
)(props => (
    <GoogleMap
        defaultZoom={11}
        defaultCenter={{lat: 42.3601, lng: -71.0589}}
        defaultOptions={defaultMapOptions}
    >

        {/* Draws all the polygons stored in the state */}
        {props.polygons.map(p =>
                <Polygon
                    key={p.key}
                    path={p.vertices}
                    options={{
                        fillColor: '#008080',
                        strokeColor: '#a13718',
                        fillOpacity: .5,
                        strokeOpacity: .8,
                        strokeWeight: 5,
                        editable: true,
                        zIndex: 1,
                    }}
                />
        )}

        <DrawingManager
            /* Contains all the configuration for the google drawing manager */
            defaultDrawingMode={google.maps.drawing.OverlayType.POLYGON}
            defaultOptions={{
                drawingControl: false,
                drawingControlOptions: {
                    drawingModes: [
                        google.maps.drawing.OverlayType.POLYGON,
                    ],
                },
                polygonOptions: {
                    fillColor: '#008080',
                    strokeColor: '#a13718',
                    fillOpacity: .5,
                    strokeOpacity: .8,
                    strokeWeight: 5,
                    editable: true,
                    zIndex: 1,
                },
            }}
            onPolygonComplete={props.onCompletePolygon}
        />

    </GoogleMap>
));

