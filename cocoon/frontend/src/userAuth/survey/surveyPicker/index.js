import React, { Component } from 'react';
import survey_endpoints from "../../../endpoints/survey_endpoints";

export default class SurveyPicker extends Component {

    displayUserSurveys = () => {
        if (this.props.surveys.length === 0) {
            return (
                <div className="tour-picker-surveys">
                    <div className="survey-item">
                        Client has no Surveys
                    </div>
                </div>
            );
        } else {
            return (
                <div className="tour-picker-surveys">
                    {this.props.surveys && this.props.surveys.map(survey => {
                        let surveyClass = 'survey-item';
                        if (this.props.survey_id === survey.id) {
                            surveyClass += ' survey-active';
                        }
                        return (
                            <div key={survey.id} className={surveyClass}
                                 onClick={() => this.props.handleClickSurvey(survey.id)}>
                                {survey.survey_name} ({survey.favorites.length})
                            </div>
                        );
                    })}
                </div>
            );
        }
    }

    render() {
        return (
            <div className="tour-box tour-picker">
                <div className="tour-top-bar">
                    <h3>User Surveys</h3>
                </div>
                {this.displayUserSurveys()}
            </div>
        );
    }
}