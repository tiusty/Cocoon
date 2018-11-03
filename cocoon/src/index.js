import React from 'react';
import ReactDOM from 'react-dom';

import Survey from './pages/survey';

const pages = {
    'survey': Survey
};

ReactDOM.render(
    React.createElement(pages[window.component], window.props),
    window.react_mount
);