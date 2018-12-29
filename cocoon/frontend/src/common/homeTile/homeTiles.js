// Import React Components
import React from 'react'
import { Component } from 'react';
import HomeTile from "./homeTile";

export default class HomeTiles extends Component {

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
        return this.props.visit_list.filter(c => c.id === home.id).length >0;
    }

    render() {
        return (
            <>
                {this.props.homes.map(home =>
                    <HomeTile
                        key={home.id}
                        home={home}
                        favorite={this.inFavorites(home)}
                        visit={this.inVisitList(home)}
                        onVisitClick={this.props.onVisitClick}
                        onFavoriteClick={this.props.onFavoriteClick}
                    />
                )}
            </>
        );
    }
}

