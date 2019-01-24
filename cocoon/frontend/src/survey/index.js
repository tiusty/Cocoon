// Import React Components
import React from 'react';
import ReactDOM from "react-dom";

// Import Cocoon Components
import RentForm from './rentForm/main/index';
import ResultsPage from "./resultsPage";

const components = {
    'RentingSurveyTemplate': <RentForm is_authenticated={window.isUser} />,
    'RentingResultTemplate': <ResultsPage/>,
};

ReactDOM.render(components[window.component], window.react_mount);