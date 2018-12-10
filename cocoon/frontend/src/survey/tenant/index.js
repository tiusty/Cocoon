import React from 'react';
import { Component, Fragment } from 'react';

import TenantForm from './tenantForm';

export default class Tenant extends Component {

    constructor(props) {
        super(props);
        this.state = {

        }

    }

    componentDidMount = () => {
        this.setInitialValid();
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

    render(){
        return (
            <>
                {this.props.tenants.map((t,i) => {
                    return (
                       <TenantForm
                           tenantInfo={t}
                           index={i}
                           key={i}
                           handleInputChange={this.props.handleInputChange}
                           setCommuteAddress={this.props.setCommuteAddress}
                           isTenantValid={this.isTenantValid}
                           commute_type_options={this.props.commute_type_options}
                           setCommuteType={this.props.setCommuteType}
                           setTransitType ={this.setTransitType} />
                    )
                })}
                <button className="col-md-12 survey-btn" style={{marginTop: '30px'}} onClick={(e) => {this.isAllValid() && this.props.handleNextStep(e)}}>
                    Next
                </button>
            </>
        );
    }
}
