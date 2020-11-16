import React from "react";
import MainPage from "./components/MainPage";
import ConfigPage from "./components/ConfigPage";
import {
    BrowserRouter as Router,
    Route,
    Switch
} from "react-router-dom";

class App extends React.Component {
    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/"><MainPage/></Route>
                    <Route path="/config/:beaconID" component={ConfigPage}></Route>
                </Switch>
            </Router>
        )
    }
}

export default App