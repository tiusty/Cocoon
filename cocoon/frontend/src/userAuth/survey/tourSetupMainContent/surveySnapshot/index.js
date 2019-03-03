import React, {Component} from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';

import SurveySubscribe from '../../../../common/surveySubscribe';
import survey_endpoints from '../../../../endpoints/survey_endpoints';

export default class SurveySnapshot extends Component {

    constructor(props) {
        super(props);
        this.state = {
            amenitiesInfo: {},
            desired_price: 0,
            num_bedrooms: undefined,
            tenants: [],
            url: '',
            subscribedClick: false,
            is_deleting: false,
        }
    }

    componentDidMount() {
        this.getSurveyData();
    }

    getSurveyData = () => {
        let endpoint = survey_endpoints['rentSurvey'] + this.props.activeSurvey.id;
        axios.get(endpoint)
            .catch(error => console.log('BAD', error))
            .then(response => {
                this.setState({
                    amenitiesInfo: response.data.amenitiesInfo,
                    desired_price: response.data.desired_price,
                    num_bedrooms: response.data.num_bedrooms,
                    tenants: response.data.tenants.sort((a, b) => a.id - b.id),
                    url: response.data.url
                }, () => this.handleAmenities())
            })
    }

    capitalize = (string) => {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    handleAmenities = () => {
        let wantedItems = Object.keys(this.state.amenitiesInfo).reduce((item, key) => {
            (this.state.amenitiesInfo[key] > 0 && typeof this.state.amenitiesInfo[key] !== 'boolean') && (item[key] = this.state.amenitiesInfo[key]);
            return item;
        }, {});
        let wantedItemsArr = Object.keys(wantedItems);
        if (Object.keys(wantedItems).length === 0) {
            return <div className="no-wanted-amenities">No Amenities Selected!</div>
        } else {
            return Object.keys(wantedItems).map((keyName, keyIndex) => {
                let text = wantedItemsArr[keyIndex].split('_weight');
                if (wantedItems[keyName] === 1) {
                    return <div key={keyIndex} className="home-badge home-badge_default">{this.capitalize(text[0]).replace(/_/g,' ')}</div>
                } else if (wantedItems[keyName] === 2) {
                    return <div key={keyIndex} className="home-badge home-badge_mid"><i className="material-icons">done</i> {this.capitalize(text[0]).replace(/_/g,' ')}</div>
                } else {
                    return <div key={keyIndex} className="home-badge home-badge_high"><i className="material-icons">done_all</i> {this.capitalize(text[0]).replace(/_/g,' ')}</div>
                }
            })
        }
    }

    saveSnapshot = (tenants) => {

        // Put all the variables in the correct format so the django formset can handle
        //  them properly
        let tenantInfo = {};
        for (let i=0; i<tenants.length; i++) {
            for(let key in tenants[i]) {
                tenantInfo['tenants-' + i + '-' + key] = tenants[i][key]
            }
        }

        // Add the management data for the tenants needed by Django
        tenantInfo['tenants-INITIAL_FORMS'] = tenants.length;
        tenantInfo['tenants-MAX_NUM_FORMS'] = 1000;
        tenantInfo['tenants-MIN_NUM_FORMS'] = 0;
        tenantInfo['tenants-TOTAL_FORMS'] = tenants.length;

        let endpoint = survey_endpoints['tenants'] + this.props.activeSurvey.id + '/';
        axios.put(endpoint,
            {
                data: tenantInfo,
            })
            .catch(error => console.log('BAD', error))
            .then(response =>
                {
                    this.setState({
                        url: response.data.url,
                        desired_price: response.data.desired_price,
                        num_bedrooms: response.data.num_bedrooms,
                        // Sort the tenants so they always return in the same order
                        tenants: response.data.tenants.sort((a, b) => a.id - b.id),
                    })
                }
            );
    }

    handleSubscribeClick = () => {
        this.setState({
            subscribedClick: !this.state.subscribedClick
        })
    }

    toggleIsDeleting = () => {
        this.setState({
            is_deleting: !this.state.is_deleting
        })
    };

    renderCancelButton = () => {
        if (!this.state.is_deleting) {
            return (<p id="delete-survey-btn"> Don't want this survey anymore? <span onClick={this.toggleIsDeleting}> Delete Survey</span></p>)
        } else {
            return (
                <p id="delete-survey-btn_confirm">
                    Are you sure?
                    <span onClick={() => this.props.deleteSurvey(this.props.activeSurvey.id)}>Yes</span>
                    or
                    <span onClick={this.toggleIsDeleting}>No</span>
                </p>
            );
        }
    };

    render() {
        return (
            <div className="snapshot-wrapper">
                <h1>Survey Snapshot</h1>

                <div className="snapshot-info">
                    <span>Desired Price: ${this.state.desired_price}</span> | <span>Number of Bedrooms: {this.state.num_bedrooms && this.state.num_bedrooms.join(', ')}</span>
                </div>

                <TenantEdit
                    tenants={this.state.tenants}
                    saveSnapshot={this.saveSnapshot}
                />


                <div className="snapshot-amenities">
                    <h2>Amenities</h2>
                    <div className="badge-wrapper">
                        {this.handleAmenities()}
                    </div>
                </div>

                <SurveySubscribe
                    survey_id={this.props.activeSurvey.id}
                />

                {this.renderCancelButton()}

            </div>
        );
    }
}

class TenantEdit extends Component {
    /**
     * Component handles displaying and updating the tenants names
     *
     * Props:
     *     this.props.tenants: (list(Tenants)) -> The list of tenants corresponding to the survey
     */
    state = {
        // Handles the current names of the tenants
        // This is used to determine if the tenants names have been changed
        curr_tenants: [],
    };
    componentDidUpdate(prevProps) {
        /**
         * Handles if the parent tenants variable changes values.
         * If it does then update the curr_tenants value.
         *
         * This is most common when the user submits the new tenants names for saving
         *  and so this updates the new names saved in the backend
         */
        if (prevProps.tenants !== this.props.tenants) {
            // This does a deep copy because otherwise it is a memory reference and causes issues
            let curr_tenants = JSON.parse(JSON.stringify(this.props.tenants));
            this.setState({curr_tenants})
        }
    }
    updateTenantInfo = (e, type) => {
        /**
         * Handles when the user changes one of the tenants names
         *
         * e: -> The event pointer
         * type: (string) -> determines which part of the name is being edited.
         *              'first' for first name
         *              'last' for last name
         */
            // Retrieve which tenant and the new value for the tenant
        const { value } = e.target;
        const name = value.trim();
        const index = e.target.dataset.tenantkey;
        let tenants = [...this.state.curr_tenants];
        // Determines which part of the name is being edited
        if (type === 'first') {
            tenants[index].first_name = name
        } else {
            tenants[index].last_name = name
        }
        // Save the value to the state
        this.setState({curr_tenants: tenants})
    };
    handleDisableSubmit() {
        /**
         * Determines if the tenants variables are the same. If anything was changed then
         *  allow the user to save the data
         *
         * This assumes the tenants are in the correct order.
         */
        for (let i=0; i<this.state.curr_tenants.length; i++) {
            if (this.state.curr_tenants[i].id !== this.props.tenants[i].id
            || this.state.curr_tenants[i].first_name !== this.props.tenants[i].first_name
            || this.state.curr_tenants[i].last_name !== this.props.tenants[i].last_name) {
                return false
            }
        }
        return true
    }

    render() {
        // let tenants = this.props.tenants;
        let tenants = this.state.curr_tenants;
        if (tenants.length > 0) {
            return (
                <>
                    <div className="snapshot-tenants">
                        <h2>Tenants <span>(Please change the names if they're not correct)</span></h2>
                        {tenants.length && tenants.sort((a, b) => a.id - b.id).map((tenant, index) => {
                            return (
                                <div key={index} className="tenant-form">
                                    <span className="tenant-name">Roommate #{index + 1}</span>
                                    <div className="tenant-inputs">
                                        <input type="text"
                                               value={tenant.first_name}
                                               onChange={(e) => this.updateTenantInfo(e, 'first')}
                                               name={'roomate_name_' + index}
                                               autoCapitalize={'words'}
                                               data-tenantkey={index}
                                        />
                                        <input type="text"
                                               value={tenant.last_name}
                                               onChange={(e) => this.updateTenantInfo(e, 'last')}
                                               name={'roomate_name_' + index}
                                               autoCapitalize={'words'}
                                               data-tenantkey={index}
                                        />
                                    </div>
                                </div>
                            );
                        })}

                        <div className="snapshot-buttons">
                            <button
                                disabled={this.handleDisableSubmit()}
                                onClick={() => this.props.saveSnapshot(this.state.curr_tenants)}>
                                Save Tenant's Names
                            </button>
                        </div>
                    </div>
                </>
            )
        } else {
            return <p>Loading</p>
        }

    }
}

TenantEdit.propTypes = {
    tenants: PropTypes.array,
};