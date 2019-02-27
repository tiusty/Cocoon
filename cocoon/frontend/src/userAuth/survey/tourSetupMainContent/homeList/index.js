import React, {Component} from 'react';

import HomeTile from '../../../../common/homeTile/homeTile';
import HomeTileLarge from '../../../../common/homeTile/homeTileLarge';

export default class HomeList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            boxHeight: 0,
        }
    }

    componentDidMount() {
        if (document.querySelector('.tile')) {
            const boxHeight = document.querySelector('.tile').clientHeight;
            this.setState({ boxHeight });
        }
    }

    handleSmallTileButtons = (id, list) => {
        return list.filter(home => home.id === id).length > 0;
    }

    handleHomeView = () => {
        if (!this.props.viewing_home) {
            return (
                <div className="content-homelist_tiles">
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
                    <div className="tour-box add-more-homes-box" style={{height: this.state.boxHeight}}>
                        <h2>Want to <span>favorite</span> more homes?</h2>
                        <a href={this.props.activeResultsUrl}>Go To Results</a>
                    </div>
                </div>
            );
        } else {
            let home = this.props.activeSurvey.favorites.find(home => home.id === this.props.clicked_home);
            return (
                <HomeTileLarge
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
                    onCloseHomeTileLarge={this.props.handleCloseHomeTileLarge}
                />
            );
        }
    }

    render() {
        return this.handleHomeView();
    }
}