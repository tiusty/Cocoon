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
            zoom: 10,
            markers: [],
        }
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

            gestureHandling: 'greedy',
            fullscreenControl: false,

            // Disables street view
            streetViewControl: false,

            zoomControl: false,
        };
    }

    renderMapMarkers = () => {
        /**
         * This function no longer renders the markers on the google map, instead
         *  this is still used on the googleapiload so that fitbounds as all the markers
         *      so it can properly size the map
         * @type {Array}
         */
        let mapMarkers = [];
        if (this.props.homes) {
            let homesCopy = [...this.props.homes];
            homesCopy.reverse().map(home => {
                // Don't add the marker if the lat and lng is 0,0
                if (parseFloat(home.home.latitude) && parseFloat(home.home.longitude)) {
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
                            handleHomePinClick={this.props.handleHomePinClick}
                            handleHomeMarkerClick={this.props.handleHomeMarkerClick}
                            setHoverId={this.props.setHoverId}
                            removeHoverId={this.props.removeHoverId}
                        />
                    );
                    mapMarkers.push(newMarker);
                }
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
                                // Don't add the marker if the lattiude is 0,0
                                if (parseFloat(t.latitude) && parseFloat(t.longitude)) {
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
                    }
                })
            }
        }
        return mapMarkers;
    };

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
                yesIWantToUseGoogleMapApiInternals
                onGoogleApiLoaded={({ map, maps }) => apiIsLoaded(map, maps, this.renderMapMarkers())}
                ref="map">
                {[...this.props.homes].reverse().map(home => {
                    if (parseFloat(home.home.latitude) && parseFloat(home.home.longitude)) {
                        return (
                            <MapMarker
                                home={home}
                                lat={home.home.latitude}
                                lng={home.home.longitude}
                                score={home.percent_match}
                                key={home.home.id}
                                id={home.home.id}
                                clicked_home={this.props.clicked_home}
                                handleHomePinClick={this.props.handleHomePinClick}
                                handleHomeMarkerClick={this.props.handleHomeMarkerClick}
                                hover_id={this.props.hover_id}
                                setHoverId={this.props.setHoverId}
                                removeHoverId={this.props.removeHoverId}
                            />
                        );
                    }
                })}
                {this.props.survey ?
                    this.props.survey.tenants.map(t => {
                            if (t.commute_type) {
                                if (t.commute_type.commute_type) {
                                    // If the user put Work From Home then we don't want the destination to render
                                    if (t.commute_type.commute_type !== "Work From Home") {
                                        // Don't add the marker if the lattiude is 0,0
                                        if (parseFloat(t.latitude) && parseFloat(t.longitude)) {
                                            return (
                                                <CommuteMarker
                                                    lat={t.latitude}
                                                    lng={t.longitude}
                                                    name={t.first_name}
                                                    key={t.id}
                                                />
                                            );
                                        }
                                    }
                                }
                            }
                        }
                    )
                    :
                    null
                }
            </GoogleMapReact>
        )
    }
}

// Fit map to its bounds after the api is loaded
const apiIsLoaded = (map, maps, places) => {
    // Get bounds by our places
    const bounds = getMapBounds(map, maps, places);

    // This sets a minimum zoom.
    // This is achieved to see if the zoom size is 0 and then if it is then it adds a slight
    //  lat and lng offset which is the "minimum zoom"
    if (bounds.getNorthEast().equals(bounds.getSouthWest())) {
        var extendPoint1 = new google.maps.LatLng(bounds.getNorthEast().lat() + 0.01, bounds.getNorthEast().lng() + 0.01);
        var extendPoint2 = new google.maps.LatLng(bounds.getNorthEast().lat() - 0.01, bounds.getNorthEast().lng() - 0.01);
        bounds.extend(extendPoint1);
        bounds.extend(extendPoint2);
    }
    // Fit map to bounds
    map.fitBounds(bounds);
    // Bind the resize listener
    bindResizeListener(map, maps, bounds);
};


// Return map bounds based on list of places
const getMapBounds = (map, maps, places) => {
  const bounds = new maps.LatLngBounds();
  // This checks to see if there are any places on the map, if there
  // isn't then it just shows the center of Boston
  if (places.length === 0) {
      bounds.extend(
          new maps.LatLng(
              42.3601,
              -71.0589,
          )
      )
  } else {
      places.forEach((place) => {
          if (place.props.lat && place.props.lng) {
              bounds.extend(new maps.LatLng(
                  place.props.lat,
                  place.props.lng,
              ));
          }
      });
  }
  return bounds;
};

// Re-center map when resizing the window
const bindResizeListener = (map, maps, bounds) => {
  maps.event.addDomListenerOnce(map, 'idle', () => {
    maps.event.addDomListener(window, 'resize', () => {
      map.fitBounds(bounds);
    });
  });
};