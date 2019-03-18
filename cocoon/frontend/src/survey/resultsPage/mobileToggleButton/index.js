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

    render() {
        if (this.props.isMobile && !this.props.isEditing && !this.props.viewing_home && !this.props.isViewingPopup) {
            return (
                createPortal(
                    <div className="mobile-toggle-wrapper">
                        <div className="toggle-btn">
                            <i className="material-icons">
                                format_list_bulleted
                            </i> List
                        </div>

                        <div className="toggle-btn">
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