import React from 'react';
import ReactDOM from "react-dom";

import RentForm from './main';
import './rentForm.css';

ReactDOM.render(<RentForm is_authenticated={window.isUser} />, window.react_mount);