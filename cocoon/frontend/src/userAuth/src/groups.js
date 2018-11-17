import React from 'react'
import { Component } from 'react';


import Survey from "./survey";

class Surveys extends Component {
    state = {
        surveys: [
            {id: 1},
            {id: 2},
        ]
    };

    constructor(props) {
        super(props);
        console.log('App - Constructor', this.props)
    }

    componentDidMount() {
        // Ajax call
        console.log('App - Mounted')
    }

    handleDelete = (counterId) => {
        const surveys = this.state.surveys.filter(c => c.id !== counterId);
        this.setState({ surveys });
    };

    render() {
        console.log('App - Rendered')
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

