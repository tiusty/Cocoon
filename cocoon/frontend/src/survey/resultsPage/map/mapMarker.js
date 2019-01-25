// Import React Components
import React, { Component } from 'react';

export default class MapMarker extends Component {
    constructor(props) {
        super(props);
    }

    colorMarkers = (score) => {
        let marker_class = 'map-marker';

        if (score > 89) {
            marker_class = marker_class + ' map-marker_dark-blue';
        } else if (score > 69) {
            marker_class = marker_class + ' map-marker_teal';
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

    render() {
        return (
            <div
                onMouseEnter={() => this.props.setHoverId(this.props.id)}
                onMouseLeave={this.props.removeHoverId}
                onClick={() => this.props.handleHomeClick(this.props.id)}
                className={this.colorMarkers(this.props.score)}>
                {this.props.score}
            </div>
        )
    }
}