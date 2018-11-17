import React from 'react'
import { Component } from 'react';

import './homeTile.css'

class HomeTile extends Component {
    state = {
        hover: false,
    };

    renderScore(home) {
        let homeScore = '';

        let classes = "scoreText ";
        if (this.state.hover) {
           classes += "scoreText-hover"
        }

        if (home.grade) {
            homeScore = <span className={classes}>{home.grade}</span>
        }

        return (
            <div className="tileScore">
                {homeScore}
                <span className="glyphicon glyphicon-heart-empty"> </span>
            </div>
        );
    }

    renderInfo(home) {
        let bit_classes = "homeBit ";
        if (this.state.hover) {
            bit_classes += "homeBit-hover";
        }
        return (
            <div className="homeInfo">
                <span className={bit_classes}>{home.price}</span>
            </div>
        );
    }

    renderImages(home) {
        let div_classes = "col-md-5 thumbnailDiv ";
        let image_classes = "thumbnailImage ";
        if (this.state.hover) {
            div_classes += "thumbnailDiv-hover";
            image_classes += "thumbnailImage-hover";
        }

        return (
            <React.Fragment>
            { home.images.map(image =>
                <div className={div_classes}>
                    <img className={image_classes} src={image}/>
                </div>
            )}
            </React.Fragment>
        );
    }

    toggleHover = () => {
        let hover = !this.state.hover;
        this.setState({hover})
    };

    render(){
        const { home } = this.props;
        return (
            <div className="tile" onMouseEnter={this.toggleHover} onMouseLeave={this.toggleHover}>
                {this.renderScore(home)}
                {this.renderInfo(home)}
                {this.renderImages(home)}
            </div>
        );
    }
}
export default HomeTile;
