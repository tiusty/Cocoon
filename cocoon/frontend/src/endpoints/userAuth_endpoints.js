/**
 * Contains the URLS for the userAuth app
 *
 * The format/naming should match the urls.py
 */

const app_name = '/userAuth';
const api_path = app_name + '/api';

const userAuth_endpoints = {
    // Template urls
    'surveys': app_name + '/surveys/',

    // Api urls
    'resendVerificationEmail': api_path + '/resendVerificationEmail',
};

export default userAuth_endpoints;
