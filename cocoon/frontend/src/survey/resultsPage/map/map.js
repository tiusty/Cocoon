// Import React Components
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import GoogleMapReact from 'google-map-react';

import MapMarker from './mapMarker';
import CommuteMarker from './commuteMarker';
import { compose, withProps } from "recompose";


export default class Map extends Component {

    constructor(props) {
        super(props);
        this.state = {
            center: {
                lat: 42.36,
                lng: -71.05
            },
            zoom: 9
        }
    }

    componentDidMount() {
        this.createBounds();
    }

    componentDidUpdate(prevProps, prevState) {

        if (this.props.clicked_home !== prevProps.clicked_home && this.props.clicked_home !== undefined) {
            this.centerMarker(this.props.clicked_home);
        }

        if (this.props.homes !== prevProps.homes) {
            this.createBounds();
        }

    }

    createMapOptions(maps) {
        const mapStyle = [ { "featureType": "all", "elementType": "labels", "stylers": [ { "visibility": "off" } ] }, { "featureType": "administrative", "elementType": "all", "stylers": [ { "visibility": "simplified" }, { "color": "#5b6571" }, { "lightness": "35" } ] }, { "featureType": "administrative.neighborhood", "elementType": "all", "stylers": [ { "visibility": "off" } ] }, { "featureType": "landscape", "elementType": "all", "stylers": [ { "visibility": "on" } ] }, { "featureType": "landscape.man_made", "elementType": "geometry", "stylers": [ { "weight": 0.9 }, { "visibility": "off" } ] }, { "featureType": "poi.park", "elementType": "geometry.fill", "stylers": [ { "visibility": "on" }, { "color": "#83cead" } ] }, { "featureType": "road", "elementType": "all", "stylers": [ { "visibility": "on" }, { "color": "#ffffff" } ] }, { "featureType": "road", "elementType": "labels", "stylers": [ { "visibility": "on" }, { "color": "#9a6868" } ] }, { "featureType": "road", "elementType": "labels.text", "stylers": [ { "visibility": "on" } ] }, { "featureType": "road", "elementType": "labels.text.fill", "stylers": [ { "color": "#454545" } ] }, { "featureType": "road", "elementType": "labels.text.stroke", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway", "elementType": "all", "stylers": [ { "visibility": "on" }, { "color": "#fee379" } ] }, { "featureType": "road.highway", "elementType": "geometry", "stylers": [ { "visibility": "on" } ] }, { "featureType": "road.highway", "elementType": "labels", "stylers": [ { "visibility": "on" } ] }, { "featureType": "road.highway", "elementType": "labels.text.fill", "stylers": [ { "visibility": "on" }, { "color": "#222121" } ] }, { "featureType": "road.highway", "elementType": "labels.text.stroke", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway", "elementType": "labels.icon", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway.controlled_access", "elementType": "labels.icon", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.arterial", "elementType": "all", "stylers": [ { "visibility": "simplified" }, { "color": "#ffffff" } ] }, { "featureType": "road.arterial", "elementType": "labels", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.arterial", "elementType": "labels.icon", "stylers": [ { "visibility": "off" } ] }, { "featureType": "transit", "elementType": "labels", "stylers": [ { "visibility": "on" } ] }, { "featureType": "water", "elementType": "all", "stylers": [ { "visibility": "on" }, { "color": "#7fc8ed" } ] } ];
        return {
            'styles': mapStyle,
            mapTypeControlOptions: {
                mapTypeIds: []
            },

            gestureHandling: 'greedy',
            fullscreenControl: false,

            // Disables street view
            streetViewControl: false,

            zoomControl: true,
            zoomControlOptions: {
                position: maps.ControlPosition.LEFT_BOTTOM,
            }
        };
    }

    renderMapMarkers = () => {
        let mapMarkers = [];
        if (this.props.homes) {
            let homesCopy = [...this.props.homes];
            homesCopy.reverse().map(home => {
                let newMarker = (
                    <MapMarker
                        home={home}
                        lat={home.home.latitude}
                        lng={home.home.longitude}
                        score={home.percent_match}
                        key={home.home.id}
                        id={home.home.id}
                        hover_id={this.props.hover_id}
                        clicked_home={this.props.clicked_home}
                        handleHomeClick={this.props.handleHomeClick}
                        handleHomeMarkerClick={this.props.handleHomeMarkerClick}
                        setHoverId={this.props.setHoverId}
                        removeHoverId={this.props.removeHoverId}
                    />
                );
                mapMarkers.push(newMarker);
            })
        }

        // Unclean way to make sure it gracefully fails if none of the values exist
        if (this.props.survey) {
            if (this.props.survey.tenants) {
                this.props.survey.tenants.map(t => {
                    if (t.commute_type) {
                        if (t.commute_type.commute_type) {
                            // If the user put Work From Home then we don't want the destination to render
                            if (t.commute_type.commute_type !== "Work From Home") {
                                let newMarker = (
                                    <CommuteMarker
                                        lat={t.latitude}
                                        lng={t.longitude}
                                        name={t.first_name}
                                        key={t.id}
                                    />
                                );
                                mapMarkers.push(newMarker);
                            }
                        }
                    }
                })
            }
        }
        return mapMarkers;
    };

    createBounds = () => {
        /*
        *   Function from stack overflow to center the map to show all map markers
        *
        *   Ideally we'd be using the google maps fitBounds() method but it doesn't
        *   seem to work with the google maps react component
        *   so we have to calculate the center of the home list coordinates ourselves
        *
        */

        if (!(this.props.homes.length > 0)){
            return false;
        }

        const num_coords = this.props.homes.length;

        let X = 0.0;
        let Y = 0.0;
        let Z = 0.0;

        for(let i = 0; i < this.props.homes.length; i++){
            let lat = this.props.homes[i].home.latitude * Math.PI / 180;
            let lon = this.props.homes[i].home.longitude * Math.PI / 180;

            let a = Math.cos(lat) * Math.cos(lon);
            let b = Math.cos(lat) * Math.sin(lon);
            let c = Math.sin(lat);

            X += a;
            Y += b;
            Z += c;
        }

        X /= num_coords;
        Y /= num_coords;
        Z /= num_coords;

        let lon = Math.atan2(Y, X);
        let hyp = Math.sqrt(X * X + Y * Y);
        let lat = Math.atan2(Z, hyp);

        let newX = (lat * 180 / Math.PI);
        let newY = (lon * 180 / Math.PI);
        this.setState({
            center: {
                lat: newX,
                lng: newY
            }
        })
    }

    centerMarker = (homeId) => {
        const home = this.props.homes.find(home => home.home.id === homeId);
        const { latitude, longitude } = home.home;
        const centerCoords = {
            lat: parseFloat(latitude),
            lng: parseFloat(longitude)
        }
        this.setState({
            center: centerCoords
        })
    }

    render() {
        return (
            <GoogleMapReact
                center={this.state.center}
                defaultZoom={this.state.zoom}
                options={this.createMapOptions}
                handleHomeClick={this.props.handleHomeClick}
                hover_id={this.props.hover_id}
                setHoverId={this.props.setHoverId}
                removeHoverId={this.props.removeHoverId}
                ref="map">
                {this.renderMapMarkers()}
            </GoogleMapReact>
        )
    }
}
