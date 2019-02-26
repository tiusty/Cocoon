import React, {Component} from 'react';

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
        } else if (this.props.favorites.length > 0) {
            this.setState({
                checklistActiveItem: 3
            })
        } else if (this.props.is_pre_tour_signed) {
            this.setState({
                checklistActiveItem: 4
            })
        } else if (this.props.visit_list.length > 0) {
            this.setState({
                checklistActiveItem: 5
            })
        }
    }

    renderSurveyCheck = () => {
        let checkListClass = 'checklist-item';
        let checkListIcon = 'check_box_outline_blank';
        if (this.props.surveys.length > 0) {
            checkListClass += ' checklist-item_checked';
        }
        return (
            <div className={checkListClass}>
                 <i className="material-icons">check_box_outline_blank</i>
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
                </div>
            </div>
        );
    }
}