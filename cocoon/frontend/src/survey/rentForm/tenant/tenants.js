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

    tenantValid = (tenant_id, valid) => {
        let tenants = [...this.state.tenants];
        for (let i=0; i<this.state.tenants.length; i++ ) {
            if (tenants[i].id === tenant_id) {
                if (tenants[i].valid !== valid) {
                    tenants[i].valid = valid;
                    this.setState({
                        tenants
                    })
                }
            }
        }
    };

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

    render() {
        return (
            <>
                {this.state.tenants.map(t =>
                    <Tenant
                        key={t.id}
                        id={t.id}
                        tenantInfo={t}
                        commute_type_options={this.state.commute_type_options}
                        tenantValid={this.tenantValid}
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
