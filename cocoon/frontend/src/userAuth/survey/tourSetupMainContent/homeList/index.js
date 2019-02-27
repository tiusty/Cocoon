import React, {Component} from 'react';

import HomeTile from '../../../../common/homeTile/homeTile';

export default class HomeList extends Component {

    handleSmallTileButtons = (id, list) => {
        return list.filter(home => home.id === id).length > 0;
    }

    render() {
        return (
            <div className="content-homelist content-homelist_tiles">
                {this.props.activeSurvey.favorites && this.props.activeSurvey.favorites.map(home => {
                    return <HomeTile
                        key={home.id}
                        home={home}
                        canFavorite={!this.handleSmallTileButtons(home.id, this.props.visit_list)}
                        canVisit={this.handleSmallTileButtons(home.id, this.props.favorites)}
                        visit={this.props.visit_list.filter(v => v.id === home.id).length > 0}
                        favorite={this.props.favorites.filter(f => f.id === home.id).length > 0}
                        onMarket={home.on_market}
                        addBorder={this.props.visit_list.filter(v => v.id === home.id).length > 0}
                        onFavoriteClick={() => this.props.handleFavoriteClick(home)}
                        onVisitClick={(e) => this.props.handleVisitClick(home, e)}
                        onHomeClick={() => this.props.handleHomeClick(home.id)}
                    />
                })}
            </div>
        );
    }
}