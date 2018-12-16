import React from 'react';
import { Component } from 'react';

import Autocomplete from 'react-google-autocomplete';
import './tenantForm.css'

export default class Tenant extends Component {

    constructor(props){
        super(props);
        this.state = {
            // General state information
            tenant_identifier: 'tenant-' + this.props.id,
            is_active: false,

            // Survey questions state
            occupation: null,
            new_job: null,
            other_occupation_reason: null,
            unemployed_follow_up: null,

            // Address
            street_address: null,
            city: null,
            state: null,
            zip_code: null,
            full_address: null,

            commute_type: null
        }
    }

    componentDidMount = () => {
        if(this.props.id === 0) {
            this.setState({
                is_active: !this.state.is_active
            });
        }
    };

    toggleQuestions = () => {
        this.setState({
            is_active: !this.state.is_active
        });
    };


    // VALIDATION FUNCTIONS //
    handleValidation = () => {
        let valid = true;
        valid = valid && this.handleOccupationValidation();
        valid = valid && this.handleOccupationFollowupValidation();
        valid = valid && this.handleCommuteTypeValidation();
        return valid
    };

    handleOccupationValidation() {
        let valid = true;
        if (!this.state.occupation) {
            valid = false;
        }
        return valid
    }

    handleOccupationFollowupValidation() {
        let valid = true;
        if (this.state.occupation === 'working') {
            if (!this.state.new_job) {
                valid = false;
            }
        } else if (this.state.occupation === 'other') {
            if (!this.state.other_occupation_reason) {
                valid = false
            } else if (this.state.other_occupation_reason === 'unemployed' && !this.state.unemployed_follow_up) {
                valid = false
            }
        }
        return valid
    }

    handleCommuteTypeValidation() {
        let valid = true;
        if (this.state.commute_type === null) {
            valid = false
        }
        if (this.state.commute_type !== this.getCommuteId('Work From Home')) {
            if (this.state.full_address === null || this.state.street_address === null || this.state.city === null
                || this.state.zip_code === null || this.state.state === null) {
                valid = false
            }
        }
        return valid
    }


