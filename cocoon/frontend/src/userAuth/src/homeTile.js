import React from 'react'
import { Component } from 'react';

import './homeTile.css'

class HomeTile extends Component {
    state = {
        hover: false,
        heartState: this.props.favorite,
    };

    renderScore(home) {

        let homeScore = '';
        if (this.props.show_score) {
            // Determines whether the user is hovering over that tile
            let classes = "scoreText ";
            if (this.state.hover) {
                classes += "scoreText-hover"
            }
            // Determines if a grade was passed to the home, if not then don't render it
            if (home.grade) {
                homeScore = <span className={classes}>{home.grade}</span>
            }
        }

        // Toggles whether the home has a empty or full heart depending on favorite status
        let heart_span = '';
        if (this.props.show_heart) {
            let heart_class = "glyphicon";
            if (this.state.heartState) {
                heart_class += " glyphicon-heart"
            } else {
                heart_class += " glyphicon-heart-empty"
            }

            heart_span = <span className={heart_class} onClick={() => this.props.onFavoriteClick(home)}> </span>;
        }

        let visit_span = '';
        if (this.props.show_visit) {
            let visit_classes = "glyphicon";
            if (this.props.visit)
            {
                visit_classes += " glyphicon-remove";
            } else {
                visit_classes += " glyphicon-ok";
            }
            visit_span = <span className={visit_classes} onClick={() => this.props.onVisitClick(home)}> </span>;
        }

        // Render the score and the heart icon
        return (
            <div className="tileScore">
                {homeScore}
                {heart_span}
                {visit_span}
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
                <span className={bit_classes}>{home.home_type.home_type}</span>
            </div>
        );
    }

    renderImages(home) {

        if (home.images) {
            let div_classes = "col-md-5 thumbnailDiv ";
            let image_classes = "thumbnailImage ";
            if (this.state.hover) {
                div_classes += "thumbnailDiv-hover";
                image_classes += "thumbnailImage-hover";
            }

            return (
                <React.Fragment>
                    { home.images.map(image =>
                        <div key={image} className={div_classes}>
                            <img className={image_classes} src={image}/>
                        </div>
                    )}
                </React.Fragment>
            );

        }
    }

    toggleHeart = () => {
        let heartState = !this.state.heartState;
        this.setState({heartState})
    };

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
