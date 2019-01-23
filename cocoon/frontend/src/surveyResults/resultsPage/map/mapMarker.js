// Import React Components
import React, { Component } from 'react';

export default class MapMarker extends Component {
    constructor(props) {
        super(props);
    }

    colorMarkers = (score) => {
        let marker_class = 'map-marker';

        if (score > 86) {
            marker_class = marker_class + ' map-marker_teal';
        } else if (score > 79) {
            marker_class = marker_class + ' map-marker_yellow';
        } else if (score > 69) {
            marker_class = marker_class + ' map-marker_orange';
        } else if (score > 59) {
            marker_class = marker_class + ' map-marker_red';
        } else {
            marker_class = marker_class + ' map-marker_dark-blue';
        }

        if (this.props.hover_id === this.props.id) {
            marker_class = marker_class + ' map-marker_hover';
        }
        return marker_class;
    }

    render() {
        return (
            <div
                onClick={() => this.props.handleHomeClick(this.props.id)}
                className={this.colorMarkers(this.props.score)}>
                {this.props.score}
            </div>
        )
    }
}