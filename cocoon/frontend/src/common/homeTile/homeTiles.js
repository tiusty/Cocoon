// Import React Components
import React from 'react'
import {Component} from 'react';
import HomeTile from "./homeTile";
import HomeTileLarge from "./homeTileLarge";

export default class HomeTiles extends Component {
    state = {
        home_click_id: undefined,
    };

    inFavorites(home) {
        /**
         * Tests whether a particular home is currently favorited
         */
        // Checks to see if the home exists within the favorites list
        return this.props.curr_favorites.filter(c => c.id === home.id).length > 0;
    }

    inVisitList(home) {
        /**
         * Tests if a particular home is currently in the visit list
         */
        // Checks to see if the home exists within the visit_list
        return this.props.visit_list.filter(c => c.id === home.id).length > 0;
    }

    handleHomeClick = (home_id) => {
        this.setState({home_click_id: home_id})
    }

    handleCloseHomeTileLarge = () => {
        this.setState(({
            home_click_id: undefined
        }))
    }

    renderPage() {
        if (this.state.home_click_id === undefined) {
            return (
                this.props.homes.map(home =>
                    <HomeTile
                        key={home.id}
                        id={home.id}
                        home={home}
                        favorite={this.inFavorites(home)}
                        visit={this.inVisitList(home)}
                        onVisitClick={this.props.onVisitClick}
                        onFavoriteClick={this.props.onFavoriteClick}
                        onHomeClick={this.handleHomeClick}
                    />
                )
            );
        } else {
            return (
                <HomeTileLarge
                    home={this.props.homes.find(home => home.id === this.state.home_click_id)}
                    onCloseHomeTileLarge={this.handleCloseHomeTileLarge}
                />
            );
        }
    }

    render() {
        return (
            <>
                {this.renderPage()}
            </>
        );
    }
}

