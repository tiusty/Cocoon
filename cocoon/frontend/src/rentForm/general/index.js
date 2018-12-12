import React from 'react';
import { Component, Fragment } from 'react';
import InputRange from 'react-input-range';
import DayPickerInput from 'react-day-picker/DayPickerInput';
import 'react-day-picker/lib/style.css';
import axios from "axios";
import houseDatabase_endpoints from "../../endpoints/houseDatabase_endpoints";

export default class General extends Component {

    constructor(props) {
        super(props);
        this.state = {
            number_of_tenants: 0,
            home_type_options: undefined,
            home_type: [],
            move_weight: '',
            num_bedrooms: '',
            desired_price: 1000,
            price_weight: '',
            max_price: 3000,
            min_bathrooms: 1,
            max_bathrooms: 6,
            parking_spot: 0, // Need to add question
            earliest_move_in: undefined,
            latest_move_in: undefined,
            value: {
                min: 1000,
                max: 3000
            },
            isMovingAsap: '',
            selectedDayEarliest: undefined,
            selectedDayLatest: undefined,
        }
    }

    componentDidMount = () => {
        axios.get(houseDatabase_endpoints['home_types'])
            .then(res => {
                const home_type_options = res.data;
                this.setState({ home_type_options });
        });
        // checks to see if general info data has been saved
        // if true, the state is set to that
        if(this.props.generalInfo) {
            this.setState(this.props.generalInfo)
        }
    }

    componentWillUnmount = () => {
        this.props.setNumberOfTenants(this.state.number_of_tenants);
    }

    // Splits name inputs into first and last names
    handleTenantName = (e) => {
        const { name, value } = e.target;
        const first_name = value.split(' ').slice(0, -1).join(' ');
        const last_name = value.split(' ').slice(-1).join(' ');
        const index = e.target.dataset.tenantkey;
        if(first_name !== '' && last_name !== '') {
            this.props.setTenants(first_name, last_name, index);
        }
    }

    getMaxPrice = (number_of_tenants) => {
        /*
        if(number_of_tenants === 1) {
            return 4000;
        } else if (number_of_tenants < 4) {
            return (number_of_tenants * 3) * 1000;
        } else {
            return 10000;
        }*/
        // For now just return 4000 always, since it will be per person
        return 4000
    }

