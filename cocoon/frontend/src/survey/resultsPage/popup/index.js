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
     */
    constructor(props) {
        super(props);
        this.state = {
            popupType: 'error',
            popupReason: 'Low Scores'
        }
    }

    componentDidMount() {
        console.log(this.props.homeList)
        console.log(this.props.survey)
    }

    componentDidUpdate(prevProps) {
        if (prevProps.homeList !== this.props.homeList || prevProps.survey !== this.props.survey) {
            console.log(this.props.homeList)
            console.log(this.props.survey)
        }
    }

    determinePopupType = () => {

        if (this.props.homeList.length <= 15) {
            this.setState({
                popupType: 'error',
                popupReason: 'Low Number of Homes'
            })
            return;
        }

        if (this.props.homeList) {
            let number_of_scores_above_fifty = 0;
            for (let i = 0; i < this.props.homeList.length; i++) {

            }
            if (number_of_scores_above_fifty <= 5) {
                this.setState({
                    popupType: 'error',
                    popupReason: 'Low Scores'
                })
            }
            return;
        }

        if (this.props.homeList) {
            let number_of_great_matches = 0;
            for (let i = 0; i < this.props.homeList.length; i++) {

            }
            if (number_of_great_matches > 10) {
                this.setState({
                    popupType: 'info',
                    popupReason: 'Protip'
                })
            }
            return;
        }

        if (this.props.homeList) {
            this.setState({
                popupType: 'success',
                popupReason: 'Congrats!'
            })
        }

    }

    handleImageSource = () => {
        let imageSource = ErrorImg;
        if (this.state.popupType === 'success') {
            imageSource = SuccessImg;
        } else if (this.state.popupType === 'info') {
            imageSource = InfoImg;
        }
        return imageSource;
    }

    handleButtonStyle = () => {
        let style = { background: 'var(--red)' };
        if (this.state.popupType === 'success') {
            style = { background: 'var(--teal)' };
        } else if (this.state.popupType === 'info') {
            style = { background: 'var(--darkBlue)' };
        }
        return style;
    }

    render() {
        return (
            <div className="popup-container">
                <div className="popup-wrapper">
                    <img src={this.handleImageSource()} alt="Popup Icon"/>
                    <h2>Low Scores</h2>
                    <p>After checking your results we noticed that you have only 2 homes above 50. This is due to not being able to find homes that meet your constraints. Please make changes to increase the scoring/add more homes such as increasing the price range, reducing amenities requirements, changing commute requirements etc.</p>
                    <button
                        onClick={this.props.handlePopupPrimary}
                        className="popup-primary"
                        style={this.handleButtonStyle()}>
                            Edit Survey
                    </button>
                    <button
                        onClick={this.props.handlePopupClose}
                        className="popup-close">
                            Cancel
                    </button>
                </div>
            </div>
        );
    }
}