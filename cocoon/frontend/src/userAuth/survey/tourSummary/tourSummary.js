// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'

// Import Cocoon Components
import CSRFToken from '../../../common/csrftoken'

export default class TourSummary extends Component {
    state = {

    }

    renderPage() {
        if (!this.props.loaded) {
            return <p>Loading</p>
        } else if (!this.props.is_pre_tour_signed && !this.props.pre_tour_forms_created) {
            return (
                <>
                    <p>You need to sign the pre tour documents before scheduling a tour</p>
                    <button className="btn btn-primary"
                            onClick={this.props.onHandleOnClickCreateDocument}>{this.props.refreshing_document_status ? 'Loading' : 'Send'}</button>
                </>
            );
        } else if (!this.props.is_pre_tour_signed && this.props.pre_tour_forms_created) {
            return (
                <>
                    <p>Refresh your document stats!</p>
                    <button className="btn btn-primary"
                            onClick={this.props.onHandleOnClickRefreshDocument}>{this.props.refreshing_document_status ? 'Loading' : 'Refresh'}</button>
                    <p>Can't find the email?</p>
                    <button className="btn btn-primary"
                            onClick={this.props.onHandleOnClickResendDocument}>{this.props.refreshing_document_status ? 'Loading' : 'Resend'}</button>
                </>
            );
        } else if (this.props.is_pre_tour_signed && this.props.pre_tour_forms_created && this.props.survey_id === undefined) {
            return(
                <>
                    <p>Please expand a survey to get started scheduling a tour</p>
                    <p>Remember you may only have one tour scheduled at a time</p>
                </>
            );

        } else if (this.props.is_pre_tour_signed && this.props.pre_tour_forms_created && this.props.survey_id !== undefined) {
            return (
                <>
                    <p>When you are done adding homes that you want to tour, click schedule!</p>
                    <p>Remember you can only have one tour scheduled at a time</p>
                    <p>Estimated duration: TBD</p>
                    <form method="post" style={{marginTop: '10px'}}>
                        <CSRFToken/>
                        <button name="submit-button"
                                className="btn btn-success"
                                value={this.props.survey_id} type="submit">Schedule!
                        </button>
                    </form>
                </>
            );

        }
    }

    render() {
        return(
            <div className="tour-summary">
                <h2 className="surveys-title">Tour Summary</h2>
                {this.renderPage()}
            </div>
        );
    }
}
