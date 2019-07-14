/**
 * Contains the URLS for the scheduler app
 *
 * The format/naming should match the urls.py for the scheduler app
 * @type {string}
 */
const app_name = '/scheduler';
const api_path = app_name + '/api';

const scheduler_endpoints = {
    'itinerary': api_path + '/itinerary/',
    'itineraryClient': api_path + '/itineraryClient/',
    'itineraryAgent': api_path + '/itineraryAgent/',
    'itineraryMarket': api_path + '/itineraryMarket/',
    'unscheduleItinerary': '/scheduler/unscheduleItinerary',
    'itineraryDuration': api_path + '/itineraryDuration/',
    'clientScheduler': '/scheduler/clientScheduler',
    'itineraryPage': '/scheduler/itineraryPage/',
    'agentSchedulerPortal': '/scheduler/agentSchedulerPortal/'
};

export default scheduler_endpoints;
