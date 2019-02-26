import React, {Component} from 'react';
import CSRFToken from '../../../common/csrftoken';
import scheduler_endpoints from '../../../endpoints/survey_endpoints';

export default class TourSetupCTA extends Component {

    constructor(props) {
        super(props);
        this.state = {
            has_off_market: false,
            homes_off_market: 0
        }
    }

    componentDidMount = () => {
        this.checkIfOffMarket();
    }

    checkIfOffMarket = () => {
        let { visit_list } = this.props;
        let error_count = 0;
        for (let i = 0; i < visit_list.length; i++) {
            if (visit_list[i].on_market === false) {
                error_count += 1;
            }
        }
        if (error_count > 0) {
            this.setState({
                has_off_market: true,
                homes_off_market: error_count
            })
        } else {
            this.setState({
                has_off_market: false,
                homes_off_market: 0
            })
        }
    }

    determineScheduleButtonStatus() {
        if (this.props.visit_list <= 0 || this.state.has_off_market === true) {
            return true;
        } else {
            return false;
        }
    }

    handleErrorMessage = () => {
        if (this.props.visit_list <= 0) {
            return <span className="tour-error">You must have at least one home in your visit list.</span>
        } else if (this.state.has_off_market === true) {
            return  <span className="tour-error">There are homes in your visit list that are sold. Remove those to schedule your tour.</span>
        } else {
            return null;
        }
    }

    handleText = () => {
        if (this.props.loaded) {

            if (!this.props.is_pre_tour_signed && !this.props.pre_tour_forms_created && !this.props.itinerary_scheduled) {
                return (
                    <>
                        <h3>Pre-Tour Documents</h3>
                        <button onClick={this.props.onHandleOnClickCreateDocument}>
                            <i className="material-icons">send</i> Send My Documents
                        </button>
                    </>
                );
            } else if (!this.props.is_pre_tour_signed && this.props.pre_tour_forms_created && !this.props.itinerary_scheduled) {
                return (
                    <>
                        <h3>Pre-Tour Documents</h3>
                        <span onClick={this.props.onHandleOnClickRefreshDocument}>
                            <i style={{fontSize: 15}} className="material-icons">refresh</i> Refresh Status <span onClick={this.props.onHandleOnClickResendDocument} className="helper-link"> (Resend Email)</span>
                        </span>
                    </>
                );
            } else if (this.props.is_pre_tour_signed && this.props.pre_tour_forms_created && !this.props.itinerary_scheduled) {
                return (
                    <>
                        <h3>Tour Summary <span className="helper-text">({this.props.visit_list.length} homes in Visit List)</span></h3>
                        <form method="post">
                            <CSRFToken />
                            <button
                                value={this.props.survey_id}
                                disabled={this.determineScheduleButtonStatus()}
                                type="submit">
                                <i style={{fontSize: 15}} className="material-icons">schedule</i> Schedule Tour
                            </button>
                        </form>
                        {this.handleErrorMessage()}
                    </>
                );
            } else if (this.props.itinerary_scheduled) {
                return (
                    <>
                        <h3>Tour Summary <span className="helper-text">({this.props.visit_list.length} homes in Visit List)</span></h3>
                        <a href={scheduler_endpoints['clientScheduler']}>
                            <i style={{fontSize: 15}} className="material-icons">place</i> View Tour
                        </a>
                    </>
                );
            }

        }
    }

    render() {
        return (
            <div className="tour-box tour-cta">
                {this.handleText()}
            </div>
        );
    }
}