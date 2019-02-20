// Import React Components
import React from 'react'
import {Component} from 'react';
import PropTypes from 'prop-types';

// Cocoon Modules
import HomeTile from "./homeTile";
import HomeTileLarge from "./homeTileLarge";

export default class HomeTiles extends Component {
    /**
     * This component holds the list of homes for a survey. This component switches between displaying
     *  all the homes and then also displaying a large tile for when a home is clicked on for more information
     *
     * Props:
     *  this.props.homes: (RentDatabase Model) -> A list of homes that are displayed
     *  this.props.visit_list: (RentDatabase Model) -> The list of homes in the visit list
     *  this.props.favorites: (RentDatabase Model) -> The list of homes in the favorites list
     *  this.props.onVisitClick: (function(RentDatabase Model, event)) -> Handles when the visit button is pressed
     *  this.props.onFavoriteClick: (function(RentDatabase Model, event)) -> Handles when the favorite button is clicked
     *  this.props.canVisit: (boolean) -> Determines if the visit button should show up for the home
     *  this.props.canFavorite: (boolean) -> Determines if the favorite button should show up for the home
     */
    state = {
        home_click_id: undefined,
    };

    componentDidUpdate(prevProps) {
        // When the home list changes then check to see if the home exists in the list, if it doesn't then set
        //  the home_click_id to undefined. This usually happens when the user clicks the visit button/ favorite button
        //  while the large home tile is open
        if (prevProps.homes !== this.props.homes) {
            if(!this.props.homes.find(home => home.id === this.state.home_click_id)) {
                this.setState({home_click_id: undefined})
            }
        }
    }

    inFavorites(home) {
        /**
         * Tests whether a particular home is currently favorited
         */
        // Checks to see if the home exists within the favorites list
        return this.props.favorites.filter(c => c.id === home.id).length > 0;
    }

    inVisitList(home) {
        /**
         * Tests if a particular home is currently in the visit list
         */
        // Checks to see if the home exists within the visit_list
        return this.props.visit_list.filter(c => c.id === home.id).length > 0;
    }

    handleHomeClick = (home_id) => {
        /**
         * Handles when a particular home tile is clicked on
         */
        this.setState({home_click_id: home_id})
    };

    handleCloseHomeTileLarge = () => {
        /**
         * Handles when the particular home tile is closed
         */
        this.setState(({
            home_click_id: undefined
        }))
    };

    renderPage() {
        /**
         * Renders the page based on the state
         */

        // Loads all the homes when no home is clicked on
        // Note: Although the home_click_id is set to undefined in the componentDidUpdate, setState takes a little bit of time
        //  to update, so a check here is necessary to display the small home tile before the componentDidUpdate will update
        // the home_click_id state to null
        if (this.state.home_click_id === undefined || !this.props.homes.find(home => home.id === this.state.home_click_id)) {
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
                        canVisit={this.props.canVisit}
                        canFavorite={this.props.canFavorite}
                        displayPercent={this.displayPercent}
                        onMarket={home.on_market}
                        displayOnMarket={true}
                    />
                )
            );
        // Loads one home with extra info when it was clicked on
        } else {
            let home = this.props.homes.find(home => home.id === this.state.home_click_id);
            return (
                <HomeTileLarge
                    home={home}
                    favorite={this.inFavorites(home)}
                    visit={this.inVisitList(home)}
                    onVisitClick={this.props.onVisitClick}
                    onFavoriteClick={this.props.onFavoriteClick}
                    onCloseHomeTileLarge={this.handleCloseHomeTileLarge}
                    canVisit={this.props.canVisit}
                    canFavorite={this.props.canFavorite}
                    displayPercent={this.displayPercent}
                    displayOnMarket={true}
                    onMarket={home.on_market}
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

// Set the types and whether any props are required
HomeTiles.propTypes = {
    homes: PropTypes.array.isRequired,
    visit_list: PropTypes.array.isRequired,
    favorites: PropTypes.array.isRequired,
    onVisitClick: PropTypes.func.isRequired,
    onFavoriteClick: PropTypes.func,
    canVisit: PropTypes.bool,
    canFavorite: PropTypes.bool,
    displayPercent: PropTypes.bool,
};

// Set the default props if they aren't passed
HomeTiles.defaultProps = {
        canFavorite: true,
        canVisit: false,
        displayPercent: false
};

