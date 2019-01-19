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
     *
     *  this.props.canFavorite: (boolean) -> True: Adds ability to favorite a home
     *                                       False: Removes ability to favorite a home
     *  this.props.canVisit: (boolean) -> True: Adds ability to add/remove home to visit list
     *                                    False: Removes ability to add/remove home to visit list
     *
     *
     * this.props.isLarge: (boolean) -> True: renders tile into square format i.e results page
     *                                  False (DEFAULT): renders tile horizontally
     *
     *
     * this.props.displayPercent: (boolean) -> True: renders the percent_match on the home tile. [Should ONLY be true if isLarge is also true!]
     *                                         False: (DEFAULT): Does not render the percent_match
     */
    state = {
        hover: false,
    };

    static defaultProps = {
        canFavorite: true,
        canVisit: true,
        isLarge: false,
        displayPercent: false
    }

    renderScore(home) {
        /**
         * Renders the score portion of the home tile
         * @type {string} THe home that is being rendered
         */

        // Toggles the button text/color based on favorite status
        let favorite_style;
        if (!this.props.canVisit) {
            favorite_style = {
                width: '100%',
                borderRight: 'none'
            }
        }
        let favorite_text = "Add to Favorites";
        let favorite_class = 'home_add_default';
        if (this.props.favorite) {
            favorite_text = "Added to Favorites";
            favorite_class += " home_added";
        } else {
            favorite_text = "Add to Favorites";
            favorite_class = 'home_add_default';
        }
        let heart_span = (
            <div className={favorite_class} style={favorite_style} onClick={(e) => this.props.onFavoriteClick(home, e)}>
                <i className="icon_heart material-icons">
                    favorite
                </i>
                <span>{favorite_text}</span>
            </div>
        );

        let visit_style;
        if (!this.props.canFavorite) {
            visit_style = {
                width: '100%',
                borderRight: 'none'
            }
        }
        let visit_icon = "playlist_add";
        let visit_text = "Add to Visit List";
        let visit_class = 'home_add_default';
        if (this.props.visit) {
            visit_icon = "playlist_add_check";
            visit_text = "Added to Visit List";
            visit_class += " home_added";
        } else {
            visit_icon = "playlist_add";
            visit_text = "Add to Visit List";
            visit_class = "home_add_default";
        }
        let visit_span = (
            <div className={visit_class} style={visit_style} onClick={(e) => this.props.onVisitClick(home, e)}>
                <i className="material-icons">
                    {visit_icon}
                </i>
                <span>{visit_text}</span>
            </div>
        );

        // Render the score and the heart icon
        return (
            <div className="tileScore">
                {this.props.canFavorite ? heart_span : null}
                {this.props.canVisit ? visit_span : null}
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

        let bedInfo = home.num_bedrooms > 1 ? 'beds' : 'bed';
        let bathInfo = home.num_bathrooms > 1 ? 'baths' : 'bath';

        return (
            <div className="homeInfo">
                <div className="homeInfo-group">
                    <span className={bit_classes}>${home.price} <span className="homeInfo-month">/ month</span></span>
                    <span className={bit_classes}>{`${home.num_bedrooms} ${bedInfo} • ${home.num_bathrooms} ${bathInfo}` }</span>
                </div>
                <span className={bit_classes}>{home.home_type.home_type}</span>
            </div>
        );
    }

    renderImages(home) {
        /**
         * Renders the image portion of the tile
         */

        if (home.images) {
            let div_classes = "thumbnailDiv";
            let image_classes = "thumbnailImage";

            // Sets percent_match to render on top of image
            let percent_match = null;
            if (this.props.isLarge && this.props.displayPercent) {
                percent_match = <span className="homeInfo-percent">{home.percent_match}</span>
            }

            // Only renders first photo
            return (
                <>
                    { home.images.slice(0,1).map(image =>
                        <div key={image.id} className={div_classes}>
                            {percent_match}
                            <img className={image_classes} src={image.image} alt='Home image'/>
                        </div>
                    )}
                </>
            );

        }
    }

    getTileClass = () => {
        let tileClass = 'tile';
        if (this.props.isLarge) {
            tileClass += ' tile_isLarge';
        } else {
            tileClass = 'tile';
        }
        return tileClass;
    }

    render(){
        const { home } = this.props;
        return (
            <div className={this.getTileClass()} onClick={() => this.props.onHomeClick(this.props.id)}>
                {this.renderScore(home)}
                {this.renderInfo(home)}
                {this.renderImages(home)}
            </div>
        );
    }
}
export default HomeTile;
