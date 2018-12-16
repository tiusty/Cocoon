import React from 'react';
import { Component } from 'react';

import './tenantForm.css'

export default class Tenant extends Component {

    constructor(props){
        super(props);
        this.state = {
            is_active: true,
            occupation_type: null,
            other_occupation_reason: null,
            commute_type: null
        }
    }

    componentDidMount = () => {
        if(this.props.id === 0) {
            this.setState({
                isActive: !this.state.isActive
            });
        }
    };

    toggleQuestions = () => {
        this.setState({
            isActive: !this.state.isActive
        });
    };

    handleValidation = () => {
        return true
    };

    handleTenantPanelClick = () => {
        this.handleValidation();
        this.toggleQuestions();
    };

    handleTenantPanelIcon = () => {
        if (this.handleValidation()) {
            return 'check_circle_outline'
        } else {
            return 'error_outline'
        }
    };

    handleTenantPanelClasses() {
        let classes = "tenant-panel ";
        if (this.state.is_active) {
            classes = classes + ' panel-active';
        }
        return classes
    }

    handleTenantIconClasses = () => {
        let classes = 'material-icons ';
        if (this.handleValidation()) {
            return classes + 'valid-panel'
        } else {
            return  classes + 'invalid-panel'
        }
    };

    render() {
        const name = this.props.tenantInfo.first_name;
        const tenant_identifier = `tenants-${this.props.id}`;
        return (
            <div className={this.handleTenantPanelClasses()} onClick={this.handleTenantPanelClick}>
                <div className="tenant-panel-left">
                    <i className={this.handleTenantIconClasses()}>
                        {this.handleTenantPanelIcon()}
                    </i>
                    <span>{name}'s Info</span>
                </div>
                <span><i className="material-icons">{this.state.isActive ? 'remove' : 'add'}</i></span>
            </div>
        );
    }
}