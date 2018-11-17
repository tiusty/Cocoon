import React from 'react'
import { Component } from 'react';
import HomeTile from "./homeTile";

import './survey.css'

class Survey extends Component {

    renderFavorites() {
        if (this.props.survey.favorites.length === 0) return <h3>Please load your survey and add favorite homes</h3>;
        return (
            <div>
                {this.props.survey.favorites.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={true}
                    />
                )}
            </div>
        );
    };

    renderVisitList() {
        if (this.props.survey.visit_list.length === 0) return <h3>Please add homes to your visit list!</h3>;
        return (
            <div>
                {this.props.survey.visit_list.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={true}
                    />
                )}
            </div>
        );
    };

    render(){
        const { survey, onDelete } = this.props;
        return (
            <div className="Dotted_box">
                <div className="row">
                    <div className="col-md-10">
                        <h1>{survey.name}</h1>
                    </div>
                    <div className="col-md-2">
                        <button onClick={() => onDelete(survey.id)} className="btn btn-danger btn-sm m-2">Delete</button>
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
