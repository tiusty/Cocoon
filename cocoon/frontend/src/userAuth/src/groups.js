import React from 'react'
import { Component } from 'react';


import Survey from "./survey";

class Surveys extends Component {
    state = {
        surveys: []
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
        fetch('http://127.0.0.1:8000/survey/api/userSurveys/')
            .then(response => {
                if (response.status !== 200) {
                    console.log("something went wrong")
                }
                return response.json()
            })
            .then(data =>
                this.setState( {surveys: this.handleData(data)})
            )
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
                    />

                )}
            </React.Fragment>
        );
    }
}
export default Surveys

