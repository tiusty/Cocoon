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
import SurveySubscribe from '../../common/surveySubscribe';
import HomeTile from '../../common/homeTile/homeTile';
import HomeTileLarge from '../../common/homeTile/homeTileLarge';
import Map from './map/map';
import RentForm from '../../survey/rentForm/main';
import PopUp from './popup';
import MobileToggleButton from './mobileToggleButton';

// Necessary XSRF headers for posting form
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class ResultsPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            googleApiLoaded: false,
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
            isViewingPopup: true,
            verificationEmailSent: false,
            verificationEmailLoading: false,
            lastViewedMap: false,

            /* State for mobile devices */
            isMobile: false,
            viewingMobileResults: false,
            viewingMobileMap: false,
        }
    }

    componentDidMount = () => {
        // This interval checks every .3 seconds to see if the google api loaded.
        this.interval = setInterval(() => this.checkGoogleApi(), 300);
        this.setPageHeight();
        this.getPageWidth();
        if (this.props.is_verified) {
            this.getSurvey();
            this.getResults();
        }
    };

    getPageWidth = () => {
        /*
         * Gets initial page width to determine whether or not user is on mobile (screen size < 768px)
         * Adds event listener to listen for screen resize to check if screen changes to < 768
         */
        if (window.innerWidth < 768) {
            this.setState({
                isMobile: true,
                viewingMobileResults: false,
                viewingMobileMap: true,
            })
        } else {
            this.setState({
                isMobile: false,
                viewingMobileResults: false,
                viewingMobileMap: false
            })
        }

        window.addEventListener('resize', e => {
            if (e.target.innerWidth < 768) {
                // Only change the state values if it wasn't already
                //  mobile. This prevents weird spamming of changing the page
                if (!this.state.isMobile) {
                    this.setState({
                        isMobile: true,
                        viewingMobileResults: false,
                        viewingMobileMap: true
                    })
                }
            } else {
                this.setState({
                    isMobile: false,
                    viewingMobileResults: false,
                    viewingMobileMap: false
                })
            }
        })

    }

    scrollMapToTop() {
        let selection = document.querySelector('.map-wrapper');
        if (selection) {
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }
    }

    scrollResultsToTop() {
        let selection = document.querySelector('.results-wrapper');
        if (selection) {
            selection.scrollTop = 0;
        }
    }

    handleMobileButtonClick = (link) => {
        if (this.state.isMobile) {
            if (link === 'list') {
                this.setState({
                    viewingMobileResults: true,
                    viewingMobileMap: false,
                    lastViewedMap: false,
                }, this.state.viewing_home ? this.handleCloseHomeTileLarge() : null);
            } else if (link === 'map') {
                this.setState({
                    viewingMobileResults: false,
                    viewingMobileMap: true,
                    lastViewedMap: false,
                    clicked_home: undefined,
                    viewing_home: false,
                }, this.scrollMapToTop);
            }
        }
    }

    handleMobileResultsStyle = () => {

        let style = {
            display: 'block'
        }

        if (this.state.isMobile && this.state.viewingMobileResults && !this.state.isEditing) {
            style['overflow'] = 'auto'
            return style;
        } else if (this.state.isMobile && !this.state.viewingMobileResults) {
            style = {
              position: 'absolute',
                top: -9999,
                left: -9999,
            }
        }

        return style;
    }

    handleMobileMapStyle = () => {

        let style = {
            display: 'block'
        }

        if (this.state.isMobile && this.state.viewingMobileMap) {
            return style;
        } else if (this.state.isMobile && !this.state.viewingMobileMap) {
            style = {
                position: 'absolute',
                top: -9999,
                left: -9999,
            }
        }

        return style;

    }

    checkGoogleApi() {
        /**
         * Function checks to see if the google api is loaded. This should be called on an interval.
         *  When it is, then the state is set to true and the interval is stopped
         */
        if (typeof window.google === 'object' && typeof window.google.maps === 'object') {
            // Since the key is now loaded, then stop the interval
            clearInterval(this.interval);

            // Mark that the api is now loaded
            this.setState({
                googleApiLoaded: true,
            })
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
        axios.get(survey_endpoints['rentSurvey'] + this.getSurveyUrl() + '/', {params: {type: 'by_url'}})
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    survey: response.data,
                    favorites: response.data.favorites,
                });
            })

    };

    getResults = () => {
        /**
         * Whenever the results are being retrieved remove the old list first
         */
        this.setState({
            homeList: undefined,
            isLoading: true
        }, this.handleMobileButtonClick('map'));

        /**
         * Retrieve the survey results
         */
        axios.get(survey_endpoints['rentResult'] + this.getSurveyUrl() + '/', {params: {type: 'by_url'}})
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    homeList: response.data,
                    isLoading: false,
                    isViewingPopup: true
                }, this.handleMobileButtonClick('map'));
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
                    <p>We've scoured the market to pick your personalized short list of the best places, now it's your turn to pick your favorites. The higher the score the better the match! Once you're done selecting your favorites, click <span>Tour Setup</span> above to continue.</p>
                    <SurveySubscribe survey_id={this.state.survey.id} />
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
                            missing_amenities={home.missing_amenities}
                            show_missing_amenities={true}
                        />))}
                </div>
            </>
        );
    };

    handleHomeMarkerClick = (id) => {
        /**
         * Handles clicks the home marker. The home marker should only be able to be clicked on the mobile
         *  version which is why this wrapper function is necessary
         */
        if (this.state.isMobile) {
            /* Change to list view to view home tile*/
            this.handleMobileButtonClick('list');

            this.setState({
                clicked_home: id,
                viewing_home: true,
                lastViewedMap: true,
            }, this.scrollResultsToTop);
        }
    };


    handleHomePinClick = (id) => {
        /**
         * Handles what happens when the home pin is clicked. This differs from mobile to desktop
         */
        if (!this.state.isEditing) {
            if (this.state.isMobile) {
                if (this.state.hover_id === id) {
                    this.setState({
                        hover_id: undefined,
                    })
                } else {
                    this.setState({
                        hover_id: id,
                    })
                }
            } else {
                if (this.state.clicked_home === id) {
                    this.setState({
                        clicked_home: undefined,
                        viewing_home: false,
                    });
                } else {
                    this.setState({
                        clicked_home: id,
                        viewing_home: true,
                    });
                    document.querySelector('.results-wrapper').scrollTop = 0;
                }
            }

        }
    }

    handleHomeClick = (id) => {
        /**
         * On the click of a homeTile, this sets the clicked_home id
         * to the target id to be used to render the large home tile.
        **/
        if (!this.state.isEditing) {
            this.saveScrollPosition();

            this.setState({
                clicked_home: id,
                viewing_home: true,
            });

            document.querySelector('.results-wrapper').scrollTop = 0;
        }
    };

    handleCloseHomeTileLarge = () => {
        /**
         *  Clears the clicked_home id and renders the home list
        **/
        if (!this.state.isMobile) {
            this.removeHoverId();
        }
        this.setState({
            clicked_home: undefined,
            viewing_home: false
        }, !this.state.isMobile || this.state.viewingMobileResults ? () => this.setScrollPosition() : null);
        if (this.state.isMobile) {
            if (this.state.lastViewedMap) {
                this.handleMobileButtonClick('map');
            }
        }
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
                    missing_amenities={home.missing_amenities}
                    show_missing_amenities={true}
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
            isViewingPopup: false,
            clicked_home: undefined,
            viewing_home: false
        }, () => this.state.isEditing ? document.querySelector('.results-wrapper').scrollTop = 0 : null)
    };

    renderEditingText = () => {
        if (!this.state.isEditing) {
            return 'Edit Survey';
        } else {
            return 'Cancel Changes';
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
                <a href={`${userAuth_endpoints['tourSetup']}?survey_url=${this.state.survey_name}`}>Tour Setup</a>
            );
        } else {
            return <span className="disabled-button">Tour Setup</span>
        }
    }

    renderButtonRow = () => {
        if (!this.state.viewing_home) {
            return (
                <div className="results-btn-row">
                    <div className="schedule-tour-div">
                        {this.renderScheduleButton()}
                    </div>
                    <span onClick={this.toggleEditing}><i className="material-icons">edit</i> {this.renderEditingText()}</span>
                </div>
            );
        } else {
            return null;
        }
    }

    handlePopupClose = () => {
        this.setState({
            isViewingPopup: false
        })
    }

    renderPopup = () => {
        if (this.state.isViewingPopup === true && this.state.homeList && this.state.survey && this.state.isLoading === false) {
            return (
                <PopUp
                    survey={this.state.survey}
                    homeList={this.state.homeList}
                    handlePopupClose={this.handlePopupClose}
                    editSurvey={this.toggleEditing}
                />
            );
        } else {
            return null;
        }
    }

    renderMapComponent() {
        /**
         * Renders a loading symbol until the map is ready to load
         */
        if (this.state.isLoading) {
            return <Preloader color={'var(--teal)'} size={12}/>
        } else {
            return(
                <div style={this.handleMobileMapStyle()} className="map-wrapper">
                    {this.state.homeList !== undefined && this.state.googleApiLoaded ?
                        <Map homes={this.state.homeList}
                             clicked_home={this.state.clicked_home}
                             handleHomePinClick={this.handleHomePinClick}
                             handleHomeMarkerClick={this.handleHomeMarkerClick}
                             hover_id={this.state.hover_id}
                             setHoverId={this.setHoverId}
                             removeHoverId={this.removeHoverId}
                             survey={this.state.survey} />
                        : null}

                    <MobileToggleButton
                        handleMobileButtonClick={this.handleMobileButtonClick}
                        viewingMobileResults={this.state.viewingMobileResults}
                        viewingMobileMap={this.state.viewingMobileMap}
                        isMobile={this.state.isMobile}
                        isEditing={this.state.isEditing}
                        isViewingPopup={this.state.isViewingPopup}
                        viewing_home={this.state.viewing_home} />
                </div>
            );
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
                    {this.renderPopup()}
                    <div style={this.handleMobileResultsStyle()} className={this.setResultsWrapperClass()}>
                        {this.renderButtonRow()}
                        {this.renderMainComponent()}
                    </div>
                    {this.renderMapComponent()}
                    <MobileToggleButton
                        handleMobileButtonClick={this.handleMobileButtonClick}
                        viewingMobileResults={this.state.viewingMobileResults}
                        viewingMobileMap={this.state.viewingMobileMap}
                        isMobile={this.state.isMobile}
                        isEditing={this.state.isEditing}
                        isViewingPopup={this.state.isViewingPopup}
                        viewing_home={this.state.viewing_home}/>
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