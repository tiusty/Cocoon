import React from 'react'
import { Component } from 'react';

class HomeTile extends Component {
    render(){
        return (
            <div>
                <h1>{this.props.home.address}</h1>
            </div>
        );
    }
}
export default HomeTile
