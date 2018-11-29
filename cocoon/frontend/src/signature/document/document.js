// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// For handling Post request with CSRF protection
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class Document extends Component {
    state = {
        loaded: false,
        id: null,
        created: false,
        template_id: this.props.template_id,
        endpoint: this.props.endpoint,
        is_signed: false,
        template_type: this.props.template_type,
        refreshing: false,
    };

    componentDidMount() {
        /**
         * Retrieves the document associated with this component
         */
        let endpoint = this.state.endpoint + this.state.template_id + '/';
        axios.get(endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                // If the response.data.result returns true then the document exists
                if (response.data.result) {
                    this.setState( {
                        id: response.data.serializer.id,
                        is_signed: response.data.serializer.is_signed,
                        created: true,
                    })
                // If response.data.result is not true then the document has not been created yet
                } else {
                    this.setState( {
                        created: false,
                    })
                }

                // After the data is done loading then render fields
                this.setState({
                    loaded:true,
                })
            });
    }

    renderIsSigned() {
        /**
         * Returns whether or not the document has been signed
         */
        if (this.state.is_signed) {
            return "Yes"
        } else {
            return "No"
        }
    }

    createDocument = () => {
        /**
         * Sends an API request to create the document specified by the template type
         */
        this.setState({
            refreshing: true,
        });
        let endpoint = this.state.endpoint;
        axios.post(endpoint,
            {
                template_type_id: this.state.template_id,
            })
            .catch(error => {
                this.setState({
                    refreshing: false,
                });
                console.log('Bad', error)
            })
            .then(response =>
                this.setState({
                    id: response.data.id,
                    is_signed: response.data.is_signed,
                    created: true,
                    refreshing: false,
                })
            );
        };

    refreshDocumentStatus = () => {
        /**
         * Sends an API request to update the status of the current document
         */
        this.setState({
            refreshing: true,
        });
        let endpoint = this.state.endpoint + this.state.template_id + '/';
        axios.put(endpoint,
            {
                'type': 'update'
            })
            .catch(error => {
                this.setState({
                    refreshing: false,
                });
                console.log('Bad', error)
            })
            .then(response =>
                this.setState({
                    id: response.data.id,
                    is_signed: response.data.is_signed,
                    created: true,
                    refreshing: false,
                })
            );
    };

    resendDocument = () => {
        /**
         * Sends an API request to resend the current document
         */
        this.setState({
            refreshing: true,
        });
        let endpoint = this.state.endpoint + this.state.template_id + '/';
        axios.put(endpoint,
            {
                'type': 'resend'
            })
            .catch(error => {
                this.setState({
                    refreshing: false,
                });
                console.log('Bad', error)
            })
            .then(response =>
                this.setState({
                    id: response.data.id,
                    is_signed: response.data.is_signed,
                    created: true,
                    refreshing: false,
                })
            );
    };

    renderButton() {
        /**
         * Renders the button for the current document if it isn't signed
         */
        if(this.state.is_signed && this.state.created) {
            return <p>All set</p>
        }
        else if (this.state.created) {
            if (this.state.refreshing) {
                return <button className="btn btn-secondary">Loading</button>
            } else {
                return (
                    <button className="btn btn-secondary" onClick={this.refreshDocumentStatus}>Refresh</button>
                );
            }
        } else {
            if (this.state.refreshing) {
                return <button className="btn btn-secondary">Loading</button>
            } else {
                return (
                    <button className="btn btn-secondary" onClick={this.createDocument}>Send</button>
                );
            }
        }
    }

    renderDocumentAction() {
        if(this.state.created && this.state.is_signed) {
            return 'None'
        } else if (this.state.created) {
            if (this.state.refreshing) {
                return <button className="btn btn-secondary">Loading</button>
            } else {
                return <button className="btn btn-secondary" onClick={this.resendDocument}>Resend</button>
            }
        } else {
            return 'None'
        }
    }

    render() {
        if (this.state.loaded) {
            return(
                <tr>
                    <th>{this.state.template_type}</th>
                    <th>{this.renderIsSigned()}</th>
                    <th>{this.renderButton()}</th>
                    <th>{this.renderDocumentAction()}</th>
                </tr>
            );
        } else {
            return (
                    <tr>
                        <td colSpan="0">
                            Loading
                        </td>
                    </tr>
            );
        }
    };
}

export default Document;
