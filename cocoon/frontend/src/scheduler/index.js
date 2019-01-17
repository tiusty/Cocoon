// Import React Components
import React from 'react';
import ReactDOM from "react-dom";
import ClientScheduler from "./clientScheduler/clientScheduler";
import AgentSchedulerPortal from "./agentScheduler/agentSchedulerPortal";
import AgentSchedulerMarketplace from "./agentScheduler/agentSchedulerMarketplace";

// Determines which component to load via dictionary
//  This should be passed in the context to the template
const components = {
    'ClientSchedulerView': ClientScheduler,
    'AgentSchedulerPortalView': AgentSchedulerPortal,
    'AgentSchedulerMarketplaceView': AgentSchedulerMarketplace,
};

ReactDOM.render(
    React.createElement(components[window.component], window.props),
    window.react_mount
);
