import React from 'react'
import { Switch, Route } from 'react-router-dom'
import { Component } from 'react';
import { BrowserRouter } from 'react-router-dom'

// Import sub components
import Signatures from './signatures/Main'
import Survey from './survey/Main'
import UserAuth from './userAuth/Main'
import HomePage from './homePage/Main'

class Home extends Component {
    render(){
        return (<h1>Home Page</h1>);
    }
}

const Main = () => (
    <main>
        <BrowserRouter>
            <Switch>
                <Route exact path='/react/' component={Home}/>
                <Route path='/react/signatures' component={Signatures}/>
                <Route path='/react/survey' component={Survey}/>
                <Route path='/react/userAuth' component={UserAuth}/>
                <Route path='/react/homePage' component={HomePage}/>
            </Switch>
        </BrowserRouter>
    </main>
);

export default Main
