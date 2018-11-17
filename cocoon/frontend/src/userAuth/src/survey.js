import React from 'react'
import { Component } from 'react';
import HomeTile from "./homeTile";

import './survey.css'

class Survey extends Component {
    state = {
        id: this.props.survey_id,
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
            {
                id: 3,
                address: "36 Stony Brook Rd",
                commute_type: "Driving",
                images: ['/media/houseDatabase/30/30_12_x0GmdOn.jpg', '/media/houseDatabase/30/30_11_uZOt5KX.jpg'],
            } ,
            {
                id: 4,
                address: "48 Stony Brook Rd",
                commute_type: "Driving",
                images: ['/media/houseDatabase/30/30_11_uZOt5KX.jpg'],
            } ,
            {
                id: 5,
                address: "48 Stony Brook Rd",
                commute_type: "Driving",
                images: ['/media/houseDatabase/30/30_11_uZOt5KX.jpg'],
            } ,
            {
                id: 6,
                address: "48 Stony Brook Rd",
                commute_type: "Driving",
                images: ['/media/houseDatabase/30/30_11_uZOt5KX.jpg'],
            } ,
            {
                id: 7,
                address: "48 Stony Brook Rd",
                commute_type: "Driving",
                images: ['/media/houseDatabase/30/30_11_uZOt5KX.jpg'],
            } ,
        ],
        visit_list:  [
            {
                id: 2,
                address: "48 Stony Brook Rd",
                commute_type: "Driving",
                images: ['/media/houseDatabase/30/30_11_uZOt5KX.jpg'],
            } ,
            {
                id: 3,
                address: "36 Stony Brook Rd",
                commute_type: "Driving",
                images: ['/media/houseDatabase/30/30_12_x0GmdOn.jpg', '/media/houseDatabase/30/30_11_uZOt5KX.jpg'],
            } ,
        ],
    };

    handleVisitClick = (home) => {
        let visit_list = [...this.state.visit_list];

        if (this.state.visit_list.filter(c => c.id === home.id).length > 0)
        {
            let home_index = visit_list.findIndex(function(visit) {
                return visit.id === home.id;
            });
            if (home_index !== -1) {
                visit_list.splice(home_index, 1);
            }
        } else {
            if (visit_list.length < 6)
            {
                visit_list.push(home)
            }
        }

        this.setState({visit_list})
    };

    renderFavorites() {
        if (this.state.favorites.length === 0) return <h3>Please load your survey and add favorite homes</h3>;
        return (
            <div>
                {this.state.favorites.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={this.inFavorites(home)}
                        visit={this.state.visit_list.filter(c => c.id === home.id).length >0}
                        onVisitClick={this.handleVisitClick}
                        show_heart={true}
                        show_score={false}
                        show_visit={true}
                    />
                )}
            </div>
        );
    };

    inFavorites(home) {
        // Checks to see if the home exists within the favorites list
        return this.state.favorites.filter(c => c.id === home.id).length > 0;
    }

    inVisitList(home) {
        // Checks to see if the home exists within the visit_list
        return this.state.visit_list.filter(c => c.id === home.id).length >0;
    }

    renderVisitList() {
        if (this.state.visit_list.length === 0) return <h3>Please add homes to your visit list!</h3>;
        return (
            <div>
                {this.state.visit_list.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={this.inFavorites(home)}
                        visit={this.inVisitList(home)}
                        onVisitClick={this.handleVisitClick}
                        show_score={false}
                        show_heart={false}
                        show_visit={true}
                    />
                )}
            </div>
        );
    };

    handleLoad = () => {
        console.log('Load survey', this.state.id)
    };

    render(){
        const { onDelete } = this.props;
        return (
            <div className="Dotted_box">
                <div className="row">
                    <div className="col-md-10">
                        <h1>{this.state.name}</h1>
                    </div>
                    <div className="col-md-2">
                        <button onClick={this.handleLoad} className="btn btn-primary btn-sm m-2">Load</button>
                        <button onClick={() => onDelete(this.state.id)} className="btn btn-danger btn-sm m-2">Delete</button>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-5">
                        <h2><u>Favorites:</u></h2>
                        {this.renderFavorites()}
                    </div>
                    <div className="col-md-5">
                        <h2><u>Visit List:</u></h2>
                        {this.renderVisitList()}
                    </div>
                </div>
            </div>
        );
    }
}
export default Survey
