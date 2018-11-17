import React from 'react'
import { Component } from 'react';

import './homeTile.css'

class HomeTile extends Component {

    static renderScore(home) {
        let homeScore = '';

        if (home.grade) {
            homeScore = <span className="scoreText">{home.grade}</span>
        }

        return (
            <div className="tileScore">
                {homeScore}
                <span className="glyphicon glyphicon-heart-empty"> </span>
            </div>
        );
    }

    static renderInfo(home) {
        return (
            <div className="homeInfo">
                <span className="homeBit">{home.price}</span>
            </div>
        );
    }

    static renderImages(home) {

        return (
            <React.Fragment>
            { home.images.map(image =>
                <div className="thumbnailDiv col-md-6">
                    <img className="thumbnailImage" src={image}></img>
                </div>
            )}
            </React.Fragment>
        );
    }

    render(){
        const { home } = this.props;
        return (
            <div className="tile">
                {HomeTile.renderScore(home)}
                {HomeTile.renderInfo(home)}
                {HomeTile.renderImages(home)}
            </div>
        );
    }
}
export default HomeTile;
