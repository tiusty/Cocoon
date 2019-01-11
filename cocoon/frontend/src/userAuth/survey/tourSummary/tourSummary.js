// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'

// Import Cocoon Components
import CSRFToken from '../../../common/csrftoken'

export default class TourSummary extends Component {

    renderPage() {
        if (!this.props.is_pre_tour_signed && !this.props.pre_tour_forms_created) {
            return (
                <div>
                    <p>You need to sign the pre tour documents before scheduling a tour</p>
                    <button className="btn btn-primary"
                            onClick={this.props.onHandleOnClickCreateDocument}>{this.props.refreshing_document_status ? 'Loading' : 'Send'}</button>
                </div>
            );
        } else if (!this.props.is_pre_tour_signed && this.props.pre_tour_forms_created) {
            return (
                <div>
                    <p>Refresh your document stats!</p>
                    <button className="btn btn-primary"
                            onClick={this.props.onHandleOnClickRefreshDocument}>{this.props.refreshing_document_status ? 'Loading' : 'Refresh'}</button>
                    <p>Can't find the email?</p>
                    <button className="btn btn-primary"
                            onClick={this.props.onHandleOnClickResendDocument}>{this.props.refreshing_document_status ? 'Loading' : 'Resend'}</button>
                </div>
            );
        } else if (this.props.is_pre_tour_signed && this.props.pre_tour_forms_created) {
            return (
                <div>
                    <p>Estimated duration: TBD</p>
                    <p>When you are done adding homes that you want to tour click schedule! Remember you can only have one tour scheduled at a time</p>
                    <form method="post" style={{marginTop: '10px'}}>
                        <CSRFToken/>
                        <button name="submit-button"
                                className="btn btn-success"
                                value={this.props.survey_id} type="submit">Schedule!
                        </button>
                    </form>
                </div>
            );

        }
    }

    render() {
        return(
            this.renderPage()
        );
    }
}
