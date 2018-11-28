// Import React Components/signatures/api/hunterDocManager/
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import signature_endpoints from "../../endpoints/signatures_endpoints";
import Document from "../document/document";

class SignaturePage extends Component {
    state = {
        template_types: [],
        hunter_doc_template_endpoint: signature_endpoints['hunterDocTemplate'],
        hunter_doc_endpoint: signature_endpoints['hunterDoc'],
    };

    componentDidMount() {
        /**
         *  Retrieves all the template types
         */
        axios.get(this.state.hunter_doc_template_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState( {template_types: response.data })
            });

    }

    render() {
        return (
            <div>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Document Type</th>
                            <th scope="col">Is_signed?</th>
                            <th scope="col">Document Status</th>
                        </tr>
                    </thead>
                    <tbody>
                    {this.state.template_types.map(template =>
                        <Document
                            key={template.id}
                            template_id={template.id}
                            endpoint={this.state.hunter_doc_endpoint}
                            template_type={template.template_type}
                        />
                    )}
                    </tbody>
                </table>
            </div>
        );
    };
}

export default SignaturePage;
