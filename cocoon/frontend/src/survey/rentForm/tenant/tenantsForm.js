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
        // After retrieving the commute types, update the validation to see
        //  if the tenants are valid
        axios.get(commutes_endpoints['commute_types'])
            .then(res => {
                const commute_type_options = res.data;
                this.setState({ commute_type_options }, () => this.validateAllTenants());
            })
    }

    validateAllTenants() {
        /**
         * Runs validation on all the tenants to update whether or not they are valid
         */
        for (let i=0; i<this.props.tenants.length; i++) {
            this.handleValidation(i, false);
        }

    }

    // VALIDATION FUNCTIONS //
    handleValidation = (index, show_errors) => {
        let valid = true;
        valid = this.handleOccupationValidation(index, show_errors) && valid;
        valid = this.handleOccupationFollowupValidation(index, show_errors) && valid;
        valid = this.handleCommuteTypeValidation(index, show_errors) && valid;
        valid = this.handleFinancialValidation(index, show_errors) && valid;

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

    handleOccupationValidation(index, show_errors) {
        let valid = true;
        if (!this.props.tenants[index].occupation) {
            if (show_errors) {
                document.querySelector(`#tenants-${index}-occupation-error`).style.display = 'block';
                document.querySelector(`#tenants-${index}-occupation-error`).innerText = `Select if ${this.props.tenants[index].first_name} is working, studying, or other.`;
            }
            valid = false;
        }
        if(valid) {
            let selection = document.querySelector(`#tenants-${index}-occupation-error`);
            if (selection) {
                selection.style.display = 'none';
            }
        }
        return valid
    }

    handleOccupationFollowupValidation(id, show_errors) {
        let valid = true;
        if (this.props.tenants[id].occupation === 'working') {
            if (!this.props.tenants[id].new_job) {
                if (show_errors) {
                    document.querySelector(`#tenants-${id}-working-occupation-error`).style.display = 'block';
                    document.querySelector(`#tenants-${id}-working-occupation-error`).innerText = `Choose whether or not ${this.props.tenants[id].first_name} has been at their job for 6 months or more.`;
                }
                valid = false;
            }
        } else if (this.props.tenants[id].occupation === 'other') {
            if (!this.props.tenants[id].other_occupation_reason) {
                if (show_errors) {
                    document.querySelector(`#tenants-${id}-other-occupation-error`).style.display = 'block';
                    document.querySelector(`#tenants-${id}-other-occupation-error`).innerText = `Select a reason why ${this.props.tenants[id].first_name} is not working or studying.`;
                }
                valid = false;
            } else if (this.props.tenants[id].other_occupation_reason === 'unemployed' && !this.props.tenants[id].unemployed_follow_up) {
                if (show_errors) {
                    document.querySelector(`#tenants-${id}-unemployed-occupation-error`).style.display = 'block';
                    document.querySelector(`#tenants-${id}-unemployed-occupation-error`).innerText = `Select if ${this.props.tenants[id].first_name} will be receiving assistance from a cosigner.`;
                }
                valid = false;
            }
        }
        if(valid) {
            if(document.querySelector(`#tenants-${id}-working-occupation-error`)) {
                document.querySelector(`#tenants-${id}-working-occupation-error`).style.display = 'none';
            }
            if(document.querySelector(`#tenants-${id}-other-occupation-error`)) {
                document.querySelector(`#tenants-${id}-other-occupation-error`).style.display = 'none';
            }
            if(document.querySelector(`#tenants-${id}-unemployed-occupation-error`)) {
                document.querySelector(`#tenants-${id}-unemployed-occupation-error`).style.display = 'none';
            }
        }
        return valid
    }

    handleCommuteTypeValidation(id, show_errors) {
        // Make sure that the commute type is not null
        let valid = true;
        if (this.props.tenants[id].commute_type === null) {
            if (show_errors) {
                document.querySelector(`#tenants-${id}-commute_type-error`).style.display = 'block';
                document.querySelector(`#tenants-${id}-commute_type-error`).innerText = `You must select a commute type for ${this.props.tenants[id].first_name}.`;
            }

            valid = false;
        } else if (valid) {
            let selection = document.querySelector(`#tenants-${id}-commute_type-error`);
            if (selection) {
                selection.style.display = 'none';
            }
        }

        // If the option is not work from home then make sure the address fields are filled in
        if (this.props.tenants[id].commute_type !== this.getCommuteId('Work From Home')) {
            if (this.props.tenants[id].full_address === null || this.props.tenants[id].street_address === null || this.props.tenants[id].city === null
                || this.props.tenants[id].zip_code === null || this.props.tenants[id].state === null) {
                if (show_errors) {
                    document.querySelector(`#tenants-${id}-commute_address-error`).style.display = 'block';
                    document.querySelector(`#tenants-${id}-commute_address-error`).innerText = `You must enter a commute address for ${this.props.tenants[id].first_name}.`;
                }
                valid = false;
            } else if (valid) {

                let selection = document.querySelector(`#tenants-${id}-commute_address-error`)
                if (selection) {
                    selection.style.display = 'none';
                }
            }

            // Make sure if the option is not work from home then the max commute is set
            if (this.props.tenants[id].max_commute === null) {
                if (show_errors) {
                    document.querySelector(`#tenants-${id}-desired_commute-error`).style.display = 'block';
                    document.querySelector(`#tenants-${id}-desired_commute-error`).innerText = `You must enter a maximum commute time for ${this.props.tenants[id].first_name}.`;
                }
                valid = false;
            } else if (valid) {
                let selection = document.querySelector(`#tenants-${id}-desired_commute-error`);
                if (selection) {
                    selection.style.display = 'none';
                }
            }

            if (this.props.tenants[id].commute_weight < 0 || this.props.tenants[id].commute_weight > 6) {
                if (show_errors) {
                    document.querySelector(`#tenants-${id}-commute_weight-error`).style.display = 'block';
                    document.querySelector(`#tenants-${id}-commute_weight-error`).innerText = `You must choose how important commute time is for ${this.props.tenants[id].first_name}.`;
                }
                valid = false;
            } else if (valid) {
                let selection = document.querySelector(`#tenants-${id}-commute_weight-error`);
                if (selection) {
                    selection.style.display = 'none';
                }
            }
        }

        // Make sure if driving then driving options selected
        if (this.props.tenants[id].commute_type === this.getCommuteId('Driving')) {
            if (this.props.tenants[id].traffic_option === null) {
                if (show_errors) {
                    document.querySelector(`#tenants-${id}-driving_options_error`).style.display = 'block';
                    document.querySelector(`#tenants-${id}-driving_options_error`).innerText = `You must select a driving option for ${this.props.tenants[id].first_name}.`;
                }
                valid = false;
            } else if (valid) {
                let selection = document.querySelector(`#tenants-${id}-driving_options_error`);
                if (selection) {
                    selection.style.display = 'none';
                }
            }
        }

        // Make sure a transit option is selected if transit is selected
        if (this.props.tenants[id].commute_type === this.getCommuteId('Transit')) {
            if (this.props.tenants[id].transit_options === null) {
                if (show_errors) {
                    document.querySelector(`#tenants-${id}-transit_options_error`).style.display = 'block';
                    document.querySelector(`#tenants-${id}-transit_options_error`).innerText = `You must select a transit option for ${this.props.tenants[id].first_name}.`;
                }
                valid = false;
            } else if (valid) {
                let selection = document.querySelector(`#tenants-${id}-transit_options_error`);
                if (selection) {
                    selection.style.display = 'none';
                }
            }
        }

        return valid
    }

    handleFinancialValidation(id, show_errors) {
        let valid = true;
        if (this.props.tenants[id].income === null || !Number.isInteger(this.props.tenants[id].income)) {
            if (show_errors) {
                document.querySelector(`#tenants-${id}-income-error`).style.display = 'block';

                if (this.props.tenants[id].income === null) {
                    document.querySelector(`#tenants-${id}-income-error`).innerText = `You must enter an annual income for ${this.props.tenants[id].first_name}.`;
                } else {
                    document.querySelector(`#tenants-${id}-income-error`).innerText = `Income must be a number for ${this.props.tenants[id].first_name}.`;
                }
            }
            valid = false
        } else if (this.props.tenants[id].income) {
            let selection = document.querySelector(`#tenants-${id}-income-error`);
            if (selection) {
                selection.style.display = 'none';
            }
        }

        if (this.props.tenants[id].credit_score === null) {
            if (show_errors) {
                document.querySelector(`#tenants-${id}-credit_score-error`).style.display = 'block';
                document.querySelector(`#tenants-${id}-credit_score-error`).innerText = `You must select an approximate credit score for ${this.props.tenants[id].first_name}.`;
            }
            valid = false;
        } else if (this.props.tenants[id].credit_score) {
            let selection = document.querySelector(`#tenants-${id}-credit_score-error`);
            if (selection) {
                selection.style.display = 'none';
            }
        }

        return valid
    }

    isAllValid = () => {
        let valid = true;
        for(let i=0; i<this.props.number_of_tenants; i++) {
            this.handleValidation(i, true)
            if (!this.props.tenants[i].valid) {
                valid = false
                alert('Please fix errors for ' + this.props.tenants[i].first_name);
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
                        onAddressChange={this.props.onAddressChange}
                        onAddressSelected={this.props.onAddressSelected}
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
