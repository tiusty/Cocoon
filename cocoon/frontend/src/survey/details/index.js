import React from 'react';
import { Component, Fragment } from 'react';

export default class Details extends Component {

    handleValidation = () => {
        return this.validateEmail() && this.validatePhone();
    }

    validateEmail = (e) => {
        const re = /\S+@\S+\.\S+/;
        const email = document.querySelector('input[type=email]').value;
        if(re.test(email)) {
            document.getElementById('email_error').style.display = 'none';
        } else {
            document.getElementById('email_error').style.display = 'block';
        }
        return re.test(email);
    }

    validatePhone = (e) => {
        const re = /^(\([0-9]{3}\)\s*|[0-9]{3}\-)[0-9]{3}-[0-9]{4}$/;
        const phone = document.querySelector('input[type=tel]').value;
        if(re.test(phone)) {
            document.getElementById('phone_error').style.display = 'none';
        } else {
            document.getElementById('phone_error').style.display = 'block';
        }
        return re.test(phone);
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
                    /> :
                    <CurrentUser
                        onSubmit={this.props.onSubmit}
                    />}
            </>
        );
    }

}

const NewUser = (props) => (
    <form method="POST">
        <div className="survey-question">
            <h2>Finish signing up to see <span>your results</span>!</h2>
            <span className="col-md-12 survey-error-message" id="email_error">Enter a valid email address.</span>
            <input className="col-md-12 survey-input" type="email" name="username" placeholder="Email address" maxLength={30} onBlur={props.validateEmail} required/>
            <span className="col-md-12 survey-error-message" id="phone_error">Enter a valid phone number. Ex. (555) 555-5555</span>
            <input className="col-md-12 survey-input" type="tel" name="phone_number" placeholder="Phone Number" onBlur={props.validatePhone} required/>
            <input className="col-md-12 survey-input" type="password" name="password" placeholder="Password" required/>
            <button className="col-md-12 survey-btn" onClick={(e) => { props.handleValidation() && props.onSubmit(e); }}>
                Check out my places
            </button>
        </div>
    </form>
);

const CurrentUser = (props) => (
    <>
        <h2><span>Awesome!</span> Check your best places out now.</h2>
        <button className="col-md-12 survey-btn" onClick={() => props.onSubmit()}>
            View now
        </button>
    </>
)
