import React from 'react';
import { Component } from 'react';
import axios from "axios";

import commutes_endpoints from "../../../endpoints/commutes_endpoints";
import TenantForm from "./tenantForm";

export default class TenantsForm extends Component {
    /**
     *
     * @param props
     *      this.props.tenants_names (Array[{first_name, last_name}]) -> An array of tenants that stores a dicitonary
     *          for their first_name and last_name
     */
    state = {
        commute_type_options: null,
    };

    componentDidMount() {
        // Retrieve all the commute type options
        axios.get(commutes_endpoints['commute_types'])
            .then(res => {
                const commute_type_options = res.data;
                this.setState({ commute_type_options });
            });
    }

    // VALIDATION FUNCTIONS //
    handleValidation = (id) => {
        let valid = true;
        valid = valid && this.handleOccupationValidation(id);
        valid = valid && this.handleOccupationFollowupValidation(id);
        valid = valid && this.handleCommuteTypeValidation(id);
        valid = valid && this.handleFinancialValidation(id);

        let tenants = [...this.props.tenants];
        for (let i=0; i<this.props.tenants.length; i++ ) {
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
        if (!this.props.tenants[id].occupation) {
            valid = false;
        }
        return valid
    }

    handleOccupationFollowupValidation(id) {
        let valid = true;
        if (this.props.tenants[id].occupation === 'working') {
            if (!this.props.tenants[id].new_job) {
                valid = false;
            }
        } else if (this.props.tenants[id].occupation === 'other') {
            if (!this.props.tenants[id].other_occupation_reason) {
                valid = false
            } else if (this.props.tenants[id].other_occupation_reason === 'unemployed' && !this.props.tenant.unemployed_follow_up) {
                valid = false
            }
        }
        return valid
    }

    handleCommuteTypeValidation(id) {
        // Make sure that the commute type is not null
        let valid = true;
        if (this.props.tenants[id].commute_type === null) {
            valid = false
        }

        // If the option is not work from home then make sure the address fields are filled in
        if (this.props.tenants[id].commute_type !== this.getCommuteId('Work From Home')) {
            if (this.props.tenants[id].full_address === null || this.props.tenants[id].street_address === null || this.props.tenants[id].city === null
                || this.props.tenants[id].zip_code === null || this.props.tenants[id].state === null) {
                valid = false
            }

            // Make sure if the option is not work from home then the max commute is set
            if (this.props.tenants[id].max_commute === null) {
                valid = false
            }

            if (this.props.tenants[id].commute_weight < 0 || this.props.tenants[id].commute_weight > 6) {
                valid = false
            }
        }

        // Make sure if driving then driving options selected
        if (this.props.tenants[id].commute_type === this.getCommuteId('Driving')) {
            if (this.props.tenants[id].driving_options === null) {
                valid = false
            }
        }

        // Make sure a transit option is selected if transit is selected
        if (this.props.tenants[id].commute_type === this.getCommuteId('Transit')) {
            if (this.props.tenants[id].transit_options === null) {
                valid = false
            }
        }
        return valid
    }

    handleFinancialValidation(id) {
        let valid = true;
        if (this.props.tenants[id].income === null) {
            valid = false
        }

        if (this.props.tenants[id].credit_score === null) {
            valid = false
        }
        return valid
    }

    isAllValid = () => {
        let valid = true;
        for(let i=0; i<this.props.number_of_tenants; i++) {
            if (!this.props.tenants[i].valid) {
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

    getCommuteId = (type) => {
        if (this.state.commute_type_options) {
            const commuteType = this.state.commute_type_options.filter(o => o.commute_type === type);
            return commuteType[0].id;
        }
    };

    render() {
        return (
            <>
                {this.props.tenants.map(t =>
                    <TenantForm
                        key={t.id}
                        id={t.id}
                        tenant={t}
                        initTenant={this.props.initTenants}
                        commute_type_options={this.state.commute_type_options}
                        onInputChange={this.props.onInputChange}
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
