// Import React Components/signatures/api/hunterDocManager/
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
                if (response.data.result) {
                    this.setState( {
                        id: response.data.serializer.id,
                        is_signed: response.data.serializer.is_signed,
                        created: true,
                    })
                } else {
                    this.setState( {
                        created: false,
                    })
                }

                this.setState({
                    loaded:true,
                })
            });
    }

    renderIsSigned() {
        if (this.state.is_signed) {
            return "Yes"
        } else {
            return "No"
        }
    }

    createDocument = () => {
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
        this.setState({
            refreshing: true,
        });
        let endpoint = this.state.endpoint + this.state.template_id + '/';
        axios.put(endpoint)
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

    renderButtonName = () => {
        if (this.state.refreshing) {
            return 'Loading'
        } else {
            if (this.state.created) {
                return 'Refresh'
            } else {
                return 'Send'
            }
        }
    };

    renderButton() {
        if(this.state.is_signed) {
            return <p>All set</p>
        }
        else if (this.state.created) {
            return (
                <button className="btn btn-secondary" onClick={this.refreshDocumentStatus}>{this.renderButtonName()}</button>
            );
        } else {
            return (
                <button className="btn btn-secondary" onClick={this.createDocument}>{this.renderButtonName()}</button>
            );
        }
    }

    render() {
        if (this.state.loaded) {
            return(
                <tr>
                    <th>{this.state.template_type}</th>
                    <th>{this.renderIsSigned()}</th>
                    <th>
                        {this.renderButton()}
                    </th>
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
