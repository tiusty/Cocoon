import React, {Component} from 'react';
import NoFavImg from '../no-homes.svg';
import './mainTourContent.css';
import HomeList from './homeList';
import SurveySnapshot from './surveySnapshot';
import axios from 'axios';
import scheduler_endpoints from '../../../endpoints/scheduler_endpoints';

export default class TourSetupContent extends Component {

    constructor(props) {
        super(props);
        this.state = {
            duration: 0
        }
    }

    componentDidMount() {
        this.getTourDuration();
    }

    componentDidUpdate(prevProps) {
        if (this.props.visit_list !== prevProps.visit_list) {
            if (this.props.activeSurvey.id !== undefined && this.props.activeSurvey.visit_list.length >= 0) {
                this.getTourDuration();
            }
        }
    }

    getTourDuration = () => {
        let endpoint = scheduler_endpoints['itineraryDuration'] + this.props.activeSurvey.id;
        axios.get(endpoint)
            .catch(error => {
                console.log('BAD', error);
            })
            .then(response => {
                this.setState({
                    duration: response.data.duration
                })
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
            if (this.props.viewing_snapshot === false) {
                return (
                    <>
                        <ContentTopBar
                            activeSurvey={this.props.activeSurvey}
                            viewing_snapshot={this.props.viewing_snapshot}
                            handleSnapshotClick={this.props.handleSnapshotClick}
                            duration={this.state.duration}
                        />
                        <HomeList
                            activeSurvey={this.props.activeSurvey}
                            activeResultsUrl={this.props.activeResultsUrl}
                            visit_list={this.props.visit_list}
                            favorites={this.props.favorites}
                            handleHomeClick={this.props.handleHomeClick}
                            handleCloseHomeTileLarge={this.props.handleCloseHomeTileLarge}
                            handleVisitClick={this.props.handleVisitClick}
                            handleFavoriteClick={this.props.handleFavoriteClick}
                            clicked_home={this.props.clicked_home}
                            viewing_home={this.props.viewing_home}
                        />
                    </>
                );
            } else if (this.props.viewing_snapshot === true) {
                return (
                   <>
                       <ContentTopBar
                            activeSurvey={this.props.activeSurvey}
                            viewing_snapshot={this.props.viewing_snapshot}
                            handleSnapshotClick={this.props.handleSnapshotClick}
                            duration={this.state.duration}
                        />
                        <SurveySnapshot
                            activeSurvey={this.props.activeSurvey}
                            deleteSurvey={this.props.deleteSurvey}
                        />
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
            <h3>{props.activeSurvey.survey_name} <span className="helper-text">({props.activeSurvey.favorites.length} Favorites)</span> | Estimated Tour Duration: {Math.round(props.duration/60)} min.</h3>
        </div>
        <div className="snapshot-button" onClick={props.handleSnapshotClick}>
            <h3>Survey Snapshot
                <i className="material-icons">
                    {props.viewing_snapshot ? 'expand_less' : 'expand_more'}
                </i>
            </h3>
        </div>
    </div>
);