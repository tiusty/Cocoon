import React from 'react'
import { Component } from 'react';


import Survey from "./survey";

class RoommateGroup extends Component {
    state = {
        surveys: [
            {
                id: 1,
                name: "Roommate Group: Me, and Tomas",
                favorites:  [
                    {
                        id: 1,
                        address: "12 Stony Brook Rd",
                        commute_type: "Driving",
                        grade: 'A',
                        price: 1500,
                        images: ['/media/houseDatabase/30/30_12_x0GmdOn.jpg', '/media/houseDatabase/30/30_11_uZOt5KX.jpg'],
                    } ,
                    {
                        id: 2,
                        address: "48 Stony Brook Rd",
                        commute_type: "Driving",
                        images: ['/media/houseDatabase/30/30_11_uZOt5KX.jpg'],
                    } ,
                ],
                visit_list:  [
                    {
                        id: 1,
                        address: "36 Stony Brook Rd",
                        commute_type: "Driving",
                        images: [],
                    } ,
                ],
            },
            {id: 2,
                name: "Second Survey",
                favorites: [],
                visit_list: [],
            },
        ]
    };

    constructor(props) {
        super(props);
        console.log('App - Constructor', this.props)
    }

    componentDidMount() {
        // Ajax call
        console.log('App - Mounted')
    }

    handleDelete = (counterId) => {
        const surveys = this.state.surveys.filter(c => c.id !== counterId);
        this.setState({ surveys });
    };

    render() {
        console.log('App - Rendered')
        return (
            <React.Fragment>
                { this.state.surveys.map(survey =>
                    <Survey
                        key={survey.id}
                        onDelete={this.handleDelete}
                        survey={survey}
                    />

                )}
            </React.Fragment>
        );
    }
}
export default RoommateGroup

