// Import React Components
import React from 'react'
import {Component} from 'react';

// Carousel
import "react-responsive-carousel/lib/styles/carousel.min.css";
import { Carousel } from 'react-responsive-carousel';
import PlaceHolder from "./homelist-empty.jpg";

export default class HomeTileLarge extends Component {
    /**
     * This component displays extra information for a home
     *
     * Props:
     *  this.props.home: (RentDatabase Home) -> The home that that is being displayed
     *  this.props.onCloseHomeTileLarge: (function()) -> Handles which the user clicks the close button
     *
     *  this.props.canFavorite: (boolean) -> True: Adds ability to favorite a home
     *                                      False: Removes ability to favorite a home
     *  this.props.canVisit: (boolean) -> True: Adds ability to add/remove home to visit list
     *                                    False: Removes ability to add/remove home to visit list
     *
     * this.props.displayPercent: (boolean) -> True: renders the percent_match on the home tile.
     *                                         False: (DEFAULT): Does not render the percent_match
     */

    static defaultProps = {
        canFavorite: true,
        canVisit: false,
        displayPercent: false
    };

    renderInterior = (home) => {
        /**
         * Renders all the interior amenities information
         * @type {Array}
         */

        // Creates a list of all the interior amenities that exist
        let interior_amenities = [];
        for (var key in home.interior_amenities) {
            if (home.interior_amenities[key]) {
                interior_amenities.push(key)
            }
        }

        // If there is at least one amenity then render it
        // Since the names have a _ instead of a space, when rendering the name
        //  replace all _ with spaces
        if (interior_amenities.length > 0) {
            return (
                <div className="point-wrapper">
                    <h3>Interior Amenities</h3>
                    {interior_amenities.map(item => (
                        <p key={item}><i className="material-icons">check</i> {item.replace(/_/g,' ')}</p>
                    ))}
                </div>
            );

        // If there is not data then render that there is no data
        } else {
            return (
                <div className="point-wrapper">
                    <h3>Interior Amenities</h3>
                    <p>No data</p>
                </div>
            );
        }
    };

    renderExterior = (home) => {
        /**
         * Renders all the exterior amenities information
         * @type {Array}
         */

        // Creates a list of all the exterior amenities that exist
        let exterior_amenities = [];
        for (var key in home.exterior_amenities) {
            if (home.exterior_amenities[key]) {
                exterior_amenities.push(key)
            }
        }

        // If there is at least one amenity then render it
        // Since the names have a _ instead of a space, when rendering the name
        //  replace all _ with spaces
        if (exterior_amenities.length > 0) {
            return (
                <div className="point-wrapper">
                    <h3>Exterior Amenities</h3>
                    {exterior_amenities.map(item => (
                        <p key={item}><i className="material-icons">check</i> {item.replace(/_/g,' ')}</p>
                    ))}
                </div>
            );

        // If there is not data then render that there is no data
        } else {
            return (
                <div className="point-wrapper">
                    <h3>Exterior Amenities</h3>
                    <p>No data</p>
                </div>
            );
        }
    };

    renderNearby = (home) => {
        /**
         * Renders all the nearby amenity information
         * @type {Array}
         */

        // Creates a list of all the nearby amenities that exist
        let nearby_amenities = [];
        for (var key in home.nearby_amenities) {
            if (home.nearby_amenities[key]) {
                nearby_amenities.push(key)
            }
        }

        // If there is at least one amenity then render it
        // Since the names have a _ instead of a space, when rendering the name
        //  replace all _ with spaces
        if (nearby_amenities.length > 0) {
            return (
                <div className="point-wrapper">
                    <h3>What's near here?</h3>
                    {nearby_amenities.map(item => (
                        <p key={item}><i className="material-icons">check</i> {item.replace(/_/g,' ')}</p>
                    ))}
                </div>
            );

        // If there is not data then render that there is no data
        } else {
            return (
                <div className="point-wrapper">
                    <h3>Nearby Amenities</h3>
                    <p>No data</p>
                </div>
            );
        }
    };

