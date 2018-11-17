import React from 'react'
import { Component } from 'react';
import HomeTile from "./homeTile";
import axios from 'axios'

import './survey.css'
import survey_endpoints from '../../endpoints/survey_endpoints'

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';


class Survey extends Component {
    state = {
        id: this.props.survey_id,
        name: "",
        url: "",
        favorites:  [],
        visit_list:  [],
    };

    componentDidMount() {
        let endpoint = this.props.endpoint + this.state.id;
        axios.get(endpoint)
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    name: response.data.name,
                    favorites: response.data.favorites,
                    visit_list: response.data.visit_list,
                    url: response.data.url,
                }),
            )
    }

    handleVisitClick = (home) => {
        // Function sends a home and toggles that home in the visit_list
        let endpoint = this.props.endpoint + this.state.id + "/";
        axios.put(endpoint,
            {
                home_id: home.id,
                type: 'visit'

            })
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    visit_list: response.data.visit_list
                })
            );
    };

    handleFavoriteClick = (home) => {
        // Function sends a home and toggles that home in the visit_list
        let endpoint = this.props.endpoint + this.state.id + "/";
        axios.put(endpoint,
            {
                home_id: home.id,
                type: 'favorite',

            })
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    favorites: response.data.favorites
                })
            );
    };

    renderFavorites() {
        if (this.state.favorites.length === 0) return <h3>Please load your survey and add favorite homes</h3>;
        return (
            <div>
                {this.state.favorites.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={this.inFavorites(home)}
                        visit={this.state.visit_list.filter(c => c.id === home.id).length >0}
                        onVisitClick={this.handleVisitClick}
                        onFavoriteClick={this.handleFavoriteClick}
                        show_heart={true}
                        show_score={false}
                        show_visit={true}
                    />
                )}
            </div>
        );
    };

    inFavorites(home) {
        // Checks to see if the home exists within the favorites list
        return this.state.favorites.filter(c => c.id === home.id).length > 0;
    }

    inVisitList(home) {
        // Checks to see if the home exists within the visit_list
        return this.state.visit_list.filter(c => c.id === home.id).length >0;
    }

    renderVisitList() {
        if (this.state.visit_list.length === 0) return <h3>Please add homes to your visit list!</h3>;
        return (
            <div>
                {this.state.visit_list.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={this.inFavorites(home)}
                        visit={this.inVisitList(home)}
                        onVisitClick={this.handleVisitClick}
                        show_score={false}
                        show_heart={false}
                        show_visit={true}
                    />
                )}
            </div>
        );
    };

    handleLoad = () => {
        return survey_endpoints['rentSurveyResult'] + this.state.url + "/";
    };

    render(){
        const { onDelete } = this.props;
        return (
            <div className="Dotted_box">
                <div className="row">
                    <div className="col-md-10">
                        <h1>{this.state.name}</h1>
                    </div>
                    <div className="col-md-2">
                        <a href={this.handleLoad()} className="btn btn-primary active">Load</a>
                        <button onClick={() => onDelete(this.state.id)} className="btn btn-danger btn-sm m-2">Delete</button>
                        <button className="btn btn-success btn-sm m-2">Schedule Group!</button>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-5">
                        <h2><u>Favorites:</u></h2>
                        {this.renderFavorites()}
                    </div>
                    <div className="col-md-5">
                        <h2><u>Visit List:</u></h2>
                        {this.renderVisitList()}
                    </div>
                </div>
            </div>
        );
    }
}
export default Survey
