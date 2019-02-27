import React, {Component} from 'react';
import axios from 'axios';
import survey_endpoints from '../../../../endpoints/survey_endpoints';

import SurveySubscribe from '../../../../common/surveySubscribe';

export default class SurveySnapshot extends Component {

    constructor(props) {
        super(props);
        this.state = {
            amenitiesInfo: {},
            desired_price: 0,
            num_bedrooms: undefined,
            tenants: [],
            updatedTenants: [],
            url: ''
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
                    tenants: response.data.tenants,
                    url: response.data.url
                }, () => this.handleAmenities())
            })
    }

    handleAmenities = () => {
        console.log(this.state.amenitiesInfo)
        // separate amentities based on want, need...
    }

    updateTenantInfo = (e, type) => {
        const { value, dataset } = e.target;
        const name = value;
        const index = dataset.tenantkey;
        let tenants = [...this.state.tenants];

        if (type === 'first') {
            tenants[index].first_name = name;
        } else {
            tenants[index].last_name = name;
        }

        this.setState({
            updatedTenants: tenants
        });

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

    render() {
        return (
            <div className="snapshot-wrapper">
                <h1>Survey Snapshot</h1>

                <div className="snapshot-info">
                    <span>Desired Price: ${this.state.desired_price}</span> | <span>Number of Bedrooms: {this.state.num_bedrooms && this.state.num_bedrooms.join(', ')}</span>
                </div>

                <div className="snapshot-tenants">
                    <h2>Tenants <span>(Please change the names if they're not correct)</span></h2>
                    {this.state.tenants.length && this.state.tenants.reverse().map((tenant, index) => {
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
                </div>

                {/*MAKE BADGES INTO COMMON COMPONENT*/}
                <div className="snapshot-amenities">
                    <h2>Amenities</h2>
                </div>

                <SurveySubscribe />

                <div className="snapshot-buttons">
                    <button onClick={() => this.saveSnapshot(this.state.updatedTenants)}>Save</button>
                    <p>Don't want this survey anymore? <span onClick={() => this.props.deleteSurvey(this.props.activeSurvey.id)}>Delete Survey</span></p>
                </div>

            </div>
        );
    }
}