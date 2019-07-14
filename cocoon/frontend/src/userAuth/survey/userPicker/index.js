import React, { Component } from 'react';

export default class UserPicker extends Component {

    render() {
        return (
            <div className="tour-box tour-picker">
                <div className="tour-top-bar">
                    <h3>My Clients</h3>
                </div>
                <div className="tour-picker-surveys">
                    {this.props.clients && this.props.clients.map(client => {
                        let clientClass = 'survey-item';
                        if (this.props.client_id === client.id) {
                            clientClass += ' survey-active';
                        }
                        return (
                            <div key={client.id} className={clientClass} onClick={() => this.props.handleClickClient(client.id)}>
                                {client.email}
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }
}