import React from 'react'
import { Component } from 'react';
import axios from 'axios'


import Survey from "./survey";
import survey_endpoints from "../../endpoints/survey_endpoints";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class Surveys extends Component {
    state = {
        surveys: [],
        endpoint: survey_endpoints['rentSurvey'],
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

    handleDelete = (survey_id) => {
        let endpoint = this.state.endpoint + survey_id + "/";
        axios.put(endpoint,
            {
                survey_id: survey_id,
                type: 'survey',
            })
            .catch(error => console.log('Bad', error))
            .then(response => {
               this.setState( {surveys: this.handleData(response.data)})
            });
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

