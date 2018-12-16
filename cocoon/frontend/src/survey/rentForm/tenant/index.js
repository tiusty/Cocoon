import React from 'react';
import { Component, Fragment } from 'react';

import TenantForm from './tenantForm/index';
import axios from "axios";
import commutes_endpoints from "../../../endpoints/commutes_endpoints";

export default class Tenant extends Component {

    constructor(props) {
        super(props);
        this.state = {
            commute_type_options: undefined,
        }

    }

    componentDidMount = () => {
        this.setInitialValid();
        axios.get(commutes_endpoints['commute_types'])
            .then(res => {
                const commute_type_options = res.data;
                this.setState({ commute_type_options });
        });
        if(this.props.allTenantInfo) {
            this.setState(this.props.allTenantInfo)
        }
    }

    setInitialValid = () => {
        for(let i = 0; i < this.props.tenants.length; i++) {
            this.setState({
                [`tenant-${[i]}`]: false
            })
        }
    }

    isTenantValid = (index, valid) => {
        this.setState({
            [`tenant-${index}`]: valid
        })
    }

    isAllValid = () => {
        if(Object.values(this.state).every(Boolean)) {
            return true;
        } else {
            return false;
        }
    }

    setTransitType = (e) => {
        const {value, name} = e.target;
        let transit_type = this.state[name] ? [...this.state[name]] : [];
        if(e.target.checked) {
            transit_type.push(value);
            this.setState({
                [name]: transit_type
            })
        } else {
            for(let i = 0; i < transit_type.length; i++) {
                if(transit_type[i] === value) {
                    transit_type.splice(i, 1);
                    this.setState({
                        [name]: transit_type
                    })
                }
            }
        }
    }

    handleInputChange = (e, type) => {
        const { name, value } = e.target;
        if(type === 'number') {
            this.setState({
                [name]: parseInt(value)
            });
        } else {
            this.setState({
                [name]: value
            });
        }
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
            [`${tenantId}zip_code`]: formatZip,
             [`${tenantId}full_address`]: place.formatted_address
        })
    }

    setCommuteType = (tenantId, commute_type) => {
        this.setState({
            [`${tenantId}-commute_type`]: commute_type
        });
    }

    render(){
        return (
            <>
                {this.props.tenants.slice(0, this.props.number_of_tenants).map((t,i) => {
                    return (
                       <TenantForm
                           tenantInfo={t}
                           index={i}
                           key={i}
                           handleInputChange={this.handleInputChange}
                           setCommuteAddress={this.setCommuteAddress}
                           isTenantValid={this.isTenantValid}
                           commute_type_options={this.state.commute_type_options}
                           setCommuteType={this.setCommuteType}
                           setTransitType ={this.setTransitType}
                           allTenantInfo={this.state} />
                    )
                })}
                <div className="row survey-btn-wrapper">
                    <div className="col-sm-6 col-xs-12">
                        <button className="col-sm-12 survey-btn survey-btn_back" style={{marginTop: '30px'}} onClick={(e) => { ( this.props.saveTenantInfo(this.state), this.props.handlePrevStep(e)) } }>
                            Back
                        </button>
                    </div>

                    <div className="col-sm-6 col-xs-12">
                        <button className="col-sm-12 survey-btn" style={{marginTop: '30px'}} onClick={(e) => { this.isAllValid() ? (this.props.saveTenantInfo(this.state), this.props.handleNextStep(e)) : null; } }>
                            Next
                        </button>
                    </div>


                </div>
            </>
        );
    }
}
