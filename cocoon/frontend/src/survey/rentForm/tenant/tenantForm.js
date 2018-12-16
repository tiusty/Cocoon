import React from 'react';
import { Component } from 'react';

import Autocomplete from 'react-google-autocomplete';
import './tenantForm.css'

export default class Tenant extends Component {

    constructor(props){
        super(props);
        this.state = {
            is_active: false,
        };
            // General state information
    }

    componentDidMount = () => {
        this.props.initTenant(this.props.id)
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


    handleTenantPanelClick = () => {
        this.props.onHandleValidation(this.props.id);
        this.toggleQuestions();
    };

    handleTenantPanelIcon = () => {
        if (this.props.tenant.valid) {
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
        if (this.props.tenant.valid) {
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
                    this.props.onInputChange(e, 'string', this.props.tenant.tenant_identifier, this.props.id);
                }}>
                    <h2>{this.props.id === 0 ? 'Are' : 'Is'} <span>{name}</span> working, studying, or other?
                    </h2>
                    <span className="col-md-12 survey-error-message"
                          id={`${this.props.tenant.tenant_identifier}-occupation-error`}>You must select an occupation type.</span>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-occupation`} value="working"
                               checked={this.props.tenant.occupation === 'working'}
                               onChange={() => {
                               }}
                        />
                        <div>Working</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-occupation`} value="studying"
                               checked={this.props.tenant.occupation === 'studying'}
                               onChange={() => {
                               }}
                        />
                        <div>Studying</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-occupation`} value="other"
                               checked={this.props.tenant.occupation === 'other'}
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
        if (this.props.tenant.occupation === 'working') {
            return this.renderWorkingOccupation(name)
        } else if (this.props.tenant.occupation === 'other') {
            return this.renderOtherOccupation()
        } else {
            return null;
        }
    }

    renderWorkingOccupation = (name) => {
        return (
            <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-working-occupation-question`} onChange={(e) => this.props.onInputChange(e, 'string', this.props.tenant.tenant_identifier, this.props.id)}>
                <h2>{this.props.id === 0 ? 'Have' : 'Has'} {name} been at this <span>job for less than 6 months</span>?</h2>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.props.tenant.tenant_identifier}-new_job`} value={true} checked={this.props.tenant.new_job === "true"} onChange={() => {}} />
                    <div>Yes</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.props.tenant.tenant_identifier}-new_job`} value={false} checked={this.props.tenant.new_job === "false"} onChange={() => {}} />
                    <div>No</div>
                </label>
            </div>
        );
    };

    renderOtherOccupation = () => {
        return (
            <>
                <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-other-occupation-question`}
                     onChange={(e) => this.props.onInputChange(e, 'string', this.props.tenant.tenant_identifier, this.props.id)}>
                    <h2>What's that <span>other</span>?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-other_occupation_reason`}
                               value="unemployed" checked={this.props.tenant.other_occupation_reason === 'unemployed'}
                               onChange={() => {
                               }}/>
                        <div>Unemployed</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-other_occupation_reason`}
                               value="seeking-work" checked={this.props.tenant.other_occupation_reason === 'seeking-work'}
                               onChange={() => {
                               }}/>
                        <div>Seeking work</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-other_occupation_reason`}
                               value="not-working" checked={this.props.tenant.other_occupation_reason === 'not-working'}
                               onChange={() => {
                               }}/>
                        <div>Not working</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-other_occupation_reason`}
                               value="disability" checked={this.props.tenant.other_occupation_reason === 'disability'}
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
        if (this.props.tenant.other_occupation_reason === 'unemployed') {
            return (
                <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-unemployed-follow-up-question`}
                     onChange={(e) => {
                         this.props.onInputChange(e, 'string', this.props.tenant.tenant_identifier, this.props.id);
                     }}>
                    <h2>Will {name} be <span>paying rent or receiving assistance</span> from a cosigner?</h2>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-unemployed_follow_up`}
                               value="paying-solo" checked={this.props.tenant.unemployed_follow_up === 'paying-solo'}
                               onChange={() => {
                               }}/>
                        <div>Paying solo</div>
                    </label>
                    <label className="col-md-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-unemployed_follow_up`}
                               value="paying-with-help" checked={this.props.tenant.unemployed_follow_up === 'paying-with-help'}
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
        if (this.props.tenant.occupation === 'other') {
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
                    <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-commute_type-question`}>
                        {this.renderCommutePrompt(name)}
                        {this.props.commute_type_options.map((o, index) => (
                                <label className="col-md-6 survey-label" key={index}
                                       onChange={(e) => this.props.onInputChange(e, 'number', this.props.tenant.tenant_identifier, this.props.id)}>
                                    <input type="radio" name={`${this.props.tenant.tenant_identifier}-commute_type`} value={o.id}
                                           checked={this.props.tenant.commute_type === o.id}
                                           onChange={() => {
                                           }}/>
                                    <div>
                                        {o.commute_type === 'Work From Home' && this.props.tenant.occupation === 'other' ? 'No' : o.commute_type}
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
        if (this.props.tenant.commute_type !== this.getCommuteId('Work From Home')) {
            return (
                <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-other-occupation-question`}>
                    <h2>What's the <span>street address</span>?</h2>
                    <Autocomplete
                        className="col-md-12 survey-input"
                        onPlaceSelected={(place) => {
                            this.setCommuteAddress(place)
                        }}
                        types={['address']}
                        name={`${this.props.tenant.tenant_identifier}-commute_address`}
                        placeholder={'Street Address'}
                        value={this.props.tenant.fulladdress}
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
        this.props.tenant.street_address = place.name;
        this.props.tenant.city = formatCity;
        this.props.tenant.state = formatState;
        this.props.tenant.zip_code = formatZip;
        this.props.tenant.full_address = place.formatted_address;
    };

    renderCommuteTypeOptions = () => {
        if (this.props.tenant.commute_type === this.getCommuteId('Driving')) {
            return this.renderDrivingOptions()
        } else if (this.props.tenant.commute_type === this.getCommuteId('Transit')) {
            return this.renderTransitOptions()
        } else {
            return null;
        }
    }

    renderDrivingOptions = () => {
        return (
            <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-driving-follow-up-question`} onChange={(e) => {
                this.props.onInputChange(e, 'string', this.props.tenant.tenant_identifier, this.props.id);
            }}>
                <h2>What are the <span>driving options</span>?</h2>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.props.tenant.tenant_identifier}-driving_options`} value="with-traffic"
                           checked={this.props.tenant.driving_options === 'with-traffic'}
                           onChange={() => {
                           }}/>
                    <div>With traffic</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name={`${this.props.tenant.tenant_identifier}-driving_options`} value="without-traffic"
                           checked={this.props.tenant.driving_options === 'without-traffic'}
                           onChange={() => {
                           }}/>
                    <div>Without traffic</div>
                </label>
            </div>
        );
    };

    renderTransitOptions = () => {
        return (
            <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-transit-follow-up-question`} onChange={(e) => {
                this.setTransitType(e);
            }}>
                <h2>What form of <span>transit</span>?</h2>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name={`${this.props.tenant.tenant_identifier}-transit_options`} value="bus"
                           checked={this.props.tenant.transit_options.some(i => i === 'bus')}
                           onChange={() => {
                           }}/>
                    <div>Bus <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name={`${this.props.tenant.tenant_identifier}-transit_options`} value="train"
                           checked={this.props.tenant.transit_options.some(i => i === 'train')}
                           onChange={() => {
                           }}/>
                    <div>Train <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name={`${this.props.tenant.tenant_identifier}-transit_options`} value="commuter-rail"
                           checked={this.props.tenant.transit_options.some(i => i === 'commuter-rail')}
                           onChange={() => {
                           }}/>
                    <div>Commuter rail <i className="material-icons">check</i></div>
                </label>
            </div>
        );
    };

    setTransitType = (e) => {
        const {value, name} = e.target;
        const nameStripped = name.replace(this.props.tenant.tenant_identifier+'-', '');
        let transit_type = this.props.tenant.transit_options;
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
        if (this.props.tenant.commute_type !== this.getCommuteId('Work From Home'))
            return (
                <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-desired_commute-question`}
                     onBlur={(e) => {
                         this.props.onInputChange(e, 'number', this.props.tenant.tenant_identifier, this.props.id);
                     }}>
                    <h2>How <span>long of a commute</span> {this.props.id === 0 ? 'do' : 'does'} {name} want?
                    </h2>
                    <input className="col-md-12 survey-input"
                           type="number"
                           name={`${this.props.tenant.tenant_identifier}-max_commute`}
                           placeholder="Time in minutes"
                           value={this.props.tenant.max_commute || ''}
                           onChange={(e) => {this.props.onInputChange(e, 'number', this.props.tenant.tenant_identifier, this.props.id)}}/>
                </div>
            );
    };

    renderCommuteWeightQuestion = (name) => {
        if (this.props.tenant.commute_type !== this.getCommuteId('Work From Home'))
            return (
                <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-commute_weight-question`}
                     onChange={(e) => {
                         this.props.onInputChange(e, 'number', this.props.tenant.tenant_identifier, this.props.id);
                     }}>
                    <h2>How <span>important is commute</span> to {name}?</h2>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-commute_weight`} value="0"
                               checked={this.props.tenant.commute_weight === 0}
                               onChange={() => {
                               }}/>
                        <div>Doesn’t care</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-commute_weight`} value="1"
                               checked={this.props.tenant.commute_weight === 1}
                               onChange={() => {
                               }}/>
                        <div>Slightly care</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-commute_weight`} value="2"
                               checked={this.props.tenant.commute_weight === 2}
                               onChange={() => {
                               }}/>
                        <div>Cares</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-commute_weight`} value="3"
                               checked={this.props.tenant.commute_weight === 3}
                               onChange={() => {
                               }}/>
                        <div>Really care</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-commute_weight`} value="4"
                               checked={this.props.tenant.commute_weight === 4}
                               onChange={() => {
                               }}/>
                        <div>Super important</div>
                    </label>
                    <label className="col-md-4 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-commute_weight`} value="5"
                               checked={this.props.tenant.commute_weight === 5}
                               onChange={() => {
                               }}/>
                        <div>Top priority!</div>
                    </label>
                </div>
            );
    };

    renderIncomeQuestion = (name) => {
        return (
            <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-income-question`} onBlur={(e) => {
                this.props.onInputChange(e, 'number', this.props.tenant.tenant_identifier, this.props.id);
            }}>
                <h2>What is {this.props.id === 0 ? 'your' : `${name}'s`} <span>approximate income</span>?
                </h2>
                <input className="col-md-12 survey-input" type="number" name={`${this.props.tenant.tenant_identifier}-income`}
                       placeholder="Yearly salary" step="1000"
                       value={this.props.tenant.income || ''} onChange={(e) => {
                    this.props.onInputChange(e, 'number', this.props.tenant.tenant_identifier, this.props.id);
                }}/>
            </div>
        );
    }

    renderCreditScoreQuestion(name) {
        return (
                <div className="survey-question" id={`${this.props.tenant.tenant_identifier}-credit_score-question`} onChange={(e) => {
                    this.props.onInputChange(e, 'string',this.props.tenant.tenant_identifier, this.props.id);
                }}>
                    <h2>What is {this.props.id === 0 ? 'your' : `${name}'s`}
                        <span>approximate credit score</span>?</h2>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-credit_score`} value="less than 500"
                               checked={this.props.tenant.credit_score === 'less than 500'}
                               onChange={() => {
                               }}/>
                        <div>&lt; 500</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-credit_score`} value="500 - 550"
                               checked={this.props.tenant.credit_score === '500 - 550'}
                               onChange={() => {
                               }}/>
                        <div>500 - 550</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-credit_score`} value="551 - 600"
                               checked={this.props.tenant.credit_score === '551 - 600'}
                               onChange={() => {
                               }}/>
                        <div>551 - 600</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-credit_score`} value="601 - 650"
                               checked={this.props.tenant.credit_score === '601 - 650'}
                               onChange={() => {
                               }}/>
                        <div>601 - 650</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-credit_score`} value="651 - 700"
                               checked={this.props.tenant.credit_score === '651 - 700'}
                               onChange={() => {
                               }}/>
                        <div>651 - 700</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-credit_score`} value="701 - 750"
                               checked={this.props.tenant.credit_score === '701 - 750'}
                               onChange={() => {
                               }}/>
                        <div>701 - 750</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-credit_score`} value="751 - 800"
                               checked={this.props.tenant.credit_score === '751 - 800'}
                               onChange={() => {
                               }}/>
                        <div>751 - 800</div>
                    </label>
                    <label className="col-md-3 col-xs-6 survey-label">
                        <input type="radio" name={`${this.props.tenant.tenant_identifier}-credit_score`} value="801 - 850"
                               checked={this.props.tenant.credit_score === '801 - 850'}
                               onChange={() => {
                               }}/>
                        <div>801 - 850</div>
                    </label>
                </div>
        );
    }

    render() {
        const name = this.props.tenant.first_name;
        const tenant_identifier = this.props.tenant.tenant_identifier;
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
                     onChange={() => this.props.onHandleValidation(this.props.id)}>
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