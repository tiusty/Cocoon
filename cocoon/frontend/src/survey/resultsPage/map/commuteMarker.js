// Import React Components
import React, { Component } from 'react';

export default class CommuteMarker extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div
                style={ { position: 'absolute', transform: 'translate(-50%, -50%)' } }
                className={'map-marker commute-marker'}>
                {`${this.props.name}'s Commute`}
            </div>
        )
    }
}