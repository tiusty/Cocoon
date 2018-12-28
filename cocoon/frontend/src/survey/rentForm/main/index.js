// Import React Components
import React from 'react';
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import Progress from '../progress/index';
import GeneralForm from '../general/generalForm';
import TenantsForm from '../tenant/tenantsForm';
import AmenitiesForm from '../amenities/amenitiesForm';
import DetailsForm from '../details/index';
import survey_endpoints from "../../../endpoints/survey_endpoints";
import './rentForm.css';

// Necessary XSRF headers for posting form
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class RentForm extends Component {

    constructor(props) {
        super(props);
        this.state = {
            step: 1,
            loading: false,

            // General Form Fields
            generalInfo: {
                number_of_tenants: 1,
                home_type: [],
                move_weight: 0,
                num_bedrooms: undefined,
                desired_price: 1000,
                max_price: 3000,
                price_weight: 2,
                min_bathrooms: 1,
                max_bathrooms: 6,
                parking_spot: 0,
                earliest_move_in: undefined,
                latest_move_in: undefined,
                is_move_asap: 'yes',
            },

            // Amenities Form Fields
            amenitiesInfo: {
                wants_laundry_in_unit: false,
                wants_laundry_in_building: false,
                wants_laundry_nearby: false,
                wants_parking: false,
                number_of_cars: 0,
                wants_furnished: false,
                furnished_weight: 0,
                wants_dogs: false,
                number_of_dogs: 0,
                service_dogs: false,
                dog_size: '',
                breed_of_dogs: '',
                wants_cats: false,
                cat_weight: 0,
                wants_hardwood_floors: false,
                hardwood_floors_weight: 0,
                wants_AC: false,
                AC_weight: 0,
                wants_dishwasher: false,
                dishwasher_weight: 0,
                wants_patio: false,
                patio_weight: 0,
                wants_pool: false,
                pool_weight: 0,
                wants_gym: false,
                gym_weight: 0,
                wants_storage: false,
                storage_weight: 0,
            },

            // Tenant form fields
            tenants: [],
        };

        // Necessary form management fields for Django formsets
        this.state['tenants-INITIAL_FORMS'] = 0;
        this.state['tenants-MAX_NUM_FORMS'] = 1000;
        this.state['tenants-MIN_NUM_FORMS'] = 0;
        this.state['tenants-TOTAL_FORMS'] = this.state.generalInfo.number_of_tenants;
    }

    componentDidUpdate(prevProps, prevState) {
        /*
        Anytime that the state updates this is called
         */

        // If the number of tenants changes then update the total number of forms to equal that
        if (this.state.generalInfo.number_of_tenants !== prevState.generalInfo.number_of_tenants) {
            this.setState({'tenants-TOTAL_FORMS': this.state.generalInfo.number_of_tenants})
        }
    };

    handleSubmit = (e, detailsData) => {
        e.preventDefault();
        /**
         * This function handles submitting the form to the backend via a rest API
         *  This will return the status of that request and if success redirect,
         *      otherwise it will return the form errors
         *
         *  All the form data is populated into the data variable.
         *      Each form section is a different dictionary element
         *      Each section is added with the appropriate fields
         *
         *      Then the data variable is submitted as the data for the form field to the backend
         */

        // Prevents the user from being able to submit the form again and informs them
        //  that the page is loading
        this.setState({loading: true});

        // Data for the form is submitted in the data variable
        let data = {};


        /**        Tenant Data            **/
        let tenants = [...this.state.tenants];
        let tenantInfo = {};
        // Adds the tenant identifier needed for Django formsets
        // Also all the fields are added to one dictionary instead of in different lists.
        for (let i=0; i<this.state.generalInfo.number_of_tenants; i++) {
            for(let key in tenants[i]) {
                tenantInfo[tenants[i].tenant_identifier + '-' + key] = tenants[i][key]
            }
        }

        // Add the management data for the tenants needed by Django
        tenantInfo['tenants-INITIAL_FORMS'] = this.state['tenants-INITIAL_FORMS'];
        tenantInfo['tenants-MAX_NUM_FORMS'] = this.state['tenants-MAX_NUM_FORMS'];
        tenantInfo['tenants-MIN_NUM_FORMS'] = this.state['tenants-MIN_NUM_FORMS'];
        tenantInfo['tenants-TOTAL_FORMS'] = this.state['tenants-TOTAL_FORMS'];

        // Add the tenant info to the data
        data['tenantInfo'] = tenantInfo;


        /**          General info data               **/
        // Add the general state to the data
        data['generalInfo'] = this.state.generalInfo;

        /**             Amenities data                     **/
        // Add amenities
        data['amenitiesInfo'] = this.state.amenitiesInfo;


        /**         Details data if it exists              **/
        let userData = detailsData;
        if (detailsData !== null) {
            // Add first and last name to details data as the information from the first tenant
            userData['first_name'] = this.state.tenants[0].first_name;
            userData['last_name'] = this.state.tenants[0].last_name;

            // Add the data to the form data
            data['detailsInfo'] = userData
        }

        // Posts the state which contains all the form elements that are needed
        axios.post(survey_endpoints['rentSurvey'],
            {
                data: data,
            })
            .catch(error => {
                console.log('BAD', error);
                this.setState({loading: false})
            })
            // If the response was successful then don't set loading to true
            //  because the page will redirect and we don't want the user to click
            //  the button again
            .then(response => {
                // On successful form submit then redirect to survey results page
                    if (response.data.result) {
                        window.location = response.data.redirect_url
                    } else {
                        this.setState({
                            errors: response.data
                        });
                        this.setState({loading: false})
                    }
                }
            );
    };

    // Renders the section of the form based on which step the user is on
    renderForm = (step) => {
        switch (step) {
            case 1:
                return <GeneralForm
                        handleNextStep={this.handleNextStep}
                        onGeneralInputChange={this.handleGeneralInputChange}
                        number_of_tenants={this.state.generalInfo.number_of_tenants}
                        onHandleTenantName={this.handleTenantName}
                        tenants={this.state.tenants}
                        generalInfo={this.state.generalInfo}
                        setHomeTypes={this.setHomeTypes}
                        setPrice={this.setPrice}
                        handleEarliestClick={this.handleEarliestClick}
                        handleLatestClick={this.handleLatestClick}
                />;
            case 2:
                return <TenantsForm
                        handleNextStep={this.handleNextStep}
                        handlePrevStep={this.handlePrevStep}
                        tenants={this.state.tenants}
                        number_of_tenants={this.state.generalInfo.number_of_tenants}
                        initTenants={this.initializeTenant}
                        onInputChange={this.handleTenantInputChange}
                />;
            case 3:
                return <AmenitiesForm
                        handleNextStep={this.handleNextStep}
                        handlePrevStep={this.handlePrevStep}
                        amenitiesInfo={this.state.amenitiesInfo}
                        onInputChange={this.handleAmenitiesInputChange}
                        />;
            case 4:
                return <DetailsForm
                        is_authenticated={this.props.is_authenticated}
                        onSubmit={this.handleSubmit}
                        handlePrevStep={this.handlePrevStep}
                        errors={this.state.errors}
                        loading={this.state.loading}
                />;
        }
    };

    handleNextStep = (e) => {
        /**
         * Handles when the user clicks next for the next survey section
         */
        e.preventDefault();
        this.setState({
            step: this.state.step + 1
        });
        document.body.scrollTop = document.documentElement.scrollTop = 0;
    };

    handlePrevStep = (e) => {
        /**
         * Handles when the user clicks back for the previous survey section
         */
        e.preventDefault();
        this.setState({
            step: this.state.step - 1
        });
        document.body.scrollTop = document.documentElement.scrollTop = 0;
    };

    handleAmenitiesInputChange = (e, type) => {
        /**
         * Handles input that goes into the amenities form
         *  i.e generalInfo dictionary
         */
        const {name, value} = e.target;
        let data = null;
        if (type === 'number') {
            if(value) {
                data = parseInt(value);
            } else {
                data = 0;
            }
        } else if (type === 'boolean') {
            data = !this.state.amenitiesInfo[name]
        } else {
            data = value
        }
        this.setState({
            amenitiesInfo: {
                ...this.state.amenitiesInfo,
                [name]: data,
            }
        })
    };

    handleGeneralInputChange = (e, type) => {
        /**
         * Handles input that goes into the general form
         *  i.e generalInfo dictionary
         */
        const {name, value} = e.target;
        let data = "";
        if (type === 'number') {
            data = parseInt(value);
        } else {
            data = value
        }

        this.setState({
            generalInfo: {
                ...this.state.generalInfo,
                [name]: data,
            }
        })
    };

    handleEarliestClick = (day, {selected}) => {
        let generalInfo = this.state.generalInfo;
        generalInfo['earliest_move_in'] = selected ? null : day;
        this.setState({generalInfo});
    };

    handleLatestClick = (day, { selected }) => {
        let generalInfo = this.state.generalInfo;
        generalInfo['latest_move_in'] = selected ? null : day;
        this.setState({generalInfo});
    };

    setHomeTypes = (e, index, id) => {
        let generalInfo = this.state.generalInfo;
        let home_type = generalInfo.home_type;
        if(e.target.checked) {
            home_type.push(id);
        } else {
            for(let i = 0; i < home_type.length; i++) {
                if(home_type[i] === id) {
                    home_type.splice(i, 1);
                }
            }
        }
        generalInfo.home_type = home_type;
        this.setState({generalInfo});
    };

    setPrice = (desired, max) => {
        let generalInfo = this.state.generalInfo;
        generalInfo.desired_price = desired;
        generalInfo.max_price = max;
        this.setState({generalInfo});
    };


    // Splits name inputs into first and last names
    handleTenantName = (e) => {
        const { value } = e.target;
        const first_name = value.split(' ').slice(0, -1).join(' ');
        const last_name = value.split(' ').slice(-1).join(' ');
        const index = e.target.dataset.tenantkey;
        let tenants = [...this.state.tenants];

        // Create a new tenant
        if (this.state.tenants.length <= index) {
            let new_tenant = {};
            if(first_name){
                new_tenant.first_name = first_name[0].toUpperCase() + first_name.substr(1);
            }
            if(last_name){
                new_tenant.last_name = last_name[0].toUpperCase() + last_name.substr(1);
            }
            new_tenant.index = parseInt(index);
            new_tenant.valid = false;
            tenants[index] = new_tenant;
            this.setState({
                tenants: tenants
            });
        // If the tenant already exists then just update that tenant
        } else {
            tenants[index].index = parseInt(index);
            tenants[index].first_name = first_name;
            tenants[index].last_name = last_name;
        }
        this.setState({tenants});
    }


    handleTenantInputChange = (e, type, tenant_identifier, id) => {
        /**
         * Handles input change from the tenant page. This ensure that the variable
         *  name is name spaced proeprly in the main state.
         *
         *  For tenant all variables live in
         *      this.state.tenants[tenant_id]
         */
        const { name, value } = e.target;
        const nameStripped = name.replace(tenant_identifier+'-', '');
        let tenants = [...this.state.tenants];
        for (let i=0; i<this.state.tenants.length; i++) {
            if (tenants[id].index === i) {
                if(type === 'number') {
                    tenants[id][nameStripped] = parseInt(value)
                } else if (type === 'boolean') {
                    tenants[id][nameStripped] = (value === 'true');
                } else {
                    tenants[id][nameStripped] = value
                }
            }
        }
        this.setState({tenants})
    };

    initializeTenant = (index) => {
        let tenants = [...this.state.tenants];
        for (let i = 0; i < this.state.tenants.length; i++) {
            if (tenants[i].index === index) {
                tenants[i].tenant_identifier =  this.state.tenants[index].tenant_identifier || 'tenants-' + index;
                tenants[i].valid = this.state.tenants[index].valid || false;

                // Survey questions state
                tenants[i].occupation = this.state.tenants[index].occupation || null;
                tenants[i].new_job = this.state.tenants[index].new_job || null;

                tenants[i].other_occupation_reason = this.state.tenants[index].other_occupation_reason || null;
                tenants[i].unemployed_follow_up = this.state.tenants[index].unemployed_follow_up || null;

                // Address
                tenants[i].street_address = this.state.tenants[index].street_address || null;
                tenants[i].city = this.state.tenants[index].city || null;
                tenants[i].state = this.state.tenants[index].state || null;
                tenants[i].zip_code = this.state.tenants[index].zip_code || null;
                tenants[i].full_address = this.state.tenants[index].full_address || null;

                // Commute questions
                tenants[i].commute_type = this.state.tenants[index].commute_type || null;
                tenants[i].traffic_option = this.state.tenants[index].traffic_option || false;
                tenants[i].transit_options = this.state.tenants[index].transit_options || [];
                tenants[i].max_commute = this.state.tenants[index].max_commute || 60;
                tenants[i].min_commute = this.state.tenants[index].min_commute || 0;
                tenants[i].commute_weight = this.state.tenants[index].commute_weight || 2;

                //Other
                tenants[i].income = this.state.tenants[index].income || null;
                tenants[i].credit_score = this.state.tenants[index].credit_score || null;

            }
            this.setState({tenants});
        }
    };

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