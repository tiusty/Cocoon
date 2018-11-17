import React from 'react'
import { Component } from 'react';
import HomeTile from "./homeTile";

class Survey extends Component {

    renderHomes() {
        console.log("in render homes", this.props.survey.favorites.length)
        if (this.props.survey.favorites.length === 0) return <p>No Homes!</p>;
        console.log('after')


        return (

            <div>
                {this.props.survey.favorites.map(home =>
                <HomeTile
                key={home.id}
                home={home}
            />
            )
                }
            </div>
        );
    };

    render(){
        const { survey, onDelete } = this.props;
        return (
            <div>
                <h1>{survey.name}</h1>
                <button onClick={() => onDelete(survey.id)} className="btn btn-danger btn-sm m-2">Delete</button>
                {this.renderHomes()}
            </div>
        );
    }
}
export default Survey