    getDefaultDates = () => {
        const today = new Date();
        const nextWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 7);
        this.setState({
            selectedDayEarliest: today,
            selectedDayLatest: nextWeek
        }, () => {
           this.setSurveyState('earliest_move_in', this.state.selectedDayEarliest);
           this.setSurveyState('latest_move_in', this.state.selectedDayLatest);
        });
    }

    handleEarliestClick = (day, { selected }) => {
        this.setState({
            selectedDayEarliest: selected ? undefined : day
        }, () => this.setSurveyState('earliest_move_in', this.state.selectedDayEarliest))
    }

    handleLatestClick = (day, { selected }) => {
        this.setState({
            selectedDayLatest: selected  ? undefined : day
        }, () => this.setSurveyState('latest_move_in', this.state.selectedDayLatest))
    }

    handleMovingAsap = (e) => {
        const { value } = e.target;
        if(value === 'yes') {
            this.setState({
                isMovingAsap: value
            }, () => this.getDefaultDates());
        } else {
            this.setState({
                isMovingAsap: value
            });
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
        });
    }

    setHomeTypes = (e, index, id) => {
        let home_type = [...this.state.home_type];
        if(e.target.checked) {
            home_type.push(this.state.home_type_options[index].id);
            this.setState({home_type});
        } else {
            for(let i = 0; i < home_type.length; i++) {
                if(home_type[i] === id) {
                    home_type.splice(i, 1);
                    this.setState({home_type});
                }
            }
        }
    }

    setPrice = (desired, max) => {
        this.setState({
            desired_price: desired,
            max_price: max
        });
    }

    handleValidation = () => {
        return this.validateRadioButton('number_of_tenants', '#number_of_tenants_error')
            && this.validateTenantNames()
            && this.validateHomeType()
            && this.validatePriceWeight()
            && this.validateDates()
            && this.validateRadioButton('move_weight', '#move_weight_error')
            && this.validateRadioButton('num_bedrooms', '#number_of_rooms_error');
    }

    validateTenantNames = () => {
        const inputs = Array.from(document.querySelectorAll('#tenant_names input[type=text]'));
        let emptyFields = inputs.filter(i => i.value === '');
        if(emptyFields.length > 0) {
            document.querySelector('#name_of_tenants_error').style.display = 'block';
            document.querySelector('#name_of_tenants_error').parentNode.scrollIntoView(true);
            return false;
        } else {
            document.querySelector('#name_of_tenants_error').style.display = 'none';
            return true;
        }
    }

    validateDates = () => {
        if(this.state.selectedDayEarliest && this.state.selectedDayLatest) {
            document.querySelector('#date_error').style.display = 'none';
            return true;
        } else {
            document.querySelector('#date_error').style.display = 'block';
            document.querySelector('#date_error').parentNode.scrollIntoView(true);
            return false;
        }
    }

    validateRadioButton = (el, err) => {
        const inputs = document.querySelectorAll(`input[name=${el}]`);
        for (let i = 0; i < inputs.length; i++) {
            if(inputs[i].checked) {
                document.querySelector(err).style.display = 'none';
                return true;
            }
        }
        document.querySelector(err).style.display = 'block';
        document.querySelector(err).parentNode.scrollIntoView(true);
        return false;
    }

    validateHomeType = () => {
        const options = document.querySelectorAll('input[name=home_type]');
        for(let i = 0; i < options.length; i++) {
            if(options[i].checked) {
                document.querySelector('#home_type_error').style.display = 'none';
                return true;
            }
        }
        document.querySelector('#home_type_error').style.display = 'block';
        document.querySelector('#home_type_error').parentNode.scrollIntoView(true);
        return false;
    }

    validatePriceWeight = () => {
        const options = document.querySelectorAll('input[name=price_weight]');
        for(let i = 0; i < options.length; i++) {
            if(options[i].checked) {
                document.querySelector('#price_weight_error').style.display = 'none';
                return true;
            }
        }
        document.querySelector('#price_weight_error').style.display = 'block';
        document.querySelector('#price_weight_error').parentNode.scrollIntoView(true);
        return false;
    }

    render(){
        return (
            <>
                <div className="survey-question" onChange={(e) => {this.handleInputChange(e, 'number'); this.validateRadioButton('number_of_tenants', '#number_of_tenants_error');}}>
                    <h2>How many people are you <span>searching with</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="number_of_tenants_error">You must select the number of people.</span>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="1" checked={this.state.number_of_tenants === 1} onChange={() => {}} />
                        <div>Just Me</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="2" checked={this.state.number_of_tenants === 2} onChange={() => {}} />
                        <div>Me + 1 other</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="3" checked={this.state.number_of_tenants === 3} onChange={() => {}} />
                        <div>Me + 2 others</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="number_of_tenants" value="4" checked={this.state.number_of_tenants === 4} onChange={() => {}} />
                            <div>Me + 3 others</div>
                    </label>
                </div>

                <div className="survey-question" id="tenant_names">
                    <h2>What <span>{this.state.number_of_tenants >= 0 ? ' is your name' : ' are your names'}</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="name_of_tenants_error">Enter first and last name separated by a space.</span>
                    <input className="col-md-12 survey-input" type="text" name="tenant_name" placeholder="First and Last Name" autoCapitalize={'words'} data-tenantkey={0} onChange={this.handleTenantName} />
                    {this.state.number_of_tenants > 1 && Array.from(Array(this.state.number_of_tenants - 1)).map((t, i) => {
                        return <input className="col-md-12 survey-input" type="text" name={'roommate_name_' + (i + 1)} autoCapitalize={'words'} data-tenantkey={i + 1} placeholder="First and Last Name"  onChange={this.handleTenantName} key={i} />
                    })}
                </div>

                {this.state.home_type_options &&
                    <div className="survey-question" onChange={this.validateHomeType}>
                        <h2>What <span>kind of home</span> do you want?</h2>
                        <span className="col-md-12 survey-error-message" id="home_type_error">You must select at least one type of home.</span>
                        {this.state.home_type_options.map((o, index) => (
                            <label className="col-md-6 survey-label survey-checkbox" key={index} onChange={(e) => this.setHomeTypes(e, index, o.id)}>
                                <input type="checkbox" name="home_type" value={o.id} checked={this.state.home_type.length && this.state.home_type.some(i => i === o.id)} onChange={() => {}} />
                                <div>{o.home_type} <i className="material-icons">check</i></div>
                            </label>
                        ))}
                    </div>
                }

                <div className="survey-question">
                    <h2>How much rent do you <span>want to pay per person</span>?</h2>
                    <InputRange
                        draggableTrack
                        maxValue={this.getMaxPrice(this.props.number_of_tenants)}
                        minValue={0}
                        step={50}
                        value={this.state.value}
                        onChange={value => {this.setState({value});this.setPrice(this.state.value.min, this.state.value.max);}}
                        formatLabel={value => `$${value}`} />
                </div>

                <div className="survey-question" onChange={(e) => {this.validatePriceWeight(); this.handleInputChange(e, 'number');}}>
                    <h2>How <span>important is the price</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="price_weight_error">You must choose how much you care about the price.</span>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="price_weight" value="0" checked={this.state.price_weight === 0} onChange={() => {}} />
                        <div>Doesn’t care</div>
                    </label>
                        <label className="col-md-4 survey-label">
                        <input type="radio" name="price_weight" value="1" checked={this.state.price_weight === 1} onChange={() => {}} />
                        <div>Slightly care</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="price_weight" value="2" checked={this.state.price_weight === 2} onChange={() => {}} />
                        <div>Cares</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="price_weight" value="3" checked={this.state.price_weight === 3} onChange={() => {}} />
                        <div>Really care</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="price_weight" value="4" checked={this.state.price_weight === 4} onChange={() => {}} />
                        <div>Super important</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name="price_weight" value="5" checked={this.state.price_weight === 5} onChange={() => {}} />
                        <div>Top priority!</div>
                    </label>
                </div>

                <div className="survey-question" onChange={(e) => this.handleMovingAsap(e)}>
                    <h2>Are you looking to move in <span>as soon as possible?</span></h2>
                    <span className="col-md-12 survey-error-message" id="date_error">You must select an answer.</span>
                    <label className="col-md-6 survey-label">
                            <input type="radio" name="move_asap" value="yes" checked={this.state.isMovingAsap === 'yes'} onChange={() => {}} />
                            <div>Yes</div>
                    </label>
                    <label className="col-md-6 survey-label">
                            <input type="radio" name="move_asap" value="no" checked={this.state.isMovingAsap === 'no'} onChange={() => {}} />
                            <div>No</div>
                    </label>
                </div>

                <div className="survey-question" style={{display: `${this.state.isMovingAsap === 'no' ? 'block' : 'none'}`}}>
                    <h2>When are you wanting to <span>move in</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="date_error">You must select an earliest and latest move in date.</span>
                    <div className="col-md-6 date-wrapper">
                        <DayPickerInput
                            placeholder={'Earliest'}
                            onDayChange={this.handleEarliestClick}
                            value={this.state.earliest_move_in && this.state.earliest_move_in} onChange={() => {}} />
                    </div>
                    <div className="col-md-6 date-wrapper">
                        <DayPickerInput
                            placeholder={'Latest'}
                            onDayChange={this.handleLatestClick}
                            value={this.state.latest_move_in && this.state.latest_move_in} onChange={() => {}} />
                    </div>
                </div>

                <div className="survey-question" onChange={(e) => {this.handleInputChange(e, 'number'); this.validateRadioButton('move_weight', '#move_weight_error');}}>
                    <h2>How badly do you <span>need to move</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="move_weight_error">You must select an option.</span>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="move_weight" value="0" checked={this.state.move_weight === 0} onChange={() => {}} />
                        <div>Just browsing</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="move_weight" value="1" checked={this.state.move_weight === 1} onChange={() => {}} />
                        <div>I've got some time</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="move_weight" value="2" checked={this.state.move_weight === 2} onChange={() => {}} />
                        <div>Moving soon</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="move_weight" value="3" checked={this.state.move_weight === 3} onChange={() => {}} />
                        <div>I gotta move!</div>
                    </label>
                </div>

                <div className="survey-question" onChange={(e) => {this.handleInputChange(e, 'number'); this.validateRadioButton('num_bedrooms', '#number_of_rooms_error');}}>
                    <h2>How many <span>bedrooms</span> do you need?</h2>
                    <span className="col-md-12 survey-error-message" id="number_of_rooms_error">You must select the number of rooms.</span>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="num_bedrooms" value="0" checked={this.state.num_bedrooms === 0} onChange={() => {}} />
                        <div>Studio</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="num_bedrooms" value="1" checked={this.state.num_bedrooms === 1} onChange={() => {}} />
                        <div>1 bed</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="num_bedrooms" value="2" checked={this.state.num_bedrooms === 2} onChange={() => {}} />
                        <div>2 beds</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name="num_bedrooms" value="3" checked={this.state.num_bedrooms === 3} onChange={() => {}} />
                        <div>3 beds</div>
                    </label>
                </div>

                <button className="col-md-12 survey-btn" onClick={(e) => {this.handleValidation() ? (this.props.saveGeneralInfo(this.state), this.props.handleNextStep(e)) : null; } }>
                    Next
                </button>
            </>
        );
    }
}
