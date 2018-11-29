import React from 'react';
import { Component, Fragment } from 'react';

import TenantForm from './tenantForm';

export default class Tenant extends Component {

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
                       />
                    )
                })}
                <button className="col-md-12 survey-btn" style={{marginTop: '30px'}} onClick={(e) => {this.isAllValid() && this.props.handleNextStep(e)}}>
                    Next
                </button>
            </>
        );
    }
}
