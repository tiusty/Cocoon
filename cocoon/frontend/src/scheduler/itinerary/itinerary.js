// Import React Components
import React from 'react'
import { Component } from 'react';
import axios from 'axios'

class Itinerary extends Component {
    state = {};

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        axios.get(this.state.endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState( {surveys: this.parseData(response.data)})
            })
    }

    render() {
        return <div><h2>Itinerary</h2></div>
    }
}

export default Itinerary
