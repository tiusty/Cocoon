// Import React Components
import React from 'react'
import { Component } from 'react';

// Import Cocoon Components
import './homeTile.css'

class HomeTile extends Component {
    /**
     * Props:
     *  this.props.id: (int) -> The id for the home
     *  this.props.home: (RentDatabase Model) -> Stores the information related to the home
     *  this.props.favorite: (boolean) -> True: The home is currently favorited
     *                                    False: The home is not currently favorited
     *  this.props.visit: (boolean) -> True: The home is currently in the visit list
     *                                 False: The home is not currently in the visit list
     *  this.props.onVisitClick: (function(RentDatabase Model, event)) -> Handles when the visit button is pressed
     *  this.props.onFavoriteClick: (function(RentDatabase Model, event)) -> Handles when the favorite button is clicked
     *  this.props.onHomeClick: (function(int)) (int- the id of the home clicked) -> Handles when a home tile is clicked
     */
    state = {
        hover: false,
    };

    renderScore(home) {
        /**
         * Renders the score portion of the home tile
         * @type {string} THe home that is being rendered
         */

        // Toggles whether the home has a empty or full heart depending on favorite status
        let heart_span = "";
        if (this.props.show_heart) {
            let heart_class = "glyphicon";
            if (this.props.favorite) {
                heart_class += " glyphicon-heart"
            } else {
                heart_class += " glyphicon-heart-empty"
            }
            heart_span = <span className={heart_class} onClick={(e) => this.props.onFavoriteClick(home, e)}> </span>;
        }

        let visit_classes = "glyphicon glyphicon-check-class";
        if (this.props.visit)
        {
            visit_classes += " glyphicon-remove";
        } else {
            visit_classes += " glyphicon-ok";
        }
        let visit_span = <span className={visit_classes} onClick={(e) => this.props.onVisitClick(home, e)}> </span>;

        // Render the score and the heart icon
        return (
            <div className="tileScore">
                {heart_span}
                {visit_span}
            </div>
        );

    }

    renderInfo(home) {
        /**
         * Renders the info portion on the home Tile
         * @type {string}
         */
        let bit_classes = "homeBit ";
        if (this.state.hover) {
            bit_classes += "homeBit-hover";
        }
        return (
            <div className="homeInfo">
                <span className={bit_classes}>${home.price}</span>
                <span className={bit_classes}>{home.home_type.home_type}</span>
            </div>
        );
    }

    renderImages(home) {
        /**
         * Renders the image portion of the tile
         */
        if (home.images) {
            let div_classes = "col-md-5 thumbnailDiv ";
            let image_classes = "thumbnailImage ";
            if (this.state.hover) {
                div_classes += "thumbnailDiv-hover";
                image_classes += "thumbnailImage-hover";
            }

            // Only renders first 2 photos
            return (
                <>
                    { home.images.slice(0,2).map(image =>
                        <div key={image.id} className={div_classes}>
                            <img className={image_classes} src={image.image} alt='Home image'/>
                        </div>
                    )}
                </>
            );

        }
    }

    toggleHover = () => {
        /**
         * Creates the hovering functionality of the tile
         * @type {boolean}
         */
        let hover = !this.state.hover;
        this.setState({hover})
    };

    render(){
        const { home } = this.props;
        return (
            <div className="tile" onClick={() => this.props.onHomeClick(this.props.id)} onMouseEnter={this.toggleHover} onMouseLeave={this.toggleHover}>
                {this.renderScore(home)}
                {this.renderInfo(home)}
                {this.renderImages(home)}
            </div>
        );
    }
}
export default HomeTile;
