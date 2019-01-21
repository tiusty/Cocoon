// Import React Components
import React from 'react';
import ReactDOM from "react-dom";

// Import Cocoon Components
import ResultsPage from "./resultsPage";

// Determines which component to load via dictionary
//  This should be passed in the context to the template
const components = {
    'SurveyResults': ResultsPage,
};

ReactDOM.render(
    React.createElement(components[window.component], window.props),
    window.react_mount
);

// We've scoured the market to pick your personalized short list of
// the best places, now it's your turn to pick your favorites