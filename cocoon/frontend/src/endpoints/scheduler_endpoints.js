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
    'itineraryAgent': api_path + '/itineraryAgent/',
    'itineraryMarket': api_path + '/itineraryMarket/',
    'unscheduleItinerary': 'scheduler/unscheduleItinerary',
};

export default scheduler_endpoints;
