import React, { Component } from 'react';

export default class UserPicker extends Component {

    render() {
        return (
            <div className="tour-box tour-picker">
                <div className="tour-top-bar">
                    <h3>My Clients</h3>
                </div>
                <div className="tour-picker-surveys">
                    {this.props.surveys && this.props.surveys.map(survey => {
                        let surveyClass = 'survey-item';
                        if (this.props.survey_id === survey.id) {
                            surveyClass += ' survey-active';
                        }
                        return (
                            <div key={survey.id} className={surveyClass} onClick={() => this.props.handleClickSurvey(survey.id)}>
                                {survey.survey_name} ({survey.favorites.length})
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }
}