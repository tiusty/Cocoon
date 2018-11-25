import React from 'react';
import { Component, Fragment } from 'react';

import TenantForm from './tenantForm';

export default class Tenant extends Component {
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
                       />
                    )
                })}
                <button className="col-md-12 survey-btn" style={{marginTop: '30px'}} onClick={this.props.handleNextStep}>
                    Next
                </button>
            </>
        );
    }
}
