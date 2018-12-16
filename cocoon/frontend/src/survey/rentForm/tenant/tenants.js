import React from 'react';
import { Component } from 'react';
import axios from "axios";

import commutes_endpoints from "../../../endpoints/commutes_endpoints";
import Tenant from "./tenantForm";

export default class Tenants extends Component {
    /**
     *
     * @param props
     *      this.props.tenants_names (Array[{first_name, last_name}]) -> An array of tenants that stores a dicitonary
     *          for their first_name and last_name
     */
    constructor(props) {
        super(props);
        this.state = {
            tenants: [],
        };
        this.state['tenants-INITIAL_FORMS'] = 0;
        this.state['tenants-MAX_NUM_FORMS'] = 1000;
        this.state['tenants-MIN_NUM_FORMS'] = 0;
        this.state['tenants-TOTAL_FORMS'] = this.props.number_of_tenants;
    }

    componentDidMount() {
        this.setState({
            tenants: this.props.tenants_names,
        });

        // Retrieve all the commute type options
        axios.get(commutes_endpoints['commute_types'])
            .then(res => {
                const commute_type_options = res.data;
                this.setState({ commute_type_options });
            });
    }

    componentDidUpdate(prevProps) {
        /*
        Anytime that the state updates this is called
         */

        // If the number of tenants changes then update the total number of forms to equal that
        if (this.props.number_of_tenants !== prevProps.number_of_tenants) {
            this.setState({'tenants-TOTAL_FORMS': this.props.number_of_tenants})
        }

        if (this.props.tenants_names !== prevProps.tenants_names) {
            let current_tenants = [...this.state.tenants];
            for(let i=0; i<this.props.number_of_tenants; i++) {
                if (current_tenants[i].first_name !== this.props.tenants_names[i].first_name) {
                    current_tenants[i].first_name = this.props.tenants_names[i].first_name
                }
                if (current_tenants[i].last_name !== this.props.tenants_names[i].last_name) {
                    current_tenants[i].last_name = this.props.tenants_names[i].last_name
                }
                if (current_tenants[i].id !== this.props.tenants_name[i].id) {
                    current_tenants[i].id = this.props.tenants_names[i].id
                }
            }
            this.setState({
                tenants: current_tenants,
            })
        }
    };

    initializeTenant = (id) => {
        let tenants = [...this.state.tenants];
        for (let i = 0; i < this.state.tenants.length; i++) {
            if (tenants[i].id === id) {
                tenants[i].tenant_identifier = 'tenant-' + id;
                tenants[i].valid = false;

                // Survey questions state
                tenants[i].occupation = null;
                tenants[i].new_job = null;

                tenants[i].other_occupation_reason = null;
                tenants[i].unemployed_follow_up = null;

                // Address
                tenants[i].street_address = null;
                tenants[i].city = null;
                tenants[i].state = null;
                tenants[i].zip_code = null;
                tenants[i].full_address = null;

                // Commute questions
                tenants[i].commute_type = null;
                tenants[i].driving_options = null;
                tenants[i].transit_options = [];
                tenants[i].max_commute = 60;
                tenants[i].min_commute = 0;
                tenants[i].commute_weight = 0;

                //Other
                tenants[i].income = null;
                tenants[i].credit_score = null;

            }
            this.setState({tenants});
        };
    };

    // VALIDATION FUNCTIONS //
    handleValidation = (id) => {
        let valid = true;
        valid = valid && this.handleOccupationValidation(id);
        valid = valid && this.handleOccupationFollowupValidation(id);
        valid = valid && this.handleCommuteTypeValidation(id);
        valid = valid && this.handleFinancialValidation(id);

        let tenants = [...this.state.tenants];
        for (let i=0; i<this.state.tenants.length; i++ ) {
            if (tenants[i].id === id) {
                if (tenants[i].valid !== valid) {
                    tenants[i].valid = valid;
                    this.setState({
                        tenants
                    })
                }
            }
        }
    };

    handleOccupationValidation(id) {
        let valid = true;
        if (!this.state.tenants[id].occupation) {
            valid = false;
        }
        return valid
    }

