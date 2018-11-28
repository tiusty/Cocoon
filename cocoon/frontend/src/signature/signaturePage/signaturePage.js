// Import React Components/signatures/api/hunterDocManager/
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

// Import Cocoon Components
import signature_endpoints from "../../endpoints/signatures_endpoints";
import Document from "../document/document";

class SignaturePage extends Component {
    state = {
        doc_ids: [],
        hunter_doc_endpoint: signature_endpoints['hunterDoc']
    };

    parseData(data) {
        /**
         * Parses data returned from the endpoint and returns it in a nicer format for react
         *
         * Expects to be passed data a list of documents from the backend and then returns a list
         *  of the document ids.
         * @type {Array}: A list of documents
         */
        let doc_ids = [];

        // For each survey just push the id for that survey to the list
        data.map(c =>
            doc_ids.push( { id: c.id} )
        );

        // Return the list of ids
        return doc_ids
    }

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        axios.get(this.state.hunter_doc_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState( {doc_ids: this.parseData(response.data)})
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
                    {this.state.doc_ids.map(doc =>
                        <Document
                            key={doc.id}
                            id={doc.id}
                            endpoint={this.state.hunter_doc_endpoint}
                        />
                    )}
                    </tbody>
                </table>
            </div>
        );
    };
}

export default SignaturePage;
