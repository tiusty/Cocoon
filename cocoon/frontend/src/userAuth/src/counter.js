import React, { Component } from 'react';

class Counter extends Component {
    state = {
        value: this.props.counter.value,
    };

    renderTags() {
        if (this.state.tags.length === 0) return <p>There are no tags!</p>;

        return <ul>{ this.state.tags.map(tag => <li key={tag}>{ tag }</li>)}</ul>;

    }

    // Binds this for counter to handleIncrement function
    handleIncrement = product => {
        console.log(product);
        this.setState({ value: this.state.value + 1 });
    };

    render() {
        console.log('props', this.props);
        return  (
            <div>
                <h4>Counter #{this.props.counter.id}</h4>
                <span className={this.getBadgeClasses()}>{this.formatCount()}</span>
                <button
                    onClick={ () => this.handleIncrement() }
                    className="btn btn-secondary btn-sm">
                    Increment</button>
                <button onClick={() => this.props.onDelete(this.props.counter.id)} className="btn btn-danger btn-sm m-2">Delete</button>
            </div>
        );
    }

    getBadgeClasses() {
        let classes = "badge m-2 badge-";
        classes += (this.state.value === 0) ? "warning" : "primary";
        return classes;
    }

    formatCount() {
        const {value} = this.state;
        return value === 0 ? 'Zero' : value;
    }
}

export default Counter;