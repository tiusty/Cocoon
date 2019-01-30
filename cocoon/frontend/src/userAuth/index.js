// Import React Components
import React from 'react';
import ReactDOM from "react-dom";

// Import Cocoon Components
import Surveys from "./survey/mysurveys";

// Determines which component to load via dictionary
//  This should be passed in the context to the template
const components = {
    'Surveys': Surveys,
};

ReactDOM.render(
    React.createElement(components[window.component], window.props),
    window.react_mount
);
