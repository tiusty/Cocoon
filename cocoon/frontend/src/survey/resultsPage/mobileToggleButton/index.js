import React, { Component } from 'react';
import { createPortal } from 'react-dom';
import './mobileToggleButton.css';

export default class MobileToggleButton extends Component {

    componentDidMount() {
        document.querySelector('body').style.position = 'relative';
    }

    componentWillUnmount() {
        document.querySelector('body').style.position = 'static';
    }

    handleActiveStyle = (target) => {
        let style = {
            color: 'var(--darkBlue)'
        }
        if (target === 'list' && this.props.viewingMobileResults) {
            style = {
                color: 'var(--red)'
            }
        }
        if (target === 'map' && this.props.viewingMobileMap) {
            style = {
                color: 'var(--red)'
            }
        }
        return style;
    }

    render() {
        if (this.props.isMobile && !this.props.isEditing && !this.props.isViewingPopup) {
            return (
                createPortal(
                    <div className="mobile-toggle-wrapper">
                        <div onClick={() => this.props.handleMobileButtonClick('list')} className="toggle-btn" style={this.handleActiveStyle('list')}>
                            <i className="material-icons">
                                format_list_bulleted
                            </i> List
                        </div>

                        <div onClick={() => this.props.handleMobileButtonClick('map')} className="toggle-btn" style={this.handleActiveStyle('map')}>
                            <i className="material-icons">
                                place
                            </i> Map
                        </div>
                    </div>,
                    document.querySelector('body')
                )

            );
        } else {
            return null;
        }
    }
}