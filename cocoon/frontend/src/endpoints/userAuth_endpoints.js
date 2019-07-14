/**
 * Contains the URLS for the userAuth app
 *
 * The format/naming should match the urls.py
 */

const app_name = '/userAuth';
const api_path = app_name + '/api';

const userAuth_endpoints = {
    // Template urls
    'tourSetup': app_name + '/tourSetup/',

    // Api urls
    'resendVerificationEmail': api_path + '/resendVerificationEmail/',
    'agentClients': api_path + '/agentClients/',
};

export default userAuth_endpoints;
