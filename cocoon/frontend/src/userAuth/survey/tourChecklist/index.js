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
        else if (this.props.pre_tour_forms_created && this.props.is_pre_tour_signed) {
            this.setState({
                checklistActiveItem: 4
            })
        }
        else if (this.props.favorites.length > 0) {
            this.setState({
                checklistActiveItem: 3
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
                <i className="material-icons">{checkListIcon}</i> <p> Take a Survey</p>
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
                <i className="material-icons">{checkListIcon}</i> <p> Review your results to pick some favorites.</p>
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
                <i className="material-icons">{checkListIcon}</i> <p> Add up to 5 homes you'd like to tour to your visit list.</p>
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
                <i className="material-icons">{checkListIcon}</i> <p> Schedule your tour by clicking Schedule Tour above.</p>
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
                <i className="material-icons">{checkListIcon}</i> <p> Stay updated with your tour status on the <a href={scheduler_endpoints['clientScheduler']}>My Itinerary</a> page.</p>

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
                    {this.renderDocCheck()}
                    {this.renderVisitsCheck()}
                    {this.renderScheduleCheck()}
                    {this.renderItineraryCheck()}
                </div>
            </div>
        );
    }
}