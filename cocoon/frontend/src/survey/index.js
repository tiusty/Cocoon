import React from 'react';
import { Component } from 'react';
import ReactDOM from "react-dom";

import Progress from './progress';
import General from './general';
import Tenant from './tenant';
import Amenities from './amenities';
import Details from './details';

import './survey.css';

import axios from 'axios'

class Survey extends Component {

    constructor(props) {
        super(props);
        this.state = {
            step: 1,
            number_of_tenants: 1,
            home_type: 2,
            move_weight: 0,
            num_bedrooms: 1,
            desired_price: 0,
            price_weight: 1,
            max_price: 0,
            earliest_move_in: undefined,
            latest_move_in: undefined,
            tenants: [],
            // tenants-TOTAL_FORMS: 4,
            // tenants-INITIAL_FORMS: 0,
            // tenants-MIN_NUM_FORMS: 0,
            // tenants-MAX_NUM_FORMS: 1000,
        };
    }


    handleSubmit = () => {
        /**
         * This function handles submitting the form to the backend via a rest API
         *  This will return the status of that request and if success redirect,
         *      otherwise it will return the form errors
         */
        console.log('submit here')
        // Function sends a home and toggles that home in the visit_list
        // let endpoint = this.props.endpoint + this.state.id + "/";
        // axios.put(endpoint,
        //     {
        //         home_id: home.id,
        //         type: 'favorite',
        //
        //     })
        //     .catch(error => console.log('BAD', error))
        //     .then(response =>
        //         this.setState({
        //             curr_favorites: response.data.favorites
        //         })
        //     );
    };

    // When changing to step 2 this trims the tenant array to be
    // the length of number_of_tenants
    setFinalTenants = () => {
        let tenants = [...this.state.tenants];
        let finalTenants = [];
        for(let i = 0; i < this.state.number_of_tenants; i++) {
            finalTenants.push(tenants[i]);
            this.setState({
                [`tenants-${i}-first_name`]: tenants[i].first_name,
                [`tenants-${i}-last_name`]: tenants[i].last_name,
            })
        }
        this.setState({
            tenants: finalTenants
        },() => console.log(this.state.tenants));
    }


    // Renders the section of the form based on which step the user is on
    renderForm = (step) => {
        switch (step) {
            case 1:
                return <General
                        handleNextStep={this.handleNextStep}
                        handleInputChange={this.handleInputChange}
                        number_of_tenants={this.state.number_of_tenants}
                        setTenants={this.setTenants}
                        setFinalTenants={this.setFinalTenants}
                        setPrice={this.setPrice}
                        setSurveyState={this.setSurveyState} />;
            case 2:
                return <Tenant
                        handleNextStep={this.handleNextStep}
                        handleInputChange={this.handleInputChange}
                        setCommuteAddress={this.setCommuteAddress}
                        tenants={this.state.tenants} />;
            case 3:
                return <Amenities
                        handleNextStep={this.handleNextStep}
                        setSurveyState={this.setSurveyState}
                        handleInputChange={this.handleInputChange} />;
            case 4:
                return <Details
                    is_authenticated={this.props.is_authenticated}
                    onSubmit={this.handleSubmit}
                />;
        }
    }

    // Increments the step on button click
    handleNextStep = (e) => {
        e.preventDefault();
        this.setState({
            step: this.state.step + 1
        })
        document.body.scrollTop = document.documentElement.scrollTop = 0;
    }

    handleInputChange = (e, type) => {
        const { name, value } = e.target;
        if(type === 'number') {
            this.setState({
                [name]: parseInt(value)
            }, () => console.log(name + ' : ' + value));
        } else {
            this.setState({
                [name]: value
            }, () => console.log(name + ' : ' + value));
        }
    }

    // Set names for tenants and adds them to array of objects
    // so we can map over them and render them out on tenant form
    setTenants = (first_name, last_name, index) => {
        // creates copy of tenants array to modify
        let tenants = [...this.state.tenants];
        let new_tenant = {};
        new_tenant.first_name = first_name[0].toUpperCase() + first_name.substr(1);
        new_tenant.last_name = last_name[0].toUpperCase() + last_name.substr(1);
        tenants[index] = new_tenant;
        this.setState({
            tenants: tenants
        });
    }

    setPrice = (desired, max) => {
        this.setState({
            desired_price: desired,
            max_price: max
        });
    }

    setSurveyState = (state, value) => {
        this.setState({
            [state]: value
        }, () => console.log(state + ': ' + this.state[state]))
    }

    setCommuteAddress = (tenantId, place) => {
        const city = place.address_components.filter(c => c.types[0] === 'locality');
        const formatCity = city[0].long_name;
        const state = place.address_components.filter(c => c.types[0] === 'administrative_area_level_1');
        const formatState = state[0].short_name;
        const zip_code = place.address_components.filter(c => c.types[0] === 'postal_code');
        const formatZip = zip_code[0].long_name;
        this.setState({
            [`${tenantId}street_address`]: place.name,
            [`${tenantId}city`]: formatCity,
            [`${tenantId}state`]: formatState,
            [`${tenantId}zip_code`]: formatZip
        })
    }

    render(){
        return (
            <div className="survey-wrapper">
                <Progress step={this.state.step}/>
                <div className="form-wrapper">
                    {this.renderForm(this.state.step)}
                </div>
            </div>
        );
    }
}

ReactDOM.render(<Survey is_authenticated={window.isUser} />, window.react_mount);