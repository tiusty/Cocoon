import React from 'react';
import ReactDOM from "react-dom";

import './userAuth.css';
import Surveys from "./src/surveys";

const components = {
    'Surveys': Surveys,
};

ReactDOM.render(
    React.createElement(components[window.component], window.props),
    window.react_mount
);
