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

import houseDatabase_endpoints from '../endpoints/houseDatabase_endpoints';
import commutes_endpoints from '../endpoints/commutes_endpoints';

import survey_endpoints from "../endpoints/survey_endpoints";

import CSRFToken from '../common/csrftoken';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class Survey extends Component {

    constructor(props) {
        super(props);
        this.state = {
            step: 1,
            number_of_tenants: 1,
            tenants: []
        }
        // This allows the variable name to include the hyphen. Including directly
        //  breaks the variable since it isn't allowed in react
        this.state['tenants-TOTAL_FORMS'] = this.state.number_of_tenants;
        this.state['tenants-INITIAL_FORMS'] = 0;
        this.state['tenants-MIN_NUM_FORMS'] = 0;
        this.state['tenants-MAX_NUM_FORMS'] = 1000;
    }

    componentDidUpdate(prevProps, prevState) {
        /*
        Anytime that the state updates this is called
         */

        // If the number of tenants changes then update the total number of forms to equal that
        if (this.state.number_of_tenants !== prevState.number_of_tenants) {
            this.setState({'tenants-TOTAL_FORMS': this.state.number_of_tenants})
        }
    }

    handleSubmit = (e) => {
        e.preventDefault();
        /**
         * This function handles submitting the form to the backend via a rest API
         *  This will return the status of that request and if success redirect,
         *      otherwise it will return the form errors
         */

        // Posts the state which contains all the form elements that are needed
        axios.post(survey_endpoints['rentSurvey'],
            {
                data: this.state,
            })
            .catch(error => console.log('BAD', error))
            .then(response => {
                // On successful form submit then redirect to survey results page
                    if (response.data.result) {
                        window.location = response.data.redirect_url
                    } else {
                        console.log(response.data)
                    }
                }
            );
    };

    setNumberOfTenants = (num) => {
        this.setState({
            number_of_tenants: num
        }, () => this.setFinalTenants())
    }

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
        });
    }


    // Renders the section of the form based on which step the user is on
    renderForm = (step) => {
        switch (step) {
            case 1:
                return <General
                        handleNextStep={this.handleNextStep}
                        setTenants={this.setTenants}
                        setFinalTenants={this.setFinalTenants}
                        tenants={this.state.tenants}
                        setNumberOfTenants={this.setNumberOfTenants} />;
            case 2:
                return <Tenant
                        handleNextStep={this.handleNextStep}
                        handlePrevStep={this.handlePrevStep}
                        tenants={this.state.tenants} />;
            case 3:
                return <Amenities
                        handleNextStep={this.handleNextStep} />;
            case 4:
                return <Details
                        is_authenticated={this.props.is_authenticated}
                        onSubmit={this.handleSubmit}
                        handleInputChange={this.handleInputChange} />;
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

    handlePrevStep = (e) => {
        e.preventDefault();
        this.setState({
            step: this.state.step - 1
        })
        document.body.scrollTop = document.documentElement.scrollTop = 0;
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
        }, () => this.setUserName());
    }

    setUserName = () => {
        this.setState({
            first_name: this.state.tenants[0].first_name,
            last_name: this.state.tenants[0].last_name
        })
    }

    render() {
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