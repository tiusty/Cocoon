import React from 'react'
import { Component } from 'react';
import axios from 'axios'


import Survey from "./survey";
import userAuth_endpoints from "../../endpoints/userAuth_endpoints"

class Surveys extends Component {
    state = {
        surveys: [],
        endpoint: userAuth_endpoints['userSurveys'],
    };

    constructor(props) {
        super(props);
    }

    handleData(data) {
        let survey_ids = [];
        data.map(c =>
            survey_ids.push( { id: c.id} )
        );
        return survey_ids
    }

    componentDidMount() {
        // Ajax call
        axios.get(this.state.endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState( {surveys: this.handleData(response.data)})
            })
    }

    handleDelete = (counterId) => {
        const surveys = this.state.surveys.filter(c => c.id !== counterId);
        this.setState({ surveys });
    };

    render() {
        return (
            <React.Fragment>
                { this.state.surveys.map(survey =>
                    <Survey
                        key={survey.id}
                        onDelete={this.handleDelete}
                        survey_id={survey.id}
                        endpoint={this.state.endpoint}
                    />

                )}
            </React.Fragment>
        );
    }
}
export default Surveys