    renderBrokerInfo = (home) => {
        /**
         * Renders all the nearby amenity information
         * @type {Array}
         */

            // Creates a list of all the nearby amenities that exist
        let broker_info = [];
        for (var key in home.broker_info) {
            console.log(key)
                broker_info.push(key)
        }

        // If there is at least one amenity then render it
        // Since the names have a _ instead of a space, when rendering the name
        //  replace all _ with spaces
        if (broker_info.length > 0) {
            return (
                <div className="broker_info">
                    <h3>Broker Info</h3>
                    {broker_info.map(item => (
                        <div key={item} className="itinerary-section-item">
                            <span className="item-left-text">{item.replace(/_/g,' ')}</span>
                            <span className="item-right-text">{home.broker_info[item]}</span>
                        </div>
                    ))}
                </div>
            );

            // If there is not data then render that there is no data
        } else {
            return (
                <div className="point-wrapper">
                    <h3>Broker Info</h3>
                    <p>No data</p>
                </div>
            );
        }
    };

    renderAmenities = () => {
        /**
         * Renders all the amenities information associated with the home
         */
        let home = this.props.home;
        return (
            <div className="expanded-points">
                {this.renderInterior(home)}
                {this.renderExterior(home)}
                {this.renderNearby(home)}
            </div>
        );

    };

    renderScore(home) {
        /**
         * Renders the score portion of the home tile
         * @type {string} THe home that is being rendered
         */

            // Toggles whether the home text depending on favorite status
        let favorite_style;
        if (!this.props.canVisit) {
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

renderPercentMatch = (home) => {
        /**
         * Returns the percent match info if it is desired
         * @type {null}
         */
        let percent_match = null;
        if (this.props.displayPercent && home.percent_match) {
            percent_match = <span className="homeInfo-percent">{home.percent_match}</span>
        }
        if (percent_match === null && this.props.percent_match) {
            percent_match = <span className="homeInfo-percent">{this.props.percent_match}</span>
        }
        return percent_match;
    }

    renderImages = () => {
        let { home } = this.props;
        // renders placeholder image if home has no images
        if (home.images.length === 0) {
            return (
                <div className="thumbnailDiv">
                    <img src={PlaceHolder} alt="place holder image" className="thumbnailImage" />
                </div>
            );
        } else {
            // renders carousel
            return (
                <Carousel
                    dynamicHeight={false}
                    infiniteLoop={true}
                    showThumbs={false}
                    showStatus={false}
                >
                    {home.images.map(image =>
                            <div key={image.id}>
                                <img src={image.image} alt="house image"/>
                            </div>
                    )}
                </Carousel>
            );
        }
    }

    render() {
        let { home } = this.props;
        let bedInfo = home.num_bedrooms > 1 ? 'beds' : 'bed';
        let bathInfo = home.num_bathrooms > 1 ? 'baths' : 'bath';
        return (
            <>
                <div className="expanded-tile-container">
                    <div className="expanded-row-top">
                        <span onClick={() => this.props.onCloseHomeTileLarge()}>
                            <i className="material-icons">arrow_back_ios</i>
                            Back
                        </span>
                    </div>
                    <div className="expanded-info">
                        <div className="home-tile-large-carousel-div">
                            {this.renderPercentMatch(home)}
                            {this.renderImages(home)}
                        </div>

                        <div className="expanded-info-text">

                            <div className="expanded-home-info">
                                <div>
                                    <span className="price">${home.price} <span className="homeInfo-month">/ month</span></span>
                                    <span className="number-rooms">{`${home.num_bedrooms} ${bedInfo} • ${home.num_bathrooms} ${bathInfo}` }</span>
                                </div>
                                <span className="home-info-badge">{home.home_type.home_type}</span>
                            </div>

                            <div className="expanded-remarks">
                                <p>{home.remarks}</p>
                            </div>

                            {this.renderAmenities()}
                            {this.renderBrokerInfo(home)}
                        </div>
                        {this.renderScore(home)}
                    </div>
                </div>
            </>
        );
    }
}
