// Import React Components
import React from 'react';
import ReactDOM from "react-dom";

// Import Cocoon Components
import Surveys from "./survey/mysurveys";
import MyClients from "./survey/myclients"

// Determines which component to load via dictionary
//  This should be passed in the context to the template
const components = {
    'Surveys': Surveys,
    'MyClients': MyClients,
};

ReactDOM.render(
    React.createElement(components[window.component], window.props),
    window.react_mount
);
