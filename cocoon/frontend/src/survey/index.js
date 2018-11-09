import React from 'react';
import { Component } from 'react';
import ReactDOM from "react-dom";

import Progress from './progress';
import General from './general';
import Tenant from './tenant';
import Amenities from './amenities';

import './survey.css';

class Survey extends Component {

    constructor(props) {
        super(props);
        this.state = {
            step: 1
        };
    }

    componentDidMount = () => {
        console.log('rendered!');
    }

    renderForm = (step) => {
        switch (step) {
            case 1:
                return <General handleNextStep={this.handleNextStep} />;
            case 2:
                return <Tenant handleNextStep={this.handleNextStep} />;
            case 3:
                return <Amenities handleNextStep={this.handleNextStep} />;
        }
    }

    handleNextStep = (e) => {
        e.preventDefault();
        this.setState({
            step: this.state.step + 1
        }, () => console.log('step: ' + this.state.step))
    }

    render(){
        return (
            <div className="survey-wrapper">
                <Progress step={this.state.step}/>
                <form action="">
                    {this.renderForm(this.state.step)}
                </form>
            </div>
        );
    }
}

ReactDOM.render(<Survey is_authenticated={window.props} />, window.react_mount);