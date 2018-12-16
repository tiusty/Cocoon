import React from 'react';
import { Component, Fragment } from 'react';

export default class Details extends Component {

    handleValidation = () => {
        return this.validateEmail() && this.validatePhone() && this.validatePassword() && this.validatePasswordMatch() && this.validateCreationKey();
    }

    validateEmail = () => {
        const re = /\S+@\S+\.\S+/;
        const email = document.querySelector('input[type=email]').value;
        if(re.test(email)) {
            document.getElementById('email_error').style.display = 'none';
        } else {
            document.getElementById('email_error').style.display = 'block';
        }
        return re.test(email);
    }

    validatePhone = () => {
        const re = /^(\([0-9]{3}\)\s*|[0-9]{3}\-)[0-9]{3}-[0-9]{4}$/;
        const phone = document.querySelector('input[type=tel]').value;
        if(re.test(phone)) {
            document.getElementById('phone_error').style.display = 'none';
        } else {
            document.getElementById('phone_error').style.display = 'block';
        }
        return re.test(phone);
    }

    validatePassword = () => {
        const password = document.querySelector('input[name=password1]').value;
        const numberMatch = /[0-9]/;
        const errors = [
            'Password must contain at least one number',
            'Password must be at least 8 characters.',
        ];
        if(!numberMatch.test(password)) {
            document.getElementById('password_error').innerText = errors[0];
            document.getElementById('password_error').style.display = 'block';
            return false;
        } else if(password.length < 8) {
            document.getElementById('password_error').innerText = errors[3];
            document.getElementById('password_error').style.display = 'block';
            return false;
        }
        document.getElementById('password_error').style.display = 'none';
        return true;
    }

    validatePasswordMatch = () => {
        const password = document.querySelector('input[name=password1]').value;
        const confirmPassword = document.querySelector('input[name=password2]').value;
        if(password !== confirmPassword) {
            document.getElementById('password_match_error').style.display = 'block';
            return false;
        }
        document.getElementById('password_match_error').style.display = 'none';
        return true;
    }

    validateCreationKey = () => {
        const creationKey = document.querySelector('input[name=creation_key').value;
        if(creationKey === '') {
            document.getElementById('creation_key_error').style.display = 'block';
            return false;
        }
        document.getElementById('creation_key_error').style.display = 'none';
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

    handleSubmit = (e) => {
        if (!this.props.is_authenticated) {
            if (!this.handleValidation())
            {
                return false;
            }
        }
        this.props.onSubmit(e, this.state)
    }

    render(){
        return (
            <>
                {!this.props.is_authenticated ?
                    <NewUser
                        onSubmit={this.props.onSubmit}
                        validateEmail={this.validateEmail}
                        validatePhone={this.validatePhone}
                        handleValidation={this.handleValidation}
                        handleInputChange={this.handleInputChange}
                        validatePassword={this.validatePassword}
                        validatePasswordMatch={this.validatePasswordMatch}
                        validateCreationKey={this.validateCreationKey}
                        handlePrevStep={this.props.handlePrevStep}
                        handleSubmit={this.handleSubmit}
                    /> :
                    <CurrentUser
                        onSubmit={this.props.onSubmit}
                        handlePrevStep={this.props.handlePrevStep}
                        handleSubmit={this.handleSubmit}
                    />}
            </>
        );
    }

}

const NewUser = (props) => (
    <>
        <div className="survey-question">
            <h2>Finish signing up to see <span>your results</span>!</h2>

            <span className="col-md-12 survey-error-message" id="email_error">Enter a valid email address.</span>
            <input className="col-md-12 survey-input" type="email" name="email" placeholder="Email address" maxLength={30} onBlur={(e) => {props.validateEmail(e) && props.handleInputChange(e, 'string')} } required/>

            <span className="col-md-12 survey-error-message" id="phone_error">Enter a valid phone number. Ex. (555) 555-5555</span>
            <input className="col-md-12 survey-input" type="tel" name="phone_number" placeholder="Phone Number" onBlur={(e) => { props.validatePhone(e) && props.handleInputChange(e, 'string')} } required/>

            <span className="col-md-12 survey-error-message" id="password_error"></span>
            <input className="col-md-12 survey-input" type="password" name="password1" placeholder="Password" required onChange={props.validatePassword} onBlur={(e) => {props.validatePassword && props.handleInputChange(e, 'string')} } />
            <span className="col-md-12 survey-error-message" id="password_match_error">Passwords must match.</span>
            <input className="col-md-12 survey-input" type="password" name="password2" placeholder="Confirm Your Password" required onChange={props.validatePasswordMatch} onBlur={(e) => {props.validatePasswordMatch && props.handleInputChange(e, 'string')} } />

            <span className="col-md-12 survey-error-message" id="creation_key_error">This field is required.</span>
            <input className="col-md-12 survey-input" type="text" name="creation_key" placeholder="Enter Your Key" required onChange={props.validateCreationKey} onBlur={(e) => props.handleInputChange(e, 'string')} />
        </div>
        <div className="row survey-btn-wrapper">
            <div className="col-sm-6 col-xs-12">
                <button className="col-sm-12 survey-btn survey-btn_back" style={{marginTop: '30px'}} onClick={(e) => {props.handlePrevStep(e)}}>
                    Back
                </button>
            </div>
            <div className="col-sm-6 col-xs-12">
                <button className="col-sm-12 survey-btn" onClick={(e) => { props.handleSubmit(e); }}>
                    Check out my places
                </button>
            </div>
        </div>
    </>
);

const CurrentUser = (props) => (
    <>
        <h2><span>Awesome!</span> Check your best places out now.</h2>
        <div className="row survey-btn-wrapper">
            <div className="col-md-6">
                <button className="col-md-12 survey-btn survey-btn_back" style={{marginTop: '30px'}} onClick={(e) => { props.handlePrevStep(e)}}>
                    Back
                </button>
            </div>
            <div className="col-md-6">
                <button className="col-md-12 survey-btn" onClick={(e) => { props.handleSubmit(e); }}>
                    View now
                </button>
            </div>
        </div>

    </>
)
