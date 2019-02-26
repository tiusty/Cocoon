import React, {Component} from 'react';
import survey_endpoints from '../../../endpoints/survey_endpoints';

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
        if (this.props.surveys.length > 0) {
            this.setState({
                checklistActiveItem: 2
            })
        }
        if (this.props.favorites.length > 0) {
            this.setState({
                checklistActiveItem: 3
            })
        }
        if (this.props.pre_tour_forms_created && this.props.is_pre_tour_signed) {
            this.setState({
                checklistActiveItem: 4
            })
        }
        if (this.props.favorites.length > 0 && this.props.is_pre_tour_signed && this.props.visit_list.length > 0) {
            this.setState({
                checklistActiveItem: 5
            })
        }
    }

    renderSurveyCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.state.checklistActiveItem === 1) {
            checkListClass += ' checklist-item_active';
        } else if (this.state.checklistActiveItem > 1) {
            checkListClass += ' checklist-item_checked';
            checkListIcon = 'check_box'
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Take a<a href={survey_endpoints['rentingSurvey']}> Survey</a></p>
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
            checkListIcon = 'check_box'
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Review your <a href={this.props.activeResultsUrl}>results</a> to pick some favorites.</p>
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
            checkListIcon = 'check_box'
        }
        let clickFunction = undefined;
        if (!this.props.pre_tour_forms_created) {
            clickFunction = this.props.onHandleOnClickCreateDocument;
        } else {
            clickFunction = this.props.onHandleOnClickResendDocument;
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Sign the pre-tour <span onClick={clickFunction}>documents</span>.</p>
            </div>
        );
    }

    renderVisitsCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.state.checklistActiveItem === 3) {
            checkListClass += ' checklist-item_active';
        } else if (this.state.checklistActiveItem > 3) {
            checkListClass += ' checklist-item_checked';
            checkListIcon = 'check_box'
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Add homes you'd like to tour to your visit list.</p>
            </div>
        );
    }

    renderScheduleCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.state.checklistActiveItem === 3) {
            checkListClass += ' checklist-item_active';
        } else if (this.state.checklistActiveItem > 3) {
            checkListClass += ' checklist-item_checked';
            checkListIcon = 'check_box'
        }
        return (
            <div className={checkListClass}>
                <i className="material-icons">{checkListIcon}</i> <p> Schedule a tour of your visit list.</p>
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
                </div>
            </div>
        );
    }
}