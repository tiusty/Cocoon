// Import React Components
import React from 'react'
import { Component } from 'react';
import PropTypes from 'prop-types';

// Import Cocoon Components
import '../styles/variables.css';
import './homeTile.css';
import PlaceHolder from './homelist-empty.jpg';
import OffMarket from './sold.svg';

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
     *
     *  this.props.addBorder: (boolean) -> Determines if a border should be added to tile i.e. when a home is in the visit list
     */
    state = {
        hover: false,
    };

    static defaultProps = {
        canFavorite: true,
        canVisit: false,
        isLarge: false,
        displayPercent: false,
        percent_match: null,
        missing_amenities: [],
        show_missing_amenities: false,
        displayOnMarket: false,
        addBorder: false
    }

    renderScore(home) {
        /**
         * Renders the score portion of the home tile
         * @type {string} THe home that is being rendered
         */

        // Toggles the button text/color based on favorite status
        let favorite_style;
        if (!this.props.canVisit || (!this.props.onMarket && !this.props.visit)) {
            favorite_style = {
                width: '100%',
                borderRight: 'none'
            }
        }
        let favorite_text = "Add to Favorites";
        let favorite_class = 'home_add_default';
        let favorite_icon = "favorite_border";
        if (this.props.favorite) {
            favorite_text = "Added to Favorites";
            favorite_class += " home_added";
            favorite_icon = "favorite";
        } else {
            favorite_text = "Add to Favorites";
            favorite_class = 'home_add_default';
            favorite_icon = "favorite_border";
        }
        let heart_span = (
            <div className={favorite_class} style={favorite_style} onClick={(e) => this.props.onFavoriteClick(home, e)}>
                <i className="icon_heart material-icons">
                    {favorite_icon}
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
            visit_text = "Remove From Visit List";
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
                {(this.props.canVisit && this.props.onMarket) || (this.props.visit && !this.props.onMarket) ? visit_span : null}
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

        let bedInfo;
        let bathInfo;

        if (home.num_bedrooms > 1) {
            bedInfo = `${home.num_bedrooms} beds`;
        } else {
            bedInfo = 'Studio';
        }

        if (home.num_bathrooms > 1) {
            bathInfo = `${home.num_bathrooms} baths`;
        } else {
            bathInfo = '0.5 baths'
        }

        return (
            <div onClick={() => this.props.onHomeClick(this.props.id)} className="homeInfo">
                <div className="homeInfo-group">
                    <span className={bit_classes}>${home.price} <span className="homeInfo-month">/ month</span></span>
                    <span className={bit_classes}>{`${bedInfo} • ${bathInfo}`}</span>
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
            let marker_class = 'homeInfo-percent';
            let score = this.props.percent_match;
            if (score > 84) {
                marker_class = marker_class + ' map-marker_green';
            } else if (score > 69) {
                marker_class = marker_class + ' map-marker_light-green';
            } else if (score > 49) {
                marker_class = marker_class + ' map-marker_yellow';
            } else if (score > 29) {
                marker_class = marker_class + ' map-marker_orange';
            } else {
                marker_class = marker_class + ' map-marker_red';
            }
            if (this.props.isLarge && this.props.displayPercent && this.props.percent_match) {
                percent_match = <span className={marker_class}>{this.props.percent_match}</span>
            }

            let missing_amenities = null;
            if (this.props.show_missing_amenities) {
                // Sets background color of badge and renders the # of missing amenities
                let missing_number = this.props.missing_amenities.length;

                let missing_style = 'var(--teal)';
                if (missing_number > 2) {
                    missing_style = '#ff0110';
                } else if (missing_number > 0) {
                    missing_style = '#ff9a00';
                }

                let missing_text = 'Missing Amenities!';
                if (missing_number === 1) {
                    missing_text = "Missing Amenity!";
                }

                missing_amenities = <span className="homeInfo-missing_amenities" style={{background: missing_style}}><i className="material-icons">notifications</i> <span className="missing_amenities_text">{missing_number} {missing_text}</span></span>;
            }

            // Styles the date available section
            let date = null;
            if (this.props.isLarge) {
                date = <span className="homeInfo-date_available" title={'Date Available: ' + home.date_available}><i className="material-icons">access_time</i> {home.date_available}</span>
            }

            let off_market_section = null;
            if (this.props.displayOnMarket && !this.props.onMarket) {
                off_market_section = (
                    <div className="off-market-wrapper">
                        <img src={OffMarket} alt="home is off the market"/>
                    </div>
                );
            }

            // renders placeholder image if home has no images
            if (home.images.length === 0) {
                return (
                    <div onClick={() => this.props.onHomeClick(this.props.id)} className={div_classes}>
                        {percent_match}
                        {missing_amenities}
                        {date}
                        {off_market_section}
                        <img src={PlaceHolder} alt="place holder image" className={image_classes} />
                    </div>
                );
            } else {
                // Only renders first photo
                return (
                    <>
                        { home.images.slice(0,1).map(image =>
                            <div onClick={() => this.props.onHomeClick(this.props.id)} key={image.id} className={div_classes}>
                                {percent_match}
                                {missing_amenities}
                                {date}
                                {off_market_section}
                                <img className={image_classes} src={image.image} alt='Home image'/>
                            </div>
                        )}
                    </>
                );
            }

        }
    }

    getTileClass = () => {
        let tileClass = 'tile';
        if (this.props.isLarge) {
            tileClass += ' tile_isLarge';
        } else {
            tileClass = 'tile';
        }
        if (this.props.addBorder) {
            tileClass += ' tile-border_active';
        }
        return tileClass;
    }

    render(){
        const { home } = this.props;
        return (
            <div className={this.getTileClass()} onMouseEnter={this.props.onMouseEnter} onMouseLeave={this.props.onMouseLeave}>
                {this.renderScore(home)}
                {this.renderInfo(home)}
                {this.renderImages(home)}
            </div>
        );
    }
}
export default HomeTile;

// Set the types and whether any props are required
HomeTile.propTypes = {
    id: PropTypes.number,
    home: PropTypes.any.isRequired,
    visit: PropTypes.bool.isRequired,
    favorite: PropTypes.bool.isRequired,
    onVisitClick: PropTypes.func,
    onFavoriteClick: PropTypes.func,
    onHomeClick: PropTypes.func.isRequired,
    canVisit: PropTypes.bool,
    canFavorite: PropTypes.bool,
    isLarge: PropTypes.bool,
    displayPercent: PropTypes.bool,
    percent_match: PropTypes.number,
    addBorder: PropTypes.bool
};