    // HANDLE INPUTS //
    handleInputChange = (e, type) => {
        const { name, value } = e.target;
        const nameStripped = name.replace(this.state.tenant_identifier+'-', '');
        if(type === 'number') {
            this.setState({
                [nameStripped]: parseInt(value)
            });
        } else {
            this.setState({
                [nameStripped]: value
            });
        }
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
            classes = classes + 'valid-panel'
        } else {
            classes = classes + 'invalid-panel'
        }
        return classes
    };

    handleTenantQuestionClasses() {
        let classes = "tenant-questions ";
        if (this.state.is_active) {
            classes = classes + "tenant-questions-active"
        }
        return classes
    }


    // Rendering functions //
    renderOccupation(name) {
        return (
            <>
                <div className="survey-question" onChange={(e) => {
                    this.handleInputChange(e, 'string');
                }}>
                    <h2>{this.props.index === 0 ? 'Are' : 'Is'} <span>{name}</span> working, studying, or other?
                    </h2>
                    <span className="col-md-12 survey-error-message"
                          id={`${this.state.tenant_identifier}-occupation-error`}>You must select an occupation type.</span>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-occupation`} value="working"
                               checked={this.state.occupation === 'working'}
                               onChange={() => {
                               }}
                        />
                        <div>Working</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-occupation`} value="studying"
                               checked={this.state.occupation === 'studying'}
                               onChange={() => {
                               }}
                        />
                        <div>Studying</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-occupation`} value="other"
                               checked={this.state.occupation === 'other'}
                               onChange={() => {
                               }}
                        />
                        <div>Other</div>
                    </label>
                </div>
                {/*After asking about the occupation, ask the follow up questions*/}
                {this.renderOccupationFollowupQuestions(name)}
            </>
        );
    }

    renderOccupationFollowupQuestions(name) {
        if (this.state.occupation === 'working') {
            return this.renderWorkingOccupation(name)
        } else if (this.state.occupation === 'other') {
            return this.renderOtherOccupation()
        }
    }

    renderWorkingOccupation = (name) => {
        return (
            <div className="survey-question" id={`${this.state.tenant_identifier}-working-occupation-question`} onChange={(e) => this.handleInputChange(e, 'string')}>
                <h2>{this.props.id === 0 ? 'Have' : 'Has'} {name} been at this <span>job for less than 6 months</span>?</h2>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-new_job`} value={true} checked={this.state.new_job === "true"} onChange={() => {}} />
                    <div>Yes</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-new_job`} value={false} checked={this.state.new_job === "false"} onChange={() => {}} />
                    <div>No</div>
                </label>
            </div>
        );
    };

    renderOtherOccupation = () => {
        return (
            <>
                <div className="survey-question" id={`${this.state.tenant_identifier}-other-occupation-question`}
                     onChange={(e) => this.handleInputChange(e, 'string')}>
                    <h2>What's that <span>other</span>?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-other_occupation_reason`}
                               value="unemployed" checked={this.state.other_occupation_reason === 'unemployed'}
                               onChange={() => {
                               }}/>
                        <div>Unemployed</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-other_occupation_reason`}
                               value="seeking-work" checked={this.state.other_occupation_reason === 'seeking-work'}
                               onChange={() => {
                               }}/>
                        <div>Seeking work</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-other_occupation_reason`}
                               value="not-working" checked={this.state.other_occupation_reason === 'not-working'}
                               onChange={() => {
                               }}/>
                        <div>Not working</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-other_occupation_reason`}
                               value="disability" checked={this.state.other_occupation_reason === 'disability'}
                               onChange={() => {
                               }}/>
                        <div>Disability</div>
                    </label>
                </div>
                {/*If the answer was unemployed then render the uunemployedquestion*/}
                {this.renderUnemployedQuestion()}
            </>
        );
    };

    renderUnemployedQuestion = (name) => {
        if (this.state.other_occupation_reason === 'unemployed') {
            return (
                <div className="survey-question" id={`${this.state.tenant_identifier}-unemployed-follow-up-question`}
                     onChange={(e) => {
                         this.handleInputChange(e, 'string');
                     }}>
                    <h2>Will {name} be <span>paying rent or receiving assistance</span> from a cosigner?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-unemployed_follow_up`}
                               value="paying-solo" checked={this.state.unemployed_follow_up === 'paying-solo'}
                               onChange={() => {
                               }}/>
                        <div>Paying solo</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-unemployed_follow_up`}
                               value="paying-with-help" checked={this.state.unemployed_follow_up === 'paying-with-help'}
                               onChange={() => {
                               }}/>
                        <div>Getting help</div>
                    </label>
                </div>
            );
        } else {
            return null;
        }
    };

    renderCommutePrompt = (name) => {
        if (this.state.occupation === 'other') {
            return (
                <h2>Would {name} be using any <span>regular commute type</span>? ex. going into the city</h2>
            );
        } else {
            return (
                <h2>How {this.props.id === 0 ? 'do' : 'does'} {name} <span>commute</span>?</h2>
            );
        }
    };

    renderCommuteTypeQuestion(name) {

        if (this.props.commute_type_options) {
            return (
                <>
                    <div className="survey-question" id={`${this.state.tenant_identifier}-commute_type-question`}>
                        {this.renderCommutePrompt(name)}
                        {this.props.commute_type_options.map((o, index) => (
                                <label className="col-md-6 survey-label" key={index}
                                       onChange={(e) => this.handleInputChange(e, 'number')}>
                                    <input type="radio" name={`${this.state.tenant_identifier}-commute_type`} value={o.id}
                                           checked={this.state.commute_type === o.id}
                                           onChange={() => {
                                           }}/>
                                    <div>
                                        {o.commute_type === 'Work From Home' && this.state.occupation === 'other' ? 'No' : o.commute_type}
                                    </div>
                                </label>
                            )
                        )}
                    </div>
                    {this.renderAddressInput()}
                </>

            );
        } else {
            return null;
        }
    }

    getCommuteId = (type) => {
        if (this.props.commute_type_options) {
            const commuteType = this.props.commute_type_options.filter(o => o.commute_type === type);
            return commuteType[0].id;
        }
    };

    renderAddressInput = () => {
        if (this.state.commute_type !== this.getCommuteId('Work From Home')) {
            return (
                <div className="survey-question" id={`${this.state.tenant_identifier}-other-occupation-question`}>
                    <h2>What's the <span>street address</span>?</h2>
                    <Autocomplete
                        className="col-md-12 survey-input"
                        onPlaceSelected={(place) => {
                            this.setCommuteAddress(place)
                        }}
                        types={['address']}
                        name={`${this.state.tenant_identifier}-commute_address`}
                        placeholder={'Street Address'}
                        value={this.state.fulladdress}
                        onChange={() => {
                        }}
                    />
                </div>
            );
        } else {
            return null;
        }
    };

    setCommuteAddress = (place) => {
        const city = place.address_components.filter(c => c.types[0] === 'locality');
        const formatCity = city[0].long_name;
        const state = place.address_components.filter(c => c.types[0] === 'administrative_area_level_1');
        const formatState = state[0].short_name;
        const zip_code = place.address_components.filter(c => c.types[0] === 'postal_code');
        const formatZip = zip_code[0].long_name;
        this.setState({
            street_address: place.name,
            city: formatCity,
            state: formatState,
            zip_code: formatZip,
            full_address: place.formatted_address
        })
    };

    render() {
        const name = this.props.tenantInfo.first_name;
        const tenant_identifier = this.state.tenant_identifier;
        return (
            <>
                <div className={this.handleTenantPanelClasses()} onClick={this.handleTenantPanelClick}>
                    <div className="tenant-panel-left">
                        <i className={this.handleTenantIconClasses()}>
                            {this.handleTenantPanelIcon()}
                        </i>
                        <span>{name}'s Info</span>
                    </div>
                    <span><i className="material-icons">{this.state.is_active ? 'remove' : 'add'}</i></span>
                </div>
                <div id={`${tenant_identifier}-questions`} className={this.handleTenantQuestionClasses()}
                     onChange={() => this.handleValidation()}>
                    {this.renderOccupation(name)}
                    {this.renderCommuteTypeQuestion(name)}
                </div>
            </>
        );
    }
}