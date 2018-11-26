import React from 'react'
import { Component } from 'react';
import HomeTile from "../../common/homeTile/homeTile";
import axios from 'axios'

import './survey.css'
import survey_endpoints from '../../endpoints/survey_endpoints'
import CSRFToken from '../../common/csrftoken';

import { confirmAlert } from 'react-confirm-alert'; // Import
import 'react-confirm-alert/src/react-confirm-alert.css' // Import css

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';


class Survey extends Component {
    state = {
        id: this.props.survey_id,
        name: "",
        url: "",
        price: 0,
        favorites:  [],
        curr_favorites: [],
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
                    curr_favorites: response.data.favorites,
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
                    curr_favorites: response.data.favorites
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
        return this.state.curr_favorites.filter(c => c.id === home.id).length > 0;
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
                        onFavoriteClick={this.handleFavoriteClick}
                        show_score={false}
                        show_heart={true}
                        show_visit={true}
                    />
                )}
            </div>
        );
    };

    handleDelete = () => {
        /*
            Opens a confirmation page first before the survey is deleted.
                If the user clicks yes then the survey gets deleted, if
                no then nothing happens
         */
        confirmAlert({
            title: 'Confirmation',
            message: "Are you sure you want to delete " + this.state.name + "?",
            buttons: [
                {
                    label: 'yes',
                    onClick: () => this.props.onDelete(this.state.id)
                },
                {
                    label: 'No',
                }
            ]
        })
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
                        <a href={this.handleLoad()} className="btn btn-primary">Load</a>
                        <button onClick={this.handleDelete} className="btn btn-danger btn-sm m-2">Delete</button>
                        <form method="post">
                            <CSRFToken/>
                            <button name="submit-button" className="btn btn-success btn-sm m-2" value={this.state.id} type="submit">Schedule Group!</button>
                        </form>
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
