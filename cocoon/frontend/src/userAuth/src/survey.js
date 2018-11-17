import React from 'react'
import { Component } from 'react';
import HomeTile from "./homeTile";
import axios from 'axios'

import './survey.css'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'


class Survey extends Component {
    state = {
        id: this.props.survey_id,
        name: "",
        favorites:  [],
        visit_list:  [],
    };

    componentDidMount() {
        let endpoint = "http://127.0.0.1:8000/survey/api/userSurveys/" + this.state.id;
        axios.get(endpoint)
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    name: response.data.name,
                    favorites: response.data.favorites,
                    visit_list: response.data.visit_list,
                }),
            )
    }

    handleVisitClick = (home) => {
        // Function sends a home and toggles that home in the visit_list
        let endpoint = "http://127.0.0.1:8000/survey/api/userSurveys/" + this.state.id + "/";
        axios.put(endpoint,
            {
                home_id: home.id

            })
            .catch(error => console.log('BAD', error))
            .then(response =>
                this.setState({
                    visit_list: response.data.visit_list
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
        console.log('Load survey', this.state.id)
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
                        <button onClick={this.handleLoad} className="btn btn-primary btn-sm m-2">Load</button>
                        <button onClick={() => onDelete(this.state.id)} className="btn btn-danger btn-sm m-2">Delete</button>
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
