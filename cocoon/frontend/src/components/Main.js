import React from 'react'
import { Switch, Route } from 'react-router-dom'
import { Component } from 'react';
import { BrowserRouter } from 'react-router-dom'

class Home extends Component {
    render(){
        return (<h1>Home Page</h1>);
    }
}

// More components
// class Car extends Component {
//     render(){
//         return (<h1>Cars page</h1>);
//     }
// }

const Car = () => (
  <div>
    <h1>Welcome to the Tornadoes Website!</h1>
  </div>
)

class About extends Component {
    render(){
        return (<h1>About page</h1>);
    }
}



// The Main component renders one of the three provided
// Routes (provided that one matches). Both the /roster
// and /schedule routes will match any pathname that starts
// with /roster or /schedule. The / route will only match
// when the pathname is exactly the string "/"
const Main = () => (
  <main>
      <BrowserRouter>
          <Switch>
      <Route exact path='/react/' component={Home}/>
      <Route path='/react/signatures' component={Car}/>
      <Route path='/react/about' component={About}/>
          </Switch>
      </BrowserRouter>
  </main>
)

export default Main
