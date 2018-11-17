import React from 'react'
import { Switch, Route } from 'react-router-dom'
import { BrowserRouter } from 'react-router-dom'
import Surveys from "./groups";




const Main = () => (
    <main>
        <BrowserRouter>
            <Switch>
                <Route path='/userAuth/surveys' component={Surveys}/>
            </Switch>
        </BrowserRouter>
    </main>
);

export default Main