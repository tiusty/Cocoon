// Import React Components/signatures/api/hunterDocManager/
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

class Document extends Component {
    state = {
        loaded: false,
        id: null,
        template_id: this.props.template_id,
        endpoint: this.props.endpoint,
        is_signed: false,
        template_type: '',

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
                this.setState( {
                    id: response.data.id,
                    template_type: response.data.template.template_type,
                    is_signed: response.data.is_signed
                })
            });

        // Now the page has all the necessary data loaded
        this.setState({
            loaded: true,
        })
    }

    renderIsSigned() {
        if (this.state.is_signed) {
            return "Yes"
        } else {
            return "No"
        }
    }

    renderButton() {
        return (
            <button className="btn btn-secondary">Sign</button>
        );
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
