import React from 'react';
import { Component } from 'react';

import houseIcon from './found-apt.png';

import PhoneInput from 'react-phone-number-input/basic-input'

export default class DetailsForm extends Component {
    state = {
        errorMessages: {
            email_error: 'You must enter a valid email address.',
            phone_error: 'Enter a valid phone number. ex. (555) 555-5555',
            agent_referral_error: 'The Agent Url is not valid, please confirm with you agent that you have the right number',
            password_error_number: 'The password must contain at least 1 number',
            password_error_length: 'Password must be at least 8 characters.',
            password_error_match: 'Passwords must match.',
        },
        phone_number: '',
        user_logging_in: false,
    }

    componentDidUpdate = (prevProps) => {
        if(this.props.errors !== prevProps.errors) {
            this.handleSubmitErrors(this.props.errors);
        }
    }

    handleSubmitErrors = (errors) => {
        /**
         * Handles errors returned from the backend
         * @type {boolean}
         */
        let valid = true;
        if (errors.user_form_errors) {
            // Email Errors
            if (errors.user_form_errors.email) {
                document.querySelector('#email_error').style.display = 'block';
                document.querySelector('#email_error').innerText = errors.user_form_errors.email[0];
                valid = false;
            } else if (!errors.user_form_errors.email) { document.querySelector('#email_error').style.display = 'none'; }

            // Password errors
                if (errors.user_form_errors.password1) {
                    document.querySelector('#password_error').style.display = 'block';
                    document.querySelector('#password_error').innerText = errors.user_form_errors.password1[0];
                    valid = false;
                } else if (!errors.user_form_errors.password1) {
                    document.querySelector('#password_error').style.display = 'none';
                }


            if (!this.state.user_logging_in) {
                // Agent Referral errors
                if (errors.user_form_errors.agent_referral) {
                    document.querySelector('#agent_referral_error').style.display = 'block';
                    document.querySelector('#agent_referral_error').innerText = errors.user_form_errors.agent_referral[0];
                    valid = false;
                } else if (!errors.user_form_errors.agent_referral) {
                    document.querySelector('#agent_referral_error').style.display = 'none';
                }

                // Password errors
                if (errors.user_form_errors.password2) {
                    document.querySelector('#password_error').style.display = 'block';
                    document.querySelector('#password_error').innerText = errors.user_form_errors.password2[0];
                    valid = false;
                } else if (!errors.user_form_errors.password2) {
                    document.querySelector('#password_error').style.display = 'none';
                }
            }
        }
        return valid;
    }

    handleValidation = () => {
        if (this.state.user_logging_in) {
            return this.validateEmail();
        } else {
            return this.validateEmail() && this.validatePhone() && this.validatePassword() && this.validatePasswordMatch();
        }
    };

    validateEmail = () => {
        const re = /\S+@\S+\.\S+/;
        const email = document.querySelector('input[type=email]').value;
        if (!re.test(email)) {
            document.querySelector('#email_error').style.display = 'block';
            document.querySelector('#email_error').innerText = this.state.errorMessages.email_error;
        } else if (re.test(email)) { document.querySelector('#email_error').style.display = 'none'; }
        return re.test(email);
    }

    validatePhone = () => {
        const re = /^(\([0-9]{3}\)\s*|[0-9]{3}\-)[0-9]{3}-[0-9]{4}$/;
        const phone = document.querySelector('input[type=tel]').value;
        if (!re.test(phone)) {
            document.querySelector('#phone_error').style.display = 'block';
            document.querySelector('#phone_error').innerText = this.state.errorMessages.phone_error;
        } else if (re.test(phone)) { document.querySelector('#phone_error').style.display = 'none'; }
        return re.test(phone);
    }

    validatePassword = () => {
        const password = document.querySelector('input[name=password1]').value;
        const numberMatch = /[0-9]/;
        if (password.length < 8) {
            document.querySelector('#password_error').style.display = 'block';
            document.querySelector('#password_error').innerText = this.state.errorMessages.password_error_length;
            return false;
        } else if (!numberMatch.test(password)) {
            document.querySelector('#password_error').style.display = 'block';
            document.querySelector('#password_error').innerText = this.state.errorMessages.password_error_number;
            return false;
        }
        if (numberMatch.test(password) && !password.length < 8) { document.querySelector('#password_error').style.display = 'none'; }
        return true;
    }

