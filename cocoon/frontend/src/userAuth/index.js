import React from 'react';
import { Component } from 'react';
import ReactDOM from "react-dom";

import './userAuth.css';
import Main from './src/main'

class UserAuth extends Component {
    componentDidMount = () => {
        console.log('rendered!');
    };

    render(){
        return (
           <Main/>
        );
    }
}


ReactDOM.render(
    React.createElement(UserAuth, window.props),
    window.react_mount
);
