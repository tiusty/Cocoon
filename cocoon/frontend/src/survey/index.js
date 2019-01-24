// Import React Components
import React from 'react';
import ReactDOM from "react-dom";

// Import Cocoon Components
import RentForm from './rentForm/main/index';

const components = {
    'RentingSurveyTemplate': <RentForm is_authenticated={window.isUser} />,
};

ReactDOM.render(components[window.component], window.react_mount);