import React from 'react';
import { Component } from 'react';
import ReactDOM from "react-dom";

import Progress from './progress';
import General from './general';
import Tenant from './tenant';
import Amenities from './amenities';

import './survey.css';

class Survey extends Component {

    constructor(props) {
        super(props);
        this.state = {
            step: 1,
            number_of_tenants: 1,
            move_weight: 0,
            num_bedrooms: 1,
            desired_price: 0,
            max_price: 0,
            earliest_move_in: undefined,
            latest_move_in: undefined,
            tenants: []
        };
    }

    // When changing to step 2 this trims the tenant array to be
    // the length of number_of_tenants
    setFinalTenants = () => {
        let tenants = [...this.state.tenants];
        let finalTenants = [];
        for(let i = 0; i < this.state.number_of_tenants; i++) {
            finalTenants.push(tenants[i]);
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
                        handleRadioChange={this.handleRadioChange}
                        number_of_tenants={this.state.number_of_tenants}
                        handleTenantArray={this.handleTenantArray}
                        setTenants={this.setTenants}
                        setFinalTenants={this.setFinalTenants}
                        setPrice={this.setPrice}
                        setMoveDate={this.setMoveDate} />;
            case 2:
                return <Tenant
                        handleNextStep={this.handleNextStep} />;
            case 3:
                return <Amenities
                        handleNextStep={this.handleNextStep} />;
        }
    }

    // Increments the step on button click
    handleNextStep = (e) => {
        e.preventDefault();
        this.setState({
            step: this.state.step + 1
        })
    }


    handleRadioChange = (e, type) => {
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
    // with empty values that will be set later in survey
    setTenants = (first_name, last_name, index) => {
        // creates copy of tenants array to modify
        let tenants = [...this.state.tenants];
        let new_tenant = {};
        new_tenant.first_name = first_name;
        new_tenant.last_name = last_name;
        new_tenant.is_student = '';
        new_tenant.street_address = '';
        new_tenant.city = '';
        new_tenant.state = '';
        new_tenant.zip_code = '';
        new_tenant.min_commute = '';
        new_tenant.commute_weight = '';
        new_tenant.commute_type = '';
        tenants[index] = new_tenant;
        this.setState({
            tenants: tenants
        }, () => console.log(this.state.tenants));
    }

    setPrice = (desired, max) => {
        this.setState({
            desired_price: desired,
            max_price: max
        });
    }

    setMoveDate = (state, value) => {
        this.setState({
            state: value
        }, () => console.log(state + ': ' + this.state.state))
    }

    render(){
        return (
            <div className="survey-wrapper">
                <Progress step={this.state.step}/>
                <form>
                    {this.renderForm(this.state.step)}
                </form>
            </div>
        );
    }
}

ReactDOM.render(<Survey is_authenticated={window.isUser} />, window.react_mount);