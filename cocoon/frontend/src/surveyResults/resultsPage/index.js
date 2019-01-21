// Import React Components
import React, { Component } from 'react';
import axios from 'axios';

// Import Cocoon Components
import '../../common/styles/variables.css';
import './resultsPage.css';
import survey_endpoints from '../../endpoints/survey_endpoints';
// import HomeTiles from '../../common/homeTile/homeTiles';
import HomeTile from '../../common/homeTile/homeTile';
// import HomeTileLarge from '../../common/homeTile/homeTileLarge';
import Map from './map/map'


// Necessary XSRF headers for posting form
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default class ResultsPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            homeList: undefined
        }
    }

    componentDidMount = () => {
        this.setPageHeight();
        axios.get(survey_endpoints['rentResult'] + '/' + this.getSurveyUrl())
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    homeList: response.data
                }, () => console.log(this.state.homeList))
            })
    }

    getSurveyUrl = () => {
        const url = window.location.pathname.split('/');
        return url[url.length - 2];
    }

    setPageHeight = () => {
        document.querySelector('body').style.overflow = 'hidden';
        document.querySelector('.navbar').style.margin = 0;
        document.querySelector('#siteWrapper').style.width = '100%';
        document.querySelector('#siteWrapper').style.height = 'auto';
        document.querySelector('#siteWrapper').style.padding = 0;
        document.querySelector('#reactWrapper').style.height = 'calc(100vh - 60px)';
    }

    renderHomeList = () => {
        if (this.state.homeList) {

            // return <HomeTiles homes={this.state.homeList} />

            // this.state.homeList.map(home => (
            //     <HomeTile isLarge={true} displayPercent={true} home={home.home} visit={false} favorite={false} onHomeClick={console.log('home click')} onVisitClick={console.log('visit click')} />
            // ))

            return (
                <>
                <HomeTile isLarge={true} home={this.state.homeList[0].home} displayPercent={true} percent_match={this.state.homeList[0].percent_match} />
                <HomeTile isLarge={true} home={this.state.homeList[1].home} displayPercent={true} percent_match={this.state.homeList[1].percent_match} />
                <HomeTile isLarge={true} home={this.state.homeList[2].home} displayPercent={true} percent_match={this.state.homeList[2].percent_match} />
                <HomeTile isLarge={true} home={this.state.homeList[3].home} displayPercent={true} percent_match={this.state.homeList[3].percent_match} />
                </>
            )
        }
    }

    render() {
        return (
            <div id="results-page">
                <div className="results-wrapper">
                    <div className="results-btn-row">
                        <span>Schedule Tour</span>
                        <span><i className="material-icons">edit</i> Edit Survey</span>
                    </div>
                    <div className="results-info">
                        <h2>Time to pick your favorites!</h2>
                        <p>We've scoured the market to pick your personalized short list of the best places, now it's your turn to pick your favorites.</p>
                    </div>
                    <div className="results">
                        {this.renderHomeList()}
                    </div>
                </div>
                <div className="map-wrapper">
                    <Map homes={this.state.homeList} />
                </div>
            </div>
        )
    }
}