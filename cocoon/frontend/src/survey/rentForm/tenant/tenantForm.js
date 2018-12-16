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
            valid: false,

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

            // Commute questions
            commute_type: null,
            driving_options: null,
            transit_options: [],
            max_commute: 60,
            min_commute: 0,
            commute_weight: 0,

            //Other
            income: null,
            credit_score: null,
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
        valid = valid && this.handleFinancialValidation();
        this.setState({
            valid
        }, () => this.props.tenantValid(this.props.id, valid));
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
        // Make sure that the commute type is not null
        let valid = true;
        if (this.state.commute_type === null) {
            valid = false
        }

        // If the option is not work from home then make sure the address fields are filled in
        if (this.state.commute_type !== this.getCommuteId('Work From Home')) {
            if (this.state.full_address === null || this.state.street_address === null || this.state.city === null
                || this.state.zip_code === null || this.state.state === null) {
                valid = false
            }

            // Make sure if the option is not work from home then the max commute is set
            if (this.state.max_commute === null) {
                valid = false
            }

            if (this.state.commute_weight < 0 || this.state.commute_weight > 6) {
                valid = false
            }
        }

        // Make sure if driving then driving options selected
        if (this.state.commute_type === this.getCommuteId('Driving')) {
            if (this.state.driving_options === null) {
                valid = false
            }
        }

        // Make sure a transit option is selected if transit is selected
        if (this.state.commute_type === this.getCommuteId('Transit')) {
            if (this.state.transit_options === null) {
                valid = false
            }
        }
        return valid
    }

    handleFinancialValidation() {
        let valid = true;
        if (this.state.income === null) {
            valid = false
        }

        if (this.state.credit_score === null) {
            valid = false
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
        if (this.state.valid) {
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
        if (this.state.valid) {
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
        } else {
            classes = classes + "tenant-questions-inactive"
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
                    <h2>{this.props.id === 0 ? 'Are' : 'Is'} <span>{name}</span> working, studying, or other?
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
        } else {
            return null;
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
                    {this.renderCommuteTypeOptions()}
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

    renderCommuteTypeOptions() {
        if (this.state.commute_type === this.getCommuteId('Driving')) {
            return this.renderDrivingOptions()
        } else if (this.state.commute_type === this.getCommuteId('Transit')) {
            return this.renderTransitOptions()
        } else {
            return null;
        }
    }

    renderDrivingOptions = () => {
        return (
            <div className="survey-question" id={`${this.state.tenant_identifier}-driving-follow-up-question`} onChange={(e) => {
                this.handleInputChange(e, 'string');
            }}>
                <h2>What are the <span>driving options</span>?</h2>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-driving_options`} value="with-traffic"
                           checked={this.state.driving_options === 'with-traffic'}
                           onChange={() => {
                           }}/>
                    <div>With traffic</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.state.tenant_identifier}-driving_options`} value="without-traffic"
                           checked={this.state.driving_options === 'without-traffic'}
                           onChange={() => {
                           }}/>
                    <div>Without traffic</div>
                </label>
            </div>
        );
    };

    renderTransitOptions = () => {
        return (
            <div className="survey-question" id={`${this.state.tenant_identifier}-transit-follow-up-question`} onChange={(e) => {
                this.setTransitType(e);
            }}>
                <h2>What form of <span>transit</span>?</h2>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name={`${this.state.tenant_identifier}-transit_options`} value="bus"
                           checked={this.state.transit_options.some(i => i === 'bus')}
                           onChange={() => {
                           }}/>
                    <div>Bus <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name={`${this.state.tenant_identifier}-transit_options`} value="train"
                           checked={this.state.transit_options.some(i => i === 'train')}
                           onChange={() => {
                           }}/>
                    <div>Train <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name={`${this.state.tenant_identifier}-transit_options`} value="commuter-rail"
                           checked={this.state.transit_options.some(i => i === 'commuter-rail')}
                           onChange={() => {
                           }}/>
                    <div>Commuter rail <i className="material-icons">check</i></div>
                </label>
            </div>
        );
    };

    setTransitType = (e) => {
        const {value, name} = e.target;
        const nameStripped = name.replace(this.state.tenant_identifier+'-', '');
        let transit_type = this.state.transit_options;
        if(e.target.checked) {
            transit_type.push(value);
            this.setState({
                [nameStripped]: transit_type
            })
        } else {
            for(let i = 0; i < transit_type.length; i++) {
                if(transit_type[i] === value) {
                    transit_type.splice(i, 1);
                    this.setState({
                        [nameStripped]: transit_type
                    })
                }
            }
        }
    };

    renderCommuteLengthQuestion = (name) => {
        if (this.state.commute_type !== this.getCommuteId('Work From Home'))
            return (
                <div className="survey-question" id={`${this.state.tenant_identifier}-desired_commute-question`}
                     onBlur={(e) => {
                         this.handleInputChange(e, 'number');
                     }}>
                    <h2>How <span>long of a commute</span> {this.props.id === 0 ? 'do' : 'does'} {name} want?
                    </h2>
                    <input className="col-md-12 survey-input"
                           type="number"
                           name={`${this.state.tenant_identifier}-max_commute`}
                           placeholder="Time in minutes"
                           value={this.state.max_commute || ''}
                           onChange={(e) => {this.handleInputChange(e, 'number')}}/>
                </div>
            );
    };

    renderCommuteWeightQuestion = (name) => {
        if (this.state.commute_type !== this.getCommuteId('Work From Home'))
            return (
                <div className="survey-question" id={`${this.state.tenant_identifier}-commute_weight-question`}
                     onChange={(e) => {
                         this.handleInputChange(e, 'number');
                     }}>
                    <h2>How <span>important is commute</span> to {name}?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-commute_weight`} value="0"
                               checked={this.state.commute_weight === 0}
                               onChange={() => {
                               }}/>
                        <div>Doesn’t care</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-commute_weight`} value="1"
                               checked={this.state.commute_weight === 1}
                               onChange={() => {
                               }}/>
                        <div>Slightly care</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-commute_weight`} value="2"
                               checked={this.state.commute_weight === 2}
                               onChange={() => {
                               }}/>
                        <div>Cares</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-commute_weight`} value="3"
                               checked={this.state.commute_weight === 3}
                               onChange={() => {
                               }}/>
                        <div>Really care</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-commute_weight`} value="4"
                               checked={this.state.commute_weight === 4}
                               onChange={() => {
                               }}/>
                        <div>Super important</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-commute_weight`} value="5"
                               checked={this.state.commute_weight === 5}
                               onChange={() => {
                               }}/>
                        <div>Top priority!</div>
                    </label>
                </div>
            );
    };

    renderIncomeQuestion(name) {
        return (
            <div className="survey-question" id={`${this.state.tenant_identifier}-income-question`} onBlur={(e) => {
                this.handleInputChange(e, 'number');
            }}>
                <h2>What is {this.props.id === 0 ? 'your' : `${name}'s`} <span>approximate income</span>?
                </h2>
                <input className="col-md-12 survey-input" type="number" name={`${this.state.tenant_identifier}-income`}
                       placeholder="Yearly salary" step="1000"
                       value={this.state.income || ''} onChange={(e) => {
                    this.handleInputChange(e, 'number');
                }}/>
            </div>
        );
    }

    renderCreditScoreQuestion(name) {
        return (
                <div className="survey-question" id={`${this.state.tenant_identifier}-credit_score-question`} onChange={(e) => {
                    this.handleInputChange(e, 'string');
                }}>
                    <h2>What is {this.props.id === 0 ? 'your' : `${name}'s`}
                        <span>approximate credit score</span>?</h2>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-credit_score`} value="less than 500"
                               checked={this.state.credit_score === 'less than 500'}
                               onChange={() => {
                               }}/>
                        <div>&lt; 500</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-credit_score`} value="500 - 550"
                               checked={this.state.credit_score === '500 - 550'}
                               onChange={() => {
                               }}/>
                        <div>500 - 550</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-credit_score`} value="551 - 600"
                               checked={this.state.credit_score === '551 - 600'}
                               onChange={() => {
                               }}/>
                        <div>551 - 600</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-credit_score`} value="601 - 650"
                               checked={this.state.credit_score === '601 - 650'}
                               onChange={() => {
                               }}/>
                        <div>601 - 650</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-credit_score`} value="651 - 700"
                               checked={this.state.credit_score === '651 - 700'}
                               onChange={() => {
                               }}/>
                        <div>651 - 700</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-credit_score`} value="701 - 750"
                               checked={this.state.credit_score === '701 - 750'}
                               onChange={() => {
                               }}/>
                        <div>701 - 750</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-credit_score`} value="751 - 800"
                               checked={this.state.credit_score === '751 - 800'}
                               onChange={() => {
                               }}/>
                        <div>751 - 800</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.state.tenant_identifier}-credit_score`} value="801 - 850"
                               checked={this.state.credit_score === '801 - 850'}
                               onChange={() => {
                               }}/>
                        <div>801 - 850</div>
                    </label>
                </div>
        );
    }

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
                    {this.renderCommuteLengthQuestion(name)}
                    {this.renderCommuteWeightQuestion(name)}
                    {this.renderIncomeQuestion(name)}
                    {this.renderCreditScoreQuestion()}
                </div>
            </>
        );
    }
}