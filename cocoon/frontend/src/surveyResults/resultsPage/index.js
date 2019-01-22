// Import React Components
import React, { Component } from 'react';
import axios from 'axios';

// Import Cocoon Components
import '../../common/styles/variables.css';
import './resultsPage.css';
import survey_endpoints from '../../endpoints/survey_endpoints';
import HomeTile from '../../common/homeTile/homeTile';
import HomeTileLarge from '../../common/homeTile/homeTileLarge';
import Map from './map/map'


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
            clicked_home: undefined,
            hover_id: undefined,
            viewing_home: false,
            scroll_position: undefined
        }
    }

    componentDidMount = () => {
        this.setPageHeight();
        this.getSurveyId();
        this.getResults();
    }

    getSurveyId = () => {
        /**
         * Retrieves the Survey Id by passing the survey url
         */
        axios.get(survey_endpoints['rentSurvey'] + this.getSurveyUrl(), {params: {type: 'by_url'}})
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    survey: response.data
                });
            })

    };

    getResults = () => {
        axios.get(survey_endpoints['rentResult'] + this.getSurveyUrl())
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    homeList: response.data
                }, () => console.log(this.state.homeList));
            })
    }

    getSurveyUrl = () => {
        const url = window.location.pathname.split('/');
        const name =  url[url.length - 2];
        this.setState({
            survey_name: name
        });
        return name;
    }

    setScrollPosition = () => {

    }

    setPageHeight = () => {
        document.querySelector('body').style.overflow = 'hidden';
        document.querySelector('.navbar').style.margin = 0;
        document.querySelector('#siteWrapper').style.width = '100%';
        document.querySelector('#siteWrapper').style.height = 'auto';
        document.querySelector('#siteWrapper').style.padding = 0;
        document.querySelector('#reactWrapper').style.height = 'calc(100vh - 60px)';
    }

    setHoverId = (id) => {
        console.log(id)
        // this.setState({
        //     hover_id: id
        // })
    }

    removeHoverId = () => {
        // this.setState({
        //     hover_id: undefined
        // })
    }

    handleFavoriteClick = (home) => {
        /**
         * This function handles toggles a home to either add or remove from the favorites list
         *
         * The response includes the updated favorite and visit list for the survey
         * @type {string}
         */
        // The survey id is passed to the put request to update the state of that particular survey
        let endpoint = survey_endpoints['rentSurvey'] + this.state.survey_id + "/";
        axios.put(endpoint,
            {
                home_id: home.id,
                type: 'favorite_toggle',

            })
            .catch(error => console.log('BAD', error))
            // Though the favorites is being updated, the response includes the visit list so update with the
            // latest visit list as well
            .then(response =>
                this.setState({
                    favorites: response.data.favorites,
                    visit_list: response.data.visit_list,
                })
            );
    }

    renderResults = () => {
        return (
            <>
                <div className="results-info">
                    <h2>Time to pick your favorites!</h2>
                    <p>We've scoured the market to pick your personalized short list of the best places, now it's your turn to pick your favorites.</p>
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
                            visit={false}
                            favorite={false}
                            onMouseEnter={() => this.setHoverId(home.home.id)}
                            onMouseLeave={this.removeHoverId}
                            onHomeClick={() => this.handleHomeClick(home.home.id)}
                            onFavoriteClick={() => this.handleFavoriteClick(home.home)}

                        />))}
                </div>
            </>
        );
    }

    handleHomeClick = (id) => {
        this.setState({
            clicked_home: id,
            viewing_home: true
        })
        document.querySelector('.results-wrapper').scrollTop = 0;
    }

    handleCloseHomeTileLarge = () => {
        this.setState({
            clicked_home: undefined,
            viewing_home: false
        })
    }

    renderLargeHome = () => {
        let home = this.state.homeList.find(home => home.home.id === this.state.clicked_home);
        return (
            <div className="expanded-wrapper">
                <HomeTileLarge
                    home={home.home}
                    // favorite={this.inFavorites(home)}
                    // onFavoriteClick={this.props.onFavoriteClick}
                    onCloseHomeTileLarge={this.handleCloseHomeTileLarge}
                    displayPercent={true}
                    percent_match={home.percent_match}
                />
            </div>
        );
    }

    render() {
        return (
            <div id="results-page">
                <div className="results-wrapper">
                    <div className="results-btn-row">
                        <span>Schedule Tour</span>
                        <span><i className="material-icons">edit</i> Edit Survey</span>
                    </div>
                    {this.state.viewing_home === false ? this.renderResults() : this.renderLargeHome()}
                </div>
                <div className="map-wrapper">
                    {this.state.homeList !== undefined ? <Map homes={this.state.homeList} /> : null}
                </div>
            </div>
        )
    }
}