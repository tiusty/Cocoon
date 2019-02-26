import React, {Component} from 'react';
import NoFavImg from '../no-homes.svg';

export default class TourSetupContent extends Component {

    constructor(props) {
        super(props);
        this.state = {
            viewing_snapshot: false,
            active_survey: undefined
        }
    }

    componentDidMount() {
        this.setActiveSurvey();
    }

    componentDidUpdate(prevProps) {
        if (this.props.survey_clicked_id !== prevProps.survey_clicked_id) {
            this.setActiveSurvey();
        }
    }

    setActiveSurvey = () => {
        let active_survey = this.props.surveys.find(s => s.id = this.props.survey_clicked_id);
        this.setState({
            active_survey: active_survey
        })
    }

    renderContent = () => {
        if (this.props.favorites.length === 0) {
            return (
                <div className="tour-content_no-favorites">
                    <img src={NoFavImg} alt="No Homes in your favorites."/>
                    <h2>There’s no homes in your favorites.</h2>
                    <p>Review your <a href={this.props.activeResultsUrl}>results</a> to pick your favorites.</p>
                </div>
            );
        } else if (this.props.favorites.length > 0) {
            if (this.state.viewing_snapshot === false) {
                return (
                    <>
                        <ContentTopBar active_survey={this.state.active_survey} />
                        {/*<HomeList />*/}
                    </>
                );
            } else if (this.state.viewing_snapshot === true) {
                return (
                   <>
                       <ContentTopBar active_survey={this.state.active_survey} />
                        {/*<SurveySnapShot />*/}
                   </>
                );
            }
        }
    }

    render() {
        return (
            <>
                {this.renderContent()}
            </>
        );
    }
}

const ContentTopBar = (props) => (
    <div className="content-top-bar">
        <div className="content-tour-info">
            <h3>{props.active_survey.survey_name} <span className="helper-text">({props.active_survey.favorites.length} Favorites)</span> | Estimated Tour Duration: 20 min.</h3>
        </div>
        <div className="snapshot-button">
            <h3>Survey Snapshot <i className="material-icons">expand_more</i></h3>
        </div>
    </div>
);