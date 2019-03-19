// Import React Components
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import GoogleMapReact from 'google-map-react';
import { fitBounds } from 'google-map-react/utils';

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
            zoom: 10
        }
    }

    componentDidMount() {
        console.log(this.refs.map)
    }

    componentDidUpdate(prevProps, prevState) {

        if (this.props.clicked_home !== prevProps.clicked_home && this.props.clicked_home !== undefined) {
            this.centerMarker(this.props.clicked_home);
        }

    }

    createMapOptions(maps) {
        const mapStyle = [ { "featureType": "all", "elementType": "labels", "stylers": [ { "visibility": "off" } ] }, { "featureType": "administrative", "elementType": "all", "stylers": [ { "visibility": "simplified" }, { "color": "#5b6571" }, { "lightness": "35" } ] }, { "featureType": "administrative.neighborhood", "elementType": "all", "stylers": [ { "visibility": "off" } ] }, { "featureType": "landscape", "elementType": "all", "stylers": [ { "visibility": "on" } ] }, { "featureType": "landscape.man_made", "elementType": "geometry", "stylers": [ { "weight": 0.9 }, { "visibility": "off" } ] }, { "featureType": "poi.park", "elementType": "geometry.fill", "stylers": [ { "visibility": "on" }, { "color": "#83cead" } ] }, { "featureType": "road", "elementType": "all", "stylers": [ { "visibility": "on" }, { "color": "#ffffff" } ] }, { "featureType": "road", "elementType": "labels", "stylers": [ { "visibility": "on" }, { "color": "#9a6868" } ] }, { "featureType": "road", "elementType": "labels.text", "stylers": [ { "visibility": "on" } ] }, { "featureType": "road", "elementType": "labels.text.fill", "stylers": [ { "color": "#454545" } ] }, { "featureType": "road", "elementType": "labels.text.stroke", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway", "elementType": "all", "stylers": [ { "visibility": "on" }, { "color": "#fee379" } ] }, { "featureType": "road.highway", "elementType": "geometry", "stylers": [ { "visibility": "on" } ] }, { "featureType": "road.highway", "elementType": "labels", "stylers": [ { "visibility": "on" } ] }, { "featureType": "road.highway", "elementType": "labels.text.fill", "stylers": [ { "visibility": "on" }, { "color": "#222121" } ] }, { "featureType": "road.highway", "elementType": "labels.text.stroke", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway", "elementType": "labels.icon", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway.controlled_access", "elementType": "labels.icon", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.arterial", "elementType": "all", "stylers": [ { "visibility": "simplified" }, { "color": "#ffffff" } ] }, { "featureType": "road.arterial", "elementType": "labels", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.arterial", "elementType": "labels.icon", "stylers": [ { "visibility": "off" } ] }, { "featureType": "transit", "elementType": "labels", "stylers": [ { "visibility": "on" } ] }, { "featureType": "water", "elementType": "all", "stylers": [ { "visibility": "on" }, { "color": "#7fc8ed" } ] } ];
        return {
            'styles': mapStyle,
            mapTypeControlOptions: {
                mapTypeIds: []
            },

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
        /* ! IN PROGRESS
        *   To resize/zoom/center the map to show all map markers
        *   uses google maps fitBounds()
        */
        if (this.props.homes) {
            const bounds = new window.google.maps.LatLngBounds();
            this.props.homes.forEach(home => bounds.extend(new window.google.maps.LatLng(parseFloat(home.home.latitude), parseFloat(home.home.longitude))));
            console.log(bounds)
            // this.refs.map.fitBounds(bounds);
        }
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
                onTilesLoaded={() => this.createBounds()}
                ref="map">
                {this.renderMapMarkers()}
            </GoogleMapReact>
        )
    }
}
