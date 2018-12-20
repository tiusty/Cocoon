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
    handleValidation = (index) => {
        let valid = true;
        valid = valid && this.handleOccupationValidation(index);
        valid = valid && this.handleOccupationFollowupValidation(index);
        valid = valid && this.handleCommuteTypeValidation(index);
        valid = valid && this.handleFinancialValidation(index);

        let tenants = [...this.props.tenants];
        for (let i=0; i<this.props.tenants.length; i++ ) {
            if (tenants[i].index === index) {
                if (tenants[i].valid !== valid) {
                    tenants[i].valid = valid;
                    this.setState({
                        tenants
                    })
                }
            }
        }
    };

    handleOccupationValidation(index) {
        let valid = true;
        if (!this.props.tenants[index].occupation) {
            document.querySelector(`#tenant-${index}-occupation-error`).style.display = 'block';
            document.querySelector(`#tenant-${index}-occupation-error`).innerText = `Select if ${this.props.tenants[index].first_name} is working, studying, or other.`;
            alert(`Select if ${this.props.tenants[index].first_name} is working, studying, or other.`)
            valid = false;
        }
        if(valid) { document.querySelector(`#tenant-${index}-occupation-error`).style.display = 'none'; }
        return valid
    }

    handleOccupationFollowupValidation(id) {
        let valid = true;
        if (this.props.tenants[id].occupation === 'working') {
            if (!this.props.tenants[id].new_job) {
                document.querySelector(`#tenant-${id}-working-occupation-error`).style.display = 'block';
                document.querySelector(`#tenant-${id}-working-occupation-error`).innerText = `Choose whether or not ${this.props.tenants[id].first_name} has been at their job for 6 months or more.`;
                alert(`Choose whether or not ${this.props.tenants[id].first_name} has been at their job for 6 months or more.`);
                valid = false;
            }
        } else if (this.props.tenants[id].occupation === 'other') {
            if (!this.props.tenants[id].other_occupation_reason) {
                document.querySelector(`#tenant-${id}-other-occupation-error`).style.display = 'block';
                document.querySelector(`#tenant-${id}-other-occupation-error`).innerText = `Select a reason why ${this.props.tenants[id].first_name} is not working or studying.`;
                alert(`Select a reason why ${this.props.tenants[id].first_name} is not working or studying.`);
                valid = false;
            } else if (this.props.tenants[id].other_occupation_reason === 'unemployed' && !this.props.tenants.unemployed_follow_up) {
                document.querySelector(`#tenant-${id}-unemployed-occupation-error`).style.display = 'block';
                document.querySelector(`#tenant-${id}-unemployed-occupation-error`).innerText = `Select if ${this.props.tenants[id].first_name} will be receiving assistance from a cosigner.`;
                alert(`Select if ${this.props.tenants[id].first_name} will be receiving assistance from a cosigner.`);
                valid = false;
            }
        }
        if(valid) {
            if(document.querySelector(`#tenant-${id}-working-occupation-error`)) {
                document.querySelector(`#tenant-${id}-working-occupation-error`).style.display = 'none';
            }
            if(document.querySelector(`#tenant-${id}-other-occupation-error`)) {
                document.querySelector(`#tenant-${id}-other-occupation-error`).style.display = 'none';
            }
            if(document.querySelector(`#tenant-${id}-unemployed-occupation-error`)) {
                document.querySelector(`#tenant-${id}-unemployed-occupation-error`).style.display = 'none';
            }
        }
        return valid
    }

    handleCommuteTypeValidation(id) {
        // Make sure that the commute type is not null
        let valid = true;
        if (this.props.tenants[id].commute_type === null) {
            document.querySelector(`#tenant-${id}-commute_type-error`).style.display = 'block';
            document.querySelector(`#tenant-${id}-commute_type-error`).innerText = `You must select a commute type for ${this.props.tenants[id].first_name}.`;
            valid = false;
        } else if (valid) { document.querySelector(`#tenant-${id}-commute_type-error`).style.display = 'none'; }

        // If the option is not work from home then make sure the address fields are filled in
        if (this.props.tenants[id].commute_type !== this.getCommuteId('Work From Home')) {
            console.log('in case')
            if (this.props.tenants[id].full_address === null || this.props.tenants[id].street_address === null || this.props.tenants[id].city === null
                || this.props.tenants[id].zip_code === null || this.props.tenants[id].state === null) {
                document.querySelector(`#tenant-${id}-commute_address-error`).style.display = 'block';
                document.querySelector(`#tenant-${id}-commute_address-error`).innerText = `You must enter a commute address for ${this.props.tenants[id].first_name}.`;
                valid = false;
            } else if (valid) { document.querySelector(`#tenant-${id}-commute_address-error`).style.display = 'none'; }

            // Make sure if the option is not work from home then the max commute is set
            console.log(this.props.tenants[id].max_commute)
            if (this.props.tenants[id].max_commute === null) {
                console.log('max_comute')
                document.querySelector(`#tenant-${id}-desired_commute-error`).style.display = 'block';
                document.querySelector(`#tenant-${id}-desired_commute-error`).innerText = `You must enter a maximum commute time for ${this.props.tenants[id].first_name}.`;
                valid = false;
            } else if (valid) { document.querySelector(`#tenant-${id}-desired_commute-error`).style.display = 'none'; }

            if (this.props.tenants[id].commute_weight < 0 || this.props.tenants[id].commute_weight > 6) {
                document.querySelector(`#tenant-${id}-commute_weight-error`).style.display = 'block';
                document.querySelector(`#tenant-${id}-commute_weight-error`).innerText = `You must choose how important commute time is for ${this.props.tenants[id].first_name}.`;
                valid = false;
            } else if (valid) { document.querySelector(`#tenant-${id}-commute_weight-error`).style.display = 'none'; }
        }

        // Make sure if driving then driving options selected
        if (this.props.tenants[id].commute_type === this.getCommuteId('Driving')) {
            if (this.props.tenants[id].driving_options === null) {
                document.querySelector(`#tenant-${id}-driving_options_error`).style.display = 'block';
                document.querySelector(`#tenant-${id}-driving_options_error`).innerText = `You must select a driving option for ${this.props.tenants[id].first_name}.`;
                valid = false;
            } else if (valid) { document.querySelector(`#tenant-${id}-driving_options_error`).style.display = 'none'; }
        }

        // Make sure a transit option is selected if transit is selected
        if (this.props.tenants[id].commute_type === this.getCommuteId('Transit')) {
            if (this.props.tenants[id].transit_options === null) {
                document.querySelector(`#tenant-${id}-transit_options_error`).style.display = 'block';
                document.querySelector(`#tenant-${id}-transit_options_error`).innerText = `You must select a transit option for ${this.props.tenants[id].first_name}.`;
                valid = false;
            } else if (valid) { document.querySelector(`#tenant-${id}-transit_options_error`).style.display = 'none'; }
        }

        if (!valid) { alert(`You must fix the commute errors for ${this.props.tenants[id].first_name}.`); }

        return valid
    }

    handleFinancialValidation(id) {
        let valid = true;
        if (this.props.tenants[id].income === null) {
            document.querySelector(`#tenant-${id}-income-error`).style.display = 'block';
            document.querySelector(`#tenant-${id}-income-error`).innerText = `You must enter an annual income for ${this.props.tenants[id].first_name}.`;
            valid = false
        } else if (this.props.tenants[id].income) { document.querySelector(`#tenant-${id}-income-error`).style.display = 'none'; }

        if (this.props.tenants[id].credit_score === null) {
            document.querySelector(`#tenant-${id}-credit_score-error`).style.display = 'block';
            document.querySelector(`#tenant-${id}-credit_score-error`).innerText = `You must select an approximate credit score for ${this.props.tenants[id].first_name}.`;
            valid = false;
        } else if (this.props.tenants[id].credit_score) { document.querySelector(`#tenant-${id}-credit_score-error`).style.display = 'none'; }

        if (!valid) { alert(`You must fix the finance errors for ${this.props.tenants[id].first_name}.`); }

        return valid
    }

    isAllValid = () => {
        let valid = true;
        for(let i=0; i<this.props.number_of_tenants; i++) {
            this.handleValidation(i)
            if (!this.props.tenants[i].valid) {
                valid = false
                return valid
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
                {this.props.tenants.slice(0, this.props.number_of_tenants).map(t =>
                    <TenantForm
                        key={t.index}
                        index={t.index}
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
