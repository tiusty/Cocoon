// Import React Components
import React from 'react'
import {Component} from 'react';

export default class HomeTileLarge extends Component {

    render() {
        let home = this.props.home;
        return (
            <>
                <div className="expanded-tile-container">
                    <div className="expanded-row-top">
                        <span onClick={() => this.props.onCloseHomeTileLarge()}
                              className="expanded-close glyphicon glyphicon-resize-small"/>
                    </div>
                    <div className="expanded-info">
                        <table className="expanded-info-table table-striped">
                            <tbody>
                            <tr>
                                <td className="expanded-tile-text category">Price</td>
                                <td className="expanded-tile-text value">{home.price}</td>
                            </tr>
                            <tr>
                                <td className="expanded-tile-text category">Beds</td>
                                <td className="expanded-tile-text value">{home.num_bedrooms}</td>
                            </tr>
                            <tr>
                                <td className="expanded-tile-text category">Baths</td>
                                <td className="expanded-tile-text value">{home.num_bathrooms}</td>
                            </tr>
                            <tr>
                                <td className="expanded-tile-text category">Home type</td>
                                <td className="expanded-tile-text value">{home.home_type}</td>
                            </tr>
                            <tr>
                                <td className="expanded-tile-text category">Remarks</td>
                                <td className="expanded-tile-text value remarks">{home.remarks}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </>
        );
    }
}
