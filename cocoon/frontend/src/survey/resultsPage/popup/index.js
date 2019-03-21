import React, { Component } from 'react';
import './popup.css';
import ErrorImg from './modal_error.svg';
import SuccessImg from './modal_success.svg';
import InfoImg from './modal_info.svg';

export default class PopUp extends Component {
    /**
     *  State:
     *  popupType: Determines what type of popup to render - 'error', 'success', or 'info
     *
     *  popupReason: Used for headline of popup and to determine which text to render
     *      'Low Scores', 'Low Number of Homes', 'Protip', 'Congrats!'
     */
    constructor(props) {
        super(props);
        this.state = {
            popupType: 'error',
            popupReason: 'Low Scores'
        }
    }

    componentDidMount() {
        this.determinePopupType();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.homeList !== this.props.homeList || prevProps.survey !== this.props.survey) {
            this.determinePopupType();
        }
    }

    getNumberOfScoresOverFifty = (homes) => {
        let number_of_scores_above_fifty = 0;
        for (let i = 0; i < homes.length; i++) {
            if (homes[i].percent_match >= 50) {
                number_of_scores_above_fifty += 1;
            }
        }
        return number_of_scores_above_fifty;
    }

    getNumberOfGreatMatches = (homes) => {
        let number_of_great_matches = 0;
        for (let i = 0; i < homes.length; i++) {
            if (homes[i].percent_match >= 90) {
                number_of_great_matches += 1;
            }
        }
        return number_of_great_matches;
    }

    determinePopupType = () => {
        const { homeList } = this.props;
        if (homeList.length <= 10) {
            this.setState({
                popupType: 'error',
                popupReason: 'Low Number of Homes'
            })
            return;
        } else if (homeList && this.getNumberOfScoresOverFifty(homeList) <= 5) {
            this.setState({
                popupType: 'error',
                popupReason: 'Low Scores'
            })
            return;
        } else if (homeList && this.getNumberOfGreatMatches(homeList) > 15) {
            this.setState({
                popupType: 'info',
                popupReason: 'Protip'
            })
            return;
        } else {
            if (this.props.homeList) {
                this.setState({
                    popupType: 'success',
                    popupReason: 'Congrats!'
                })
            }
        }

    }

    handleImageSource = () => {
        const { popupType } = this.state;
        let imageSource = ErrorImg;
        if (popupType === 'success') {
            imageSource = SuccessImg;
        } else if (popupType === 'info') {
            imageSource = InfoImg;
        }
        return imageSource;
    }

    handleButtonStyle = () => {
        const { popupType } = this.state;
        let style = { background: 'var(--red)' };
        if (popupType === 'success' || popupType === 'info') {
            style = { background: 'var(--teal)' };
        }
        return style;
    }

    handleText = () => {
        const { popupReason } = this.state;
        const { homeList } = this.props;
        if (popupReason === 'Low Scores') {
            let homeCount = this.getNumberOfScoresOverFifty(homeList);
            return (
                <p>After checking your results we noticed that you have only {homeCount} {homeCount > 1 ? 'homes ' : 'home '}
                    above 50. This is due to not being able to find homes that meet
                    your constraints. Please make changes to increase the scoring
                    such as increasing the price range, reducing amenities requirements, changing commute requirements etc.
                </p>
            );
        } else if (popupReason === 'Low Number of Homes') {
            if (this.props.survey.generalInfo.move_weight === 0 || this.props.survey.generalInfo.move_weight === 1) {
                return (
                    <>
                        <p>
                            After checking your results we noticed that not many homes
                            showed up for your criteria. Since you’re not in a rush, we
                            recommend that you subscribe to this survey by clicking
                            "Keep me updated" so you’re notified the moment something comes online!
                        </p>
                        <p>Alternatively, to fix this please increase the
                            price range, commute range/type, polygons etc to add more
                            homes.
                        </p>
                    </>
                );
            } else {
                return (
                    <p>After checking your results we noticed that not many homes
                    showed up for your criteria. To fix this please increase the
                    price range, commute range/type, polygons etc to add more
                    homes. Alternatively you may subscribe to the survey by clicking
                    "Keep me updated" and you will be notified when more homes show up.</p>
                );
            }
        } else if (popupReason === 'Protip') {
            return (
                <p>
                    We noticed you had a ton of great matches. To separate them
                    out more you should increase the restrictions of your survey
                    so your perfect home stands out!
                </p>
            );
        } else if (popupReason === 'Congrats!') {
            return (
                <p>
                    We found a bunch of homes that we think you'll like!
                    Look through them and pick your favorites. Hope you enjoy.
                </p>
            );
        }
    }

    renderButtons = () => {
        const { popupReason } = this.state;
        if (popupReason === 'Low Scores' || popupReason === 'Low Number of Homes' || popupReason === 'Protip') {
            return (
                <>
                    <button
                        onClick={this.props.editSurvey}
                        className="popup-primary"
                        style={this.handleButtonStyle()}>
                            Edit Survey
                    </button>
                    <button
                        onClick={this.props.handlePopupClose}
                        className="popup-close">
                            View Homes
                    </button>
            </>
            );
        } else {
            return (
                <button
                    onClick={this.props.handlePopupClose}
                    className="popup-primary"
                    style={this.handleButtonStyle()}>
                        View Homes
                    </button>
            );
        }
    }

    render() {
        return (
            <div className="popup-container">
                <div className="popup-wrapper">
                    <img src={this.handleImageSource()} alt="Popup Icon"/>
                    <h2>{this.state.popupReason}</h2>
                    {this.handleText()}
                    {this.renderButtons()}
                </div>
            </div>
        );
    }
}