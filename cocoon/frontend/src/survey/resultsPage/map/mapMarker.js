// Import React Components
import React, { Component } from 'react';
import PlaceHolder from './homelist-empty.jpg';

export default class MapMarker extends Component {
    constructor(props) {
        super(props);
    }

    colorMarkers = (score) => {
        let marker_class = 'map-marker';
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

        if (this.props.hover_id === this.props.id) {
            marker_class = marker_class + ' map-marker_hover';
        }
        return marker_class;
    }

    renderMapMarkerInfo = () => {
        if (this.props.hover_id === this.props.id || (this.props.clicked_home && this.props.clicked_home === this.props.id)) {
            return (
                <MapMarkerInfo
                    onClickMarker={this.props.handleHomeMarkerClick}
                    home={this.props.home.home} />
                );
        } else {
            return null;
        }
    }

    render() {
        return (
            <>
                {this.renderMapMarkerInfo()}
                <div
                    onMouseEnter={() => this.props.setHoverId(this.props.id)}
                    onMouseLeave={this.props.removeHoverId}
                    onClick={() => this.props.handleHomeClick(this.props.id)}
                    style={ { position: 'absolute', transform: 'translate(-50%, -50%)' } }
                    className={this.colorMarkers(this.props.score)}>
                    {this.props.score}
                </div>
            </>
        )
    }
}

class MapMarkerInfo extends Component {

    constructor(props) {
        super(props);
    }

    renderRoomInfo = (home) => {
        let bedInfo;
        let bathInfo;

        if (home.num_bedrooms > 1) {
            bedInfo = `${home.num_bedrooms} beds`;
        } else if (home.num_bedrooms === 1) {
            bedInfo = `${home.num_bedrooms} bed`;
        } else {
            bedInfo = 'Studio';
        }

        if (home.num_bathrooms > 1) {
            bathInfo = `${home.num_bathrooms} baths`;
        } else {
            bathInfo = `${home.num_bathrooms} bath`;
        }

        return `${bedInfo} • ${bathInfo}`;
    }

    renderImage = (home) => {
        let style = {
            backgroundImage: `url(${PlaceHolder})`
        }
        if (home.images.length > 0) {
            style = {
                backgroundImage: `url(${home.images[0].image})`
            }
        }
        return style;
    }

    render() {
        return (
            <div className="map-marker-info-wrapper" onClick={() => this.props.onClickMarker(this.props.home.id)}>
                <div className="map-marker-info_img" style={this.renderImage(this.props.home)}></div>
                <div className="map-marker-info">
                    <div className="map-marker-info_price">
                        ${this.props.home.price} <span>/ month</span>
                    </div>
                    <div className="map-marker-info_rooms">
                        {this.renderRoomInfo(this.props.home)}
                    </div>
                </div>
            </div>
        );
    }
}