    handleOccupationFollowupValidation(id) {
        let valid = true;
        if (this.state.tenants[id].occupation === 'working') {
            if (!this.state.tenants[id].new_job) {
                valid = false;
            }
        } else if (this.state.tenants[id].occupation === 'other') {
            if (!this.state.tenants[id].other_occupation_reason) {
                valid = false
            } else if (this.state.tenants[id].other_occupation_reason === 'unemployed' && !this.props.tenant.unemployed_follow_up) {
                valid = false
            }
        }
        return valid
    }

    handleCommuteTypeValidation(id) {
        // Make sure that the commute type is not null
        let valid = true;
        if (this.state.tenants[id].commute_type === null) {
            valid = false
        }

        // If the option is not work from home then make sure the address fields are filled in
        if (this.state.tenants[id].commute_type !== this.getCommuteId('Work From Home')) {
            if (this.state.tenants[id].full_address === null || this.state.tenants[id].street_address === null || this.state.tenants[id].city === null
                || this.state.tenants[id].zip_code === null || this.state.tenants[id].state === null) {
                valid = false
            }

            // Make sure if the option is not work from home then the max commute is set
            if (this.state.tenants[id].max_commute === null) {
                valid = false
            }

            if (this.state.tenants[id].commute_weight < 0 || this.state.tenants[id].commute_weight > 6) {
                valid = false
            }
        }

        // Make sure if driving then driving options selected
        if (this.state.tenants[id].commute_type === this.getCommuteId('Driving')) {
            if (this.state.tenants[id].driving_options === null) {
                valid = false
            }
        }

        // Make sure a transit option is selected if transit is selected
        if (this.state.tenants[id].commute_type === this.getCommuteId('Transit')) {
            if (this.state.tenants[id].transit_options === null) {
                valid = false
            }
        }
        return valid
    }

    handleFinancialValidation() {
        let valid = true;
        if (this.state.tenants[id].income === null) {
            valid = false
        }

        if (this.state.tenants[id].credit_score === null) {
            valid = false
        }
        return valid
    }

    isAllValid = () => {
        let valid = true;
        for(let i=0; i<this.props.number_of_tenants; i++) {
            if (!this.state.tenants[i].valid) {
                valid = false
            }
        }
        return valid
    };

    handleButtonClick(e) {
        if(this.isAllValid()) {
            this.props.handleNextStep(e)
        }
    }

    // HANDLE INPUTS //
    handleInputChange = (e, type, tenant_identifier, id) => {
        const { name, value } = e.target;
        const nameStripped = name.replace(tenant_identifier+'-', '');
        let tenants = [...this.state.tenants];
        for (let i=0; i<this.state.tenants.length; i++) {
            if (tenants[id].id === i) {
                if(type === 'number') {
                    tenants[id][nameStripped] = parseInt(value)
                } else {
                    tenants[id][nameStripped] = value
                }
            }
        }
        this.setState({tenants})
    };

    getCommuteId = (type) => {
        if (this.state.commute_type_options) {
            const commuteType = this.state.commute_type_options.filter(o => o.commute_type === type);
            return commuteType[0].id;
        }
    };

    render() {
        return (
            <>
                {this.state.tenants.map(t =>
                    <Tenant
                        key={t.id}
                        id={t.id}
                        tenant={t}
                        initTenant={this.initializeTenant}
                        commute_type_options={this.state.commute_type_options}
                        onInputChange={this.handleInputChange}
                        onHandleValidation={this.handleValidation}
                    />
                )}
                <div className="row survey-btn-wrapper">
                    <div className="col-sm-6 col-xs-12">
                        <button className="col-sm-12 survey-btn survey-btn_back" style={{marginTop: '30px'}} onClick={(e) => {this.props.handlePrevStep(e)}} >
                            Back
                        </button>
                    </div>
                    <div className="col-sm-6 col-xs-12">
                        <button className="col-sm-12 survey-btn" style={{margintop: '30px'}} onClick={(e) => this.handleButtonClick(e)} >
                            Next
                        </button>
                    </div>
                </div>
            </>
        );
    }
}
