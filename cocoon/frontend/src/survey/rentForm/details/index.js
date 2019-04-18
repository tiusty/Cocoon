import React from 'react';
import { Component } from 'react';

import houseIcon from './found-apt.png';

import PhoneInput from 'react-phone-number-input/basic-input'

export default class DetailsForm extends Component {
    state = {
        email: "",
        password1: "",
        password2: "",
        phone_number: '',
        user_logging_in: false,

        // errors
        login_error: "",
        email_error: "",
        password1_error: "",
        agent_referral_error: "",
        password2_error: "",
        phone_error: "",

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
        let email_error = "";
        let password1_error = "";
        let agent_referral_error = "";
        let password2_error = "";
        let login_error = "";


        if (errors.user_form_errors) {
            // Tests if there was a login error
            if (errors.user_form_errors.sign_in_failure) {
                login_error = errors.user_form_errors.sign_in_failure
            }

            // Email Errors
            if (errors.user_form_errors.email) {
                email_error = errors.user_form_errors.email[0]
            }

            // Password errors
            if (errors.user_form_errors.password1) {
                password1_error = errors.user_form_errors.password[0];
            } else if (errors.user_form_errors.password) {
                password1_error = errors.user_form_errors.password[0];
            }

            if (!this.state.user_logging_in) {
                // Agent Referral errors
                if (errors.user_form_errors.agent_referral) {
                    agent_referral_error = errors.user_form_errors.agent_referral[0];
                }

                // Password errors
                if (errors.user_form_errors.password2) {
                    password2_error = errors.user_form_errors.password2[0];
                }
            }
        }
        this.setState({
            email_error,
            password1_error,
            agent_referral_error,
            password2_error,
            login_error,
        })
    };

    handleValidation = () => {
        if (this.state.user_logging_in) {
            return this.validateEmail() && this.validatePassword();
        } else {
            return this.validateEmail() && this.validatePhone() && this.validatePassword() && this.validatePasswordMatch();
        }
    };

    validateEmail = () => {
        const re = /\S+@\S+\.\S+/;
        let email_error =  "";
        const email = document.querySelector('input[type=email]').value;
        if (!re.test(email)) {
            email_error = "You must enter in a valid email";
        }
        this.setState({
            email_error
        })
        return re.test(email);
    }

    validatePhone = () => {
        const re = /^(\([0-9]{3}\)\s*|[0-9]{3}\-)[0-9]{3}-[0-9]{4}$/;
        let phone_error = "";
        const phone = document.querySelector('input[type=tel]').value;
        if (!re.test(phone)) {
            phone_error = "Enter a valid phone number. ex. (555) 555-5555";
        }
        this.setState({
            phone_error
        })
        return re.test(phone);
    }

    validatePassword = () => {
        if (this.state.user_logging_in) {
            return this.validatePasswordLogin()
        } else {
            return this.validatePasswordUserCreation()
        }
    }

    validatePasswordLogin() {
        const password = document.querySelector('input[name=password1]').value;
        let password1_error = "";
        let valid = true;
        if (password.length <= 0) {
            password1_error = "Please enter your password";
            valid = false;
        }
        this.setState({
            password1_error
        });
        return valid;
    }

    validatePasswordUserCreation() {
        const password = document.querySelector('input[name=password1]').value;
        let password1_error = "";
        let valid = true;
        const numberMatch = /[0-9]/;
        if (password.length < 8) {
            password1_error = "Password must be at least 8 characters.";
            valid = false;
        } else if (!numberMatch.test(password)) {
            password1_error = "The password must contain at least 1 number";
            valid = false;
        }
        this.setState({
            password1_error
        })
        return valid;
    }

    validatePasswordMatch = () => {
        const password = document.querySelector('input[name=password1]').value;
        const confirmPassword = document.querySelector('input[name=password2]').value;
        let password2_error = "";
        let valid = true;
        if (password !== confirmPassword) {
            password2_error = "Passwords must match";
            valid = false;
        }
        this.setState({
            password2_error
        });
        return valid;
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
            user_logging_in: true,
            password1: "",
            password2: "",
        })
    }

    setUserCreation = () => {
        this.setState({
            user_logging_in: false,
            password1: "",
            password2: "",
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
                        login_error={this.state.login_error}
                        email_error={this.state.email_error}
                        password1_error={this.state.password1_error}

                        errors={this.state.user_form_errors}
                        onSubmit={this.props.onSubmit}
                        onUserCreation={this.setUserCreation}
                        validateEmail={this.validateEmail}
                        validatePassword={this.validatePassword}
                        handleInputChange={this.handleInputChange}
                        handlePrevStep={this.props.handlePrevStep}
                        handleSubmit={this.handleSubmit}
                        loading={this.props.loading}
                    />
                );
            } else {
                return (
                    <NewUser
                        email_error={this.state.email_error}
                        password1_error={this.state.password1_error}
                        agent_referral_error={this.state.agent_referral_error}
                        password2_error={this.state.password2_error}
                        phone_error={this.state.phone_error}


                        onSubmit={this.props.onSubmit}
                        onUserLoggingIn={this.setUserLoggingIn}
                        validateEmail={this.validateEmail}
                        validatePhone={this.validatePhone}
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
            <p className="col-md-12 survey-error-message">
            {props.login_error ? props.login_error : null}
            </p>

            <span className="col-md-12 survey-error-message">
            {props.email_error ? props.email_error : null}
            </span>
            <input className="col-md-12 survey-input" type="email" name="email" placeholder="Email address" maxLength={30} onBlur={(e) => {props.validateEmail(e) && props.handleInputChange(e, 'string')} } required/>

            <span className="col-md-12 survey-error-message">
            {props.password1_error ? props.password1_error : null}
            </span>
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

            <span className="col-md-12 survey-error-message">
            {props.email_error ? props.email_error : null}
            </span>
            <input className="col-md-12 survey-input" type="email" name="email" placeholder="Email address" maxLength={30} onBlur={(e) => {props.validateEmail(e) && props.handleInputChange(e, 'string')} } required/>

            <span className="col-md-12 survey-error-message">
            {props.phone_error ? props.phone_error : null}
            </span>
            <PhoneInput
                country="US"
                className="col-md-12 survey-input"
                placeholder="Enter phone number"
                value={props.phone_number }
                onChange={
                    phone => props.onUpdatePhoneNumber(phone)
                }
            />

            <span className="col-md-12 survey-error-message">
            {props.agent_referral_error ? props.agent_referral_error : null}
            </span>
            <input className="col-md-12 survey-input" type="text" name="agent_referral" placeholder="Agent Referral - Optional" onBlur={(e) => {props.handleInputChange(e, 'string')} } />

            <span className="col-md-12 survey-error-message">
            {props.password1_error ? props.password1_error : null}
            </span>
            <input className="col-md-12 survey-input" type="password" name="password1" placeholder="Password" required onChange={props.validatePassword} onBlur={(e) => {props.validatePassword && props.handleInputChange(e, 'string')} } />

            <span className="col-md-12 survey-error-message">
            {props.password2_error ? props.password2_error : null}
            </span>
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
