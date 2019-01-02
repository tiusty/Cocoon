// Import React Components
import React from 'react';
import ReactDOM from "react-dom";

// Import Cocoon Components
import RentForm from './rentForm/main/index';

const components = {
    'RentingSurvey': RentForm
};

ReactDOM.render(<RentForm is_authenticated={window.isUser} />, window.react_mount);