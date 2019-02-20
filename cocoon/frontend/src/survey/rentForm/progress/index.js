import React from 'react';

const Progress = (props) => (
    <ul className="survey-progress-bar">
        <li className={`progress-bar-step ${props.step >= 1 ? 'progress-bar-step_active' : ''}`}>General</li>
        <li className={`progress-bar-step ${props.step >= 2 ? 'progress-bar-step_active' : ''}`}>Tenants</li>
        <li className={`progress-bar-step ${props.step >= 3 ? 'progress-bar-step_active' : ''}`}>Amenities</li>
        <li className={`progress-bar-step ${props.step >= 4 ? 'progress-bar-step_active' : ''}`}>Details</li>
    </ul>
);

export default Progress;