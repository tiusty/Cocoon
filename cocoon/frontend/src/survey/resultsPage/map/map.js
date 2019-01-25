// Import React Components
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import GoogleMapReact from 'google-map-react';

import MapMarker from './mapMarker';
import CommuteMarker from './commuteMarker';

export default class Map extends Component {

    constructor(props) {
        super(props);
        this.state = {
            commutes: []
        }
    }

    static defaultProps = {
        center: {
            lat: 42.36,
            lng: -71.05
        },
        zoom: 11
    }

    componentDidUpdate(prevProps) {
        if (this.props.survey !== prevProps.survey) {
            this.getCommuteCoords();
        }
    }

    getMapStyle = () => {
        const mapStyle = [
            {
                "featureType": "all",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "simplified"
                    },
                    {
                        "color": "#5b6571"
                    },
                    {
                        "lightness": "35"
                    }
                ]
            },
            {
                "featureType": "administrative.neighborhood",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "landscape",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#f3f4f4"
                    }
                ]
            },
            {
                "featureType": "landscape.man_made",
                "elementType": "geometry",
                "stylers": [
                    {
                        "weight": 0.9
                    },
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#83cead"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#fee379"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway.controlled_access",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "simplified"
                    },
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#7fc8ed"
                    }
                ]
            }
        ];
        return mapStyle;
    }

    getCommuteCoords = () => {
        let commutes = [];
        this.props.survey.tenants.forEach(t => {
            if (t.street_address) {
                let address = `${t.street_address} ${t.city} ${t.state} ${t.zip_code}`;
                let coords = {};
                const geocoder = new google.maps.Geocoder();
                geocoder.geocode( { 'address': address }, (results, status) => {
                    if (status === google.maps.GeocoderStatus.OK) {
                        coords.lat = results[0].geometry.location.lat();
                        coords.lng = results[0].geometry.location.lng();
                        commutes.push(coords)
                    }
                });
            }
        })
        this.setState({
            commutes: commutes
        })
    }

    renderCommutes = () => {
        if (this.state.commutes.length > 0) {
            console.log(this.state.commutes)
            this.state.commutes.map(commute => (
                <CommuteMarker
                    lat={commute.lat}
                    lng={commute.lng}
                    key={commute.lat}
                />
            ))
        }
    }

    render() {

        const mapOptions = {
            styles: this.getMapStyle()
        }

        let homesCopy = [...this.props.homes];

        return (
            <GoogleMapReact
                defaultCenter={this.props.center}
                defaultZoom={this.props.zoom}
                options={mapOptions}
                handleHomeClick={this.props.handleHomeClick}
                hover_id={this.props.hover_id}
                setHoverId={this.props.setHoverId}
                removeHoverId={this.props.removeHoverId}
            >
                {this.props.homes && homesCopy.reverse().map(home => (
                    <MapMarker
                        lat={home.home.latitude}
                        lng={home.home.longitude}
                        score={home.percent_match}
                        key={home.home.id}
                        id={home.home.id}
                        hover_id={this.props.hover_id}
                        handleHomeClick={this.props.handleHomeClick}
                        setHoverId={this.props.setHoverId}
                        removeHoverId={this.props.removeHoverId}
                    />
                ))}

            </GoogleMapReact>
        )
    }
}

Map.propTypes = {
    homes: PropTypes.array.isRequired
}