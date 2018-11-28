// Import React Components/signatures/api/hunterDocManager/
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import signature_endpoints from "../../endpoints/signatures_endpoints";

class Document extends Component {
    state = {
        loaded: false,
        id: this.props.id,
        endpoint: this.props.endpoint,
        is_signed: false,
        template_type: '',

    };

    componentDidMount() {
        /**
         * Retrieves the document associated with this component
         */
        console.log(this.state.endpoint + this.state.id + '/');
        let endpoint = this.state.endpoint + this.state.id + '/';
        axios.get(endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState( {
                    template_type: response.data.template.template_type,
                    is_signed: response.data.is_signed
                })
            });
        this.setState({
            loaded: true,
        })
    }

    renderIsSigned() {
        if (this.state.is_signed) {
            return "YES!"
        } else {
            return "No"
        }
    }

    render() {
        return(
            <tr>
                <th>{this.state.template_type}</th>
                <th>{this.renderIsSigned()}</th>
                <th>
                    <button className="btn btn-secondary">Sign</button>
                </th>
            </tr>
        );
    };
}

export default Document;
