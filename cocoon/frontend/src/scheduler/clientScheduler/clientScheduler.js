// Import React Components
import React from 'react'
import { Component } from 'react';
import Itinerary from "../itinerary/itinerary";

class ClientScheduler extends Component {
    state = {};

    render() {
        return (
            <React.Fragment>
                <div className='row'>
                    <div className='col-md-4'>
                        <Itinerary/>
                    </div>
                    <div className='col-md-8'>
                        <h2>Hi</h2>
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default ClientScheduler