// Import React Components
import React, { Component } from 'react';
import axios from 'axios';

// Import Cocoon Components
import '../../common/styles/variables.css';
import './resultsPage.css';
import BlurredImg from './not-verified-bg.jpg';
import BlurredImg2 from './not-verified-bg-2.jpg';
import BlurredImg3 from './not-verified-bg-3.jpg';


import survey_endpoints from '../../endpoints/survey_endpoints';
import userAuth_endpoints from '../../endpoints/userAuth_endpoints';

import Preloader from '../../common/preloader';
import HomeTile from '../../common/homeTile/homeTile';
import HomeTileLarge from '../../common/homeTile/homeTileLarge';
import Map from './map/map';
import RentForm from '../../survey/rentForm/main';


// Necessary XSRF headers for posting form
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class ResultsPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            homeList: undefined,
            survey_name: undefined,
            survey: undefined,
            favorites: [],
            commutes: [],
            clicked_home: undefined,
            hover_id: undefined,
            viewing_home: false,
            scroll_position: undefined,
            isEditing: false,
            isLoading: true,
            center: undefined,
            verificationEmailSent: false,
            verificationEmailLoading: false,
        }
    }

    componentDidMount = () => {
        this.setPageHeight();
        if (this.props.is_verified) {
            this.getSurvey();
            this.getResults();
        }
    }

    handleUpdateSurvey = (survey) => {
        /**
         * This is passed the new survey and saves it to the state.
         *  Also after updating the survey it calls the getResults function to get the new results
         */
        this.setState({
            survey: survey,
            favorites: survey.favorites,
            isEditing: false,
            viewing_home: false,
        }, () => this.getResults())
    };

    getSurvey = () => {
        /**
         * Retrieves the Survey by passing the survey url
         */
        axios.get(survey_endpoints['rentSurvey'] + this.getSurveyUrl(), {params: {type: 'by_url'}})
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    survey: response.data,
                    tenants: response.data.tenants,
                    favorites: response.data.favorites,
                    commutes: this.getCommuteCoords(response.data.tenants)
                });
            })

    };

    getCommuteCoords = (tenants) => {
        let commutes = [];
        if (tenants) {
            tenants.forEach(t => {
                if (t.street_address) {
                    let address = `${t.street_address} ${t.city} ${t.state} ${t.zip_code}`;
                    let name = `${t.first_name}`;
                    let coords = {};
                    const geocoder = new google.maps.Geocoder();
                    geocoder.geocode( { 'address': address }, (results, status) => {
                        if (status === google.maps.GeocoderStatus.OK) {
                            console.log(results);
                            coords.lat = results[0].geometry.location.lat();
                            coords.lng = results[0].geometry.location.lng();
                            coords.name = name;
                            commutes.push(coords);
                        }
                    });
                }
            })
        }
        return commutes;
    };

    getResults = () => {
        /**
         * Whenever the results are being retrieved remove the old list first
         */
        this.setState({
            homeList: [],
            isLoading: true
        });

        /**
         * Retrieve the survey results
         */
        axios.get(survey_endpoints['rentResult'] + this.getSurveyUrl())
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    homeList: response.data,
                    isLoading: false
                });
            })
    };

    getSurveyUrl = () => {
        /**
         * Retrieve the survey url via the web url
         * @type {string[]}
         */
        const url = window.location.pathname.split('/');
        const name =  url[url.length - 2];
        this.setState({
            survey_name: name
        });
        return name;
    };

    setPageHeight = () => {
        /**
         *  On render this function resizes the divs to be 100% off the screen
         *  size. Also disables the scroll for the body element
        **/
        document.querySelector('body').style.overflow = 'hidden';
        document.querySelector('#siteWrapper').style.width = '100%';
        document.querySelector('#siteWrapper').style.height = 'auto';
        document.querySelector('#siteWrapper').style.padding = 0;
        document.querySelector('#reactWrapper').style.height = 'calc(100vh - 60px)';
    };

    setHoverId = (id) => {
        /**
         *  On hover this sets the hover_id to
         *  the id of the home.
         *  Active on the home tiles and map markers
        **/
        this.setState({
            hover_id: id
        })
    };

    removeHoverId = () => {
        /**
         *  Removes the hover_id on mouse leave
        **/
        this.setState({
            hover_id: undefined
        })
    };

    handleFavoriteClick = (home) => {
        /**
         * This function handles toggles a home to either add or remove from the favorites list
         *
         * The response includes the updated favorite and visit list for the survey
         * @type {string}
         */
        // The survey id is passed to the put request to update the state of that particular survey
        let endpoint = survey_endpoints['rentSurvey'] + this.state.survey.id + "/";
        axios.put(endpoint,
            {
                home_id: home.id,
                type: 'favorite_toggle',

            })
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    favorites: response.data.favorites,
                })
            );
    };

    renderResults = () => {
        /**
         *  Renders the list of home tiles
        **/
        return (
            <>
                <div className="results-info">
                    <h2>Time to pick your favorites!</h2>
                    <p>We've scoured the market to pick your personalized short list of the best places, now it's your turn to pick your favorites. The higher the score the better the match! Once you're done favoriting, click <span>schedule tour</span> above to continue.</p>
                </div>
                <div className="results">
                    {this.state.homeList && this.state.homeList.map(home => (
                        <HomeTile
                            id={home.home.id}
                            isLarge={true}
                            displayPercent={true}
                            percent_match={home.percent_match}
                            key={home.home.id}
                            home={home.home}
                            canVisit={false}
                            visit={false}
                            favorite={this.state.favorites.filter(fav => fav.id === home.home.id).length > 0}
                            onHomeClick={() => this.handleHomeClick(home.home.id)}
                            onFavoriteClick={() => this.handleFavoriteClick(home.home)}
                            onMouseLeave={() => this.removeHoverId(home.home.id)}
                            onMouseEnter={() => this.setHoverId(home.home.id)}
                        />))}
                </div>
            </>
        );
    };

    handleHomeClick = (id) => {
        /**
         * On the click of a homeTile or map marker, this sets the clicked_home id
         * to the target id to be used to render the large home tile.
        **/
        this.saveScrollPosition();
        this.setState({
            clicked_home: id,
            viewing_home: true
        });
        document.querySelector('.results-wrapper').scrollTop = 0;
    };

    handleCloseHomeTileLarge = () => {
        /**
         *  Clears the clicked_home id and renders the home list
        **/
        this.removeHoverId();
        this.setState({
            clicked_home: undefined,
            viewing_home: false
        }, () => this.setScrollPosition())
    };

    renderLargeHome = () => {
        let home = this.state.homeList.find(home => home.home.id === this.state.clicked_home);
        return (
            <div className="expanded-wrapper">
                <HomeTileLarge
                    home={home.home}
                    onFavoriteClick={() => this.handleFavoriteClick(home.home)}
                    favorite={this.state.favorites.filter(fav => fav.id === home.home.id).length > 0}
                    onCloseHomeTileLarge={this.handleCloseHomeTileLarge}
                    displayPercent={true}
                    percent_match={home.percent_match}
                />
            </div>
        );
    };

    toggleEditing = () => {
        /**
         *  Renders the survey
        **/
        this.setState({
            isEditing: !this.state.isEditing,
            clicked_home: undefined,
            viewing_home: false
        }, () => this.state.isEditing ? document.querySelector('.results-wrapper').scrollTop = 0 : null)
    };

    renderEditingText = () => {
        if (!this.state.isEditing) {
            return 'Edit Survey';
        } else {
            return 'Cancel Survey';
        }
    };

    renderEmptyHomes = () => {
        return (
            <div className="results-info empty-results">
                <h2>Nothing's here!</h2>
                <p>Sorry, no homes exist for your requirements. Please update your survey criteria.</p>
                <span onClick={this.toggleEditing}>Edit Survey</span>
            </div>
        );
    };

    renderMainComponent = () => {
        if (!this.state.viewing_home && !this.state.isEditing) {
            if (this.state.isLoading) {
                return <Preloader color={'var(--teal)'} size={12} />
            } if (!this.state.isLoading && (!this.state.homeList || this.state.homeList.length === 0)) {
                return this.renderEmptyHomes();
            } else {
                return this.renderResults();
            }
        } else if (this.state.viewing_home && !this.state.isEditing) {
            return this.renderLargeHome();
        } else if (this.state.isEditing) {
            return <RentForm survey={this.state.survey} is_authenticated={true} onUpdateSurvey={this.handleUpdateSurvey} is_editing={true}/>
        }
    };

    saveScrollPosition = () => {
        if (document.querySelector('.homelist-wrapper')) {
            const homeList = document.querySelector('.homelist-wrapper');
            this.setState({
                scroll_position: homeList.scrollTop
            })
        }
    };

    setScrollPosition = () => {
        const homeList = document.querySelector('.results-wrapper');
        homeList.scrollTop = this.state.scroll_position;
    };

    setResultsWrapperClass = () => {
        let wrapper_class = 'results-wrapper';
        if (this.state.viewing_home === false && this.state.isEditing === false) {
            wrapper_class += ' homelist-wrapper';
        }
        return wrapper_class;
    };

    resendConfirmationEmail = () => {

        if (!this.state.verificationEmailLoading) {
            // Patch request needs an id, but in reality it isn't needed so none is sent
            this.setState({
                verificationEmailLoading: true,
            });
            let endpoint = userAuth_endpoints['resendVerificationEmail'] + 'none/';
            axios.patch(endpoint)
                .catch(error => console.log('BAD', error))
                .then(response =>
                    {
                        if (response.data.result) {
                            this.setState({
                                verificationEmailSent: true,
                                verificationEmailLoading: false,
                            })
                        }
                    }
                );
        }
    };

    renderScheduleButton = () => {
        if (this.state.favorites.length > 0) {
            return (
                <a href={userAuth_endpoints['surveys']}>Schedule Tour</a>
            );
        } else {
            return <span className="disabled-button">Schedule Tour</span>
        }
    }

    renderButtonRow = () => {
        if (!this.state.viewing_home) {
            return (
                <div className="results-btn-row">
                    <div className="schedule-tour-div">
                        {this.renderScheduleButton()}
                        {/*<p>Done favoriting homes? Click below to continue</p>*/}
                        {/*<a href={userAuth_endpoints['surveys']}>Schedule Tour</a>*/}
                    </div>
                    <span onClick={this.toggleEditing}><i className="material-icons">edit</i> {this.renderEditingText()}</span>
                </div>
            );
        } else {
            return null;
        }
    }

    handleVerification = () => {
        /**
         *  If the user is verified this will render the normal page.
         *  And if not verified, they will have the resend confirmation email modal
        **/
        if (this.props.is_verified) {
            return (
                <div id="results-page">
                    <div className={this.setResultsWrapperClass()}>
                        {this.renderButtonRow()}
                        {this.renderMainComponent()}
                    </div>
                    <div className="map-wrapper">
                        {this.state.homeList !== undefined ? <Map homes={this.state.homeList} handleHomeClick={this.handleHomeClick} hover_id={this.state.hover_id} setHoverId={this.setHoverId} removeHoverId={this.removeHoverId} commutes={this.state.commutes} /> : null}
                    </div>
                </div>
            );
        } else {
            const imgArray = [BlurredImg, BlurredImg2, BlurredImg3];
            const randomImage = imgArray[Math.floor(Math.random() * imgArray.length)]
            return (
              <div id="unverified-wrapper" style={{backgroundImage: `url(${randomImage})`}}>
                  <div className="unverified-modal">
                      <h2>Confirm your email before viewing your results.</h2>
                      {this.state.verificationEmailSent ? <p>Email sent!</p> : null}
                      <button className="btn btn-primary" onClick={this.resendConfirmationEmail}>
                          {this.state.verificationEmailLoading ? 'Loading' : 'Resend confirmation email'}
                      </button>
                      <h3>Please refresh your page once you confirm your email</h3>
                  </div>
              </div>
            );
        }
    }

    render() {
        return this.handleVerification();
    }
}