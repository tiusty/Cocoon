import React from 'react';
import { Component } from 'react';

import Progress from '../progress/index';
import General from '../general/index';
import Tenant from '../tenant/index';
import Amenities from '../amenities/index';
import Details from '../details/index';

import axios from 'axios'
import survey_endpoints from "../../../endpoints/survey_endpoints";
import './rentForm.css';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class RentForm extends Component {

    constructor(props) {
        super(props);
        this.state = {
            step: 1,
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
                        setNumberOfTenants={this.setNumberOfTenants}
                        saveGeneralInfo={this.saveGeneralInfo}
                        generalInfo={this.state.generalInfo} />;
            case 2:
                return <Tenant
                        handleNextStep={this.handleNextStep}
                        handlePrevStep={this.handlePrevStep}
                        tenants={this.state.tenants}
                        number_of_tenants={this.state.number_of_tenants}
                        saveTenantInfo={this.saveTenantInfo}
                        allTenantInfo={this.state.allTenantInfo} />;
            case 3:
                return <Amenities
                        handleNextStep={this.handleNextStep}
                        handlePrevStep={this.handlePrevStep}
                        saveAmenitiesInfo={this.saveAmenitiesInfo}
                        allAmenitiesInfo={this.state.allAmenitiesInfo} />;
            case 4:
                return <Details
                        is_authenticated={this.props.is_authenticated}
                        onSubmit={this.handleSubmit}
                        handlePrevStep={this.handlePrevStep}
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

    // Saves the data from the general tab to repopulate fields with
    saveGeneralInfo = (data) => {
        this.setState({
            generalInfo: data
        }, () => console.log(this.state.generalInfo));
    }

    // Saves the data from the tenant tab to repopulate fields with
    saveTenantInfo = (data) => {
        console.log("save tenant")
        this.setState({
            allTenantInfo: data
        }, () => console.log(this.state.allTenantInfo))
    }

    // Saves the data from the amenities tab to repopulate fields with
    saveAmenitiesInfo = (data) => {
        this.setState({
            allAmenitiesInfo: data
        }, () => console.log(this.state.allAmenitiesInfo))
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