    validatePasswordMatch = () => {
        const password = document.querySelector('input[name=password1]').value;
        const confirmPassword = document.querySelector('input[name=password2]').value;
        if (password !== confirmPassword) {
            document.querySelector('#password_match_error').style.display = 'block';
            document.querySelector('#password_match_error').innerText = this.state.errorMessages.password_error_match;
            return false;
        } else if (password === confirmPassword) { document.querySelector('#password_match_error').style.display = 'none'; }
        return true;
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

    setUserLoggingIn = () => {
        this.setState({
            user_logging_in: true
        })
    }

    setUserCreation = () => {
        this.setState({
            user_logging_in: false
        })
    }

    handleSubmit = (e) => {
        /**
         * Does a validation check before attempting to send form to backend
         * If the page is already loading, i.e the button is clicked then the button is
         *  disabled to prevent pressing multiple times
         */
        if (!this.props.loading) {
            if (!this.props.is_authenticated) {
                if (!this.handleValidation())
                {
                    return false;
                }
            }
            this.props.onSubmit(e, this.state)
        }
    }

    handleUpdatePhoneNumber = (phone_number) => {
        /**
         * Updates the phone_number in the state
         */
        this.setState({
            phone_number
        })
    }

    render() {
        if (!this.props.is_authenticated) {
            if (this.state.user_logging_in) {
                return (
                    <LoginUser
                        onSubmit={this.props.onSubmit}
                        onUserCreation={this.setUserCreation}
                        validateEmail={this.validateEmail}
                        handleValidation={this.handleValidation}
                        handleInputChange={this.handleInputChange}
                        handlePrevStep={this.props.handlePrevStep}
                        handleSubmit={this.handleSubmit}
                        loading={this.props.loading}
                    />
                );
            } else {
                return (
                    <NewUser
                        onSubmit={this.props.onSubmit}
                        onUserLoggingIn={this.setUserLoggingIn}
                        validateEmail={this.validateEmail}
                        validatePhone={this.validatePhone}
                        handleValidation={this.handleValidationCreation}
                        handleInputChange={this.handleInputChange}
                        validatePassword={this.validatePassword}
                        validatePasswordMatch={this.validatePasswordMatch}
                        handlePrevStep={this.props.handlePrevStep}
                        handleSubmit={this.handleSubmit}
                        loading={this.props.loading}
                        phone_number={this.state.phone_number}
                        onUpdatePhoneNumber={this.handleUpdatePhoneNumber}
                    />
                );
            }
        } else {
            return (
                <CurrentUser
                    onSubmit={this.props.onSubmit}
                    handlePrevStep={this.props.handlePrevStep}
                    handleSubmit={this.handleSubmit}
                    loading={this.props.loading}
                />
            );
        }
    }
}

const LoginUser = (props) => (
    <>
        <div className="survey-question">
            <h2>Login to see <span>your results</span>! <small>(or click <a className="login-toggle" onClick={props.onUserCreation}>here</a> to sign up)</small></h2>

            <span className="col-md-12 survey-error-message" id="email_error"></span>
            <input className="col-md-12 survey-input" type="email" name="email" placeholder="Email address" maxLength={30} onBlur={(e) => {props.validateEmail(e) && props.handleInputChange(e, 'string')} } required/>

            <span className="col-md-12 survey-error-message" id="password_error"></span>
            <input className="col-md-12 survey-input" type="password" name="password1" placeholder="Password" required onChange={props.validatePassword} onBlur={(e) => {props.validatePassword && props.handleInputChange(e, 'string')} } />
        </div>
        <div className="row survey-btn-wrapper">
            <div className="col-sm-6 col-xs-12">
                <button className="col-sm-12 survey-btn survey-btn_back" style={{marginTop: '30px'}} onClick={(e) => {props.handlePrevStep(e)}}>
                    Back
                </button>
            </div>
            <div className="col-sm-6 col-xs-12">
                <button className="col-sm-12 survey-btn" onClick={(e) => { props.handleSubmit(e); }}>
                    {props.loading ? 'Loading' : 'View'}
                </button>
            </div>
        </div>
    </>
)

const NewUser = (props) => (
    <>
        <div className="survey-question">
            <h2>Finish signing up to see <span>your results</span>! <small>(or click <a className="login-toggle" onClick={props.onUserLoggingIn}>here</a> to login)</small></h2>

            <span className="col-md-12 survey-error-message" id="email_error"></span>
            <input className="col-md-12 survey-input" type="email" name="email" placeholder="Email address" maxLength={30} onBlur={(e) => {props.validateEmail(e) && props.handleInputChange(e, 'string')} } required/>

            <span className="col-md-12 survey-error-message" id="phone_error"></span>
            <PhoneInput
                country="US"
                className="col-md-12 survey-input"
                placeholder="Enter phone number"
                value={props.phone_number }
                onChange={
                    phone => props.onUpdatePhoneNumber(phone)
                }
            />

            <span className="col-md-12 survey-error-message" id="agent_referral_error"></span>
            <input className="col-md-12 survey-input" type="text" name="agent_referral" placeholder="Agent Referral - Optional" onBlur={(e) => {props.handleInputChange(e, 'string')} } />

            <span className="col-md-12 survey-error-message" id="password_error"></span>
            <input className="col-md-12 survey-input" type="password" name="password1" placeholder="Password" required onChange={props.validatePassword} onBlur={(e) => {props.validatePassword && props.handleInputChange(e, 'string')} } />
            <span className="col-md-12 survey-error-message" id="password_match_error"></span>
            <input className="col-md-12 survey-input" type="password" name="password2" placeholder="Confirm Your Password" required onChange={props.validatePasswordMatch} onBlur={(e) => {props.validatePasswordMatch && props.handleInputChange(e, 'string')} } />
        </div>
        <div className="row survey-btn-wrapper">
            <div className="col-sm-6 col-xs-12">
                <button className="col-sm-12 survey-btn survey-btn_back" style={{marginTop: '30px'}} onClick={(e) => {props.handlePrevStep(e)}}>
                    Back
                </button>
            </div>
            <div className="col-sm-6 col-xs-12">
                <button className="col-sm-12 survey-btn" onClick={(e) => { props.handleSubmit(e); }}>
                    {props.loading ? 'Loading' : 'View'}
                </button>
            </div>
        </div>
    </>
);

const CurrentUser = (props) => (
    <div className="form-details-box">

        <h2><span>Awesome!</span> Check your best places out now.</h2>
        <img src={houseIcon} alt="Icon of a house"/>
        <div className="row survey-btn-wrapper">
            <div className="col-xs-6">
                <button className="col-sm-12 survey-btn survey-btn_back" style={{marginTop: '30px'}} onClick={(e) => { props.handlePrevStep(e)}}>
                    Back
                </button>
            </div>
            <div className="col-xs-6">
                <button className="col-sm-12 survey-btn" onClick={(e) => { props.handleSubmit(e); }}>
                    {props.loading ? 'Loading' : 'View'}
                </button>
            </div>
        </div>

    </div>
)
