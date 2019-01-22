// Import React Components
import React, { Component } from 'react';

export default class MapMarker extends Component {
    constructor(props) {
        super(props);
    }

    colorMarkers = (score) => {
        let marker_class = 'map-marker';
        if (score > 86) {
            return marker_class + ' map-marker_teal';
        } else if (score > 79) {
            return marker_class + ' map-marker_yellow';
        } else if (score > 69) {
            return marker_class + ' map-marker_orange';
        } else if (score > 59) {
            return marker_class + ' map-marker_red';
        } else {
            return marker_class + ' map-marker_dark-blue';
        }
    }

    render() {
        return <div className={this.colorMarkers(this.props.score)}>{this.props.score}</div>
    }
}