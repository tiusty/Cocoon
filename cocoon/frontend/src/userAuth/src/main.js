import React from 'react'
import { Switch, Route } from 'react-router-dom'
import { BrowserRouter } from 'react-router-dom'
import RoommateGroup from "./groups";




const Main = () => (
    <main>
        <BrowserRouter>
            <Switch>
                <Route path='/userAuth/groups' component={RoommateGroup}/>
            </Switch>
        </BrowserRouter>
    </main>
);

export default Main