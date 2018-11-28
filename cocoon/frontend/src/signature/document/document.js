// Import React Components/signatures/api/hunterDocManager/
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

class Document extends Component {
    state = {
        loaded: false,
        id: null,
        created: false,
        template_id: this.props.template_id,
        endpoint: this.props.endpoint,
        is_signed: false,
        template_type: this.props.template_type,

    };

    componentDidMount() {
        /**
         * Retrieves the document associated with this component
         */
        console.log(this.state.endpoint + this.state.template_id + '/');
        let endpoint = this.state.endpoint + this.state.template_id + '/';

        axios.get(endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                if (response.data.result) {
                    this.setState( {
                        id: response.data.id,
                        is_signed: response.data.is_signed,
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

    renderButton() {
        if(this.state.is_signed) {
            return <p>All set</p>
        }
        else if (this.state.created) {
            return (
                <button className="btn btn-secondary">Sign</button>
            );
        } else {
            return (
                <button className="btn btn-secondary">Create</button>
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
