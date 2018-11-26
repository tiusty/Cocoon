import React from 'react';
import { Component, Fragment } from 'react';

export default class Details extends Component {

    render(){
        return (
            <>
                {!this.props.is_authenticated ?
                    <NewUser
                        onSubmit={this.props.onSubmit}
                    /> :
                    <CurrentUser
                        onSubmit={this.props.onSubmit}
                    />}
            </>
        );
    }

}

const NewUser = (props) => (
    <form>
        <div className="survey-question">
            <h2>Finish signing up to see <span>your results</span>!</h2>
            <input className="col-md-12 survey-input" type="email" name="username" placeholder="Email address" maxLength={30} required/>
            <input className="col-md-12 survey-input" type="tel" name="phone_number" placeholder="Phone Number" required/>
            <input className="col-md-12 survey-input" type="password" name="password" placeholder="Password" required/>
            <button className="col-md-12 survey-btn" onClick={() => props.onSubmit()}>
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
