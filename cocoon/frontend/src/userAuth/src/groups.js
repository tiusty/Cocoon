import React from 'react'
import { Component } from 'react';


import Counters from "./counters";

class RoommateGroup extends Component {
    state = {
        counters: [
            { id: 1, value: 4 },
            { id: 2, value: 0 },
            { id: 3, value: 0 },
            { id: 4, value: 0 },
        ]
    };

    constructor(props) {
        super(props);
        console.log('App - Constructor', this.props)
    }

    componentDidMount() {
        // Ajax call
        console.log('App - Mounted')
    }

    handleIncrement = counter => {
        // Clone counters (using spread function)
        const counters = [...this.state.counters];
        const index = counters.indexOf(counter);
        counters[index] = {...counter};
        counters[index].value++;
        this.setState({counters});
    };

    handleDelete = (counterId) => {
        const counters = this.state.counters.filter(c => c.id !== counterId);
        this.setState({ counters });
    };

    handleReset = () => {
      const counters = this.state.counters.map(c => {
          c.value = 0;
          return c;
      });

        this.setState({counters})
    };

    render() {
        console.log('App - Rendered')
        return (

            <React.Fragment>
                <h1>{this.state.counters.filter(c => c.value > 0).length}</h1>
                <Counters
                    onReset={this.handleReset}
                    onIncrement={this.handleIncrement}
                    onDelete={this.handleDelete}
                    counters={this.state.counters}
                />
            </React.Fragment>
        );
    }
}
export default RoommateGroup

