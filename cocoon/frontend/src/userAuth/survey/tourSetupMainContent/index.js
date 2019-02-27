import React, {Component} from 'react';
import NoFavImg from '../no-homes.svg';
import './mainTourContent.css';
import HomeList from './homeList';

export default class TourSetupContent extends Component {

    constructor(props) {
        super(props);
        this.state = {
            viewing_snapshot: false,
            clicked_home: undefined,
            viewing_home: false
        }
    }

    handleHomeClick = (id) => {
        this.setState({
            clicked_home: id,
            viewing_home: true
        })
    }

    handleCloseHomeTileLarge = () => {
        this.setState({
            clicked_home: undefined,
            viewing_home: false
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
                        <ContentTopBar activeSurvey={this.props.activeSurvey} />
                        <HomeList
                            activeSurvey={this.props.activeSurvey}
                            visit_list={this.props.visit_list}
                            favorites={this.props.favorites}
                            handleHomeClick={this.handleHomeClick}
                            handleCloseHomeTileLarge={this.handleCloseHomeTileLarge}
                            handleVisitClick={this.props.handleVisitClick}
                            handleFavoriteClick={this.props.handleFavoriteClick}
                        />
                    </>
                );
            } else if (this.state.viewing_snapshot === true) {
                return (
                   <>
                       <ContentTopBar activeSurvey={this.props.activeSurvey} />
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
            <h3>{props.activeSurvey.survey_name} <span className="helper-text">({props.activeSurvey.favorites.length} Favorites)</span> | Estimated Tour Duration: 20 min.</h3>
        </div>
        <div className="snapshot-button">
            <h3>Survey Snapshot <i className="material-icons">expand_more</i></h3>
        </div>
    </div>
);