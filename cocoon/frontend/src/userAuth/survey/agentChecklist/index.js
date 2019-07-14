import React, {Component} from 'react';
import survey_endpoints from '../../../endpoints/survey_endpoints';
import scheduler_endpoints from "../../../endpoints/scheduler_endpoints";

export default class TourChecklist extends  Component {
    constructor(props) {
        super(props);
        this.state = {
            checklistActiveItem: 1
        }
    }

    componentDidMount() {
        this.handleChecklistNumber();
    }

    componentDidUpdate(prevProps, ) {
        if (this.props.surveys !== prevProps.surveys || this.props.favorites !== prevProps.favorites || this.props.is_pre_tour_signed !== prevProps.is_pre_tour_signed || this.props.visit_list !== prevProps.visit_list) {
            this.handleChecklistNumber();
        }
    }

    handleChecklistNumber = () => {
        if (this.props.itinerary_scheduled) {
            this.setState({
                checklistActiveItem: 6
            })
        }
        else if (this.props.pre_tour_forms_created && this.props.is_pre_tour_signed && this.props.favorites.length > 0 && this.props.visit_list.length > 0) {
            this.setState({
                checklistActiveItem: 5
            })
        }
        // Skipping step 3 since we are disabling the pre tour documents for now
        // else if (this.props.pre_tour_forms_created && this.props.is_pre_tour_signed) {
        //     this.setState({
        //         checklistActiveItem: 4
        //     })
        // }
        else if (this.props.favorites.length > 0) {
            this.setState({
                checklistActiveItem: 4
            })
        }
        else if (this.props.surveys.length > 0) {
            this.setState({
                checklistActiveItem: 2
            })
        }
    };

    renderSurveyCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.state.checklistActiveItem === 1) {
            checkListClass += ' checklist-item_active';
        } else if (this.state.checklistActiveItem > 1) {
            checkListClass += ' checklist-item_checked';
            checkListIcon = 'check_box';
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Have your client take a Survey</p>
            </div>
        );
    }

    renderFavoritesCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.state.checklistActiveItem === 2) {
            checkListClass += ' checklist-item_active';
        } else if (this.state.checklistActiveItem > 2) {
            checkListClass += ' checklist-item_checked';
            checkListIcon = 'check_box';
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Either set favorites or have you client set favorites</p>
            </div>
        );
    }

    renderDocCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.state.checklistActiveItem === 3) {
            checkListClass += ' checklist-item_active';
        } else if (this.state.checklistActiveItem > 3) {
            checkListClass += ' checklist-item_checked';
            checkListIcon = 'check_box';
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Sign the pre-tour documents.</p>
            </div>
        );
    }

    renderVisitsCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.state.checklistActiveItem === 4) {
            checkListClass += ' checklist-item_active';
        } else if (this.state.checklistActiveItem > 4) {
            checkListClass += ' checklist-item_checked';
            checkListIcon = 'check_box';
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Make sure there are up to 5 homes on the visit list.</p>
            </div>
        );
    }

    renderScheduleCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.state.checklistActiveItem === 5) {
            checkListClass += ' checklist-item_active';
        }else if (this.state.checklistActiveItem > 5) {
            checkListClass += ' checklist-item_checked';
            checkListIcon = 'check_box';
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Have your client schedule a tour</p>
            </div>
        );
    }

    renderItineraryCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.state.checklistActiveItem === 6) {
            checkListClass += ' checklist-item_active';
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Your client already has a tour scheduled view by going to the agent portal <a href={scheduler_endpoints['agentSchedulerPortal']}>page</a>.</p>

            </div>
        );
    }

    render() {
        return (
            <div className="tour-box tour-checklist">
                <div className="tour-top-bar">
                    <h3>Tour Setup Tasks</h3>
                </div>
                <div className="tour-checklist-items">
                    {this.renderSurveyCheck()}
                    {this.renderFavoritesCheck()}
                    {/*{this.renderDocCheck()}*/}
                    {this.renderVisitsCheck()}
                    {this.renderScheduleCheck()}
                    {this.renderItineraryCheck()}
                </div>
            </div>
        );
    }
}