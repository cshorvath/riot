import {BrowserRouter, Route, Switch} from "react-router-dom";
import React from "react";
import Container from "react-bootstrap/Container";
import Header from "./Header";
import Devices from "./Devices";
import Login from "./Login";
import {Redirect} from "react-router";
import {connect} from "react-redux";



const App = function ({loggedIn}) {

    function authReq(Component) {
        return loggedIn ? Component : Login;
    }

    return <BrowserRouter>
        <Header/>
        <Container className="mt-3">
            <Switch>
                <Route exact path="/"><Redirect to="/device"/></Route>
                <Route path="/device" component={authReq(Devices)}/>
            </Switch>
        </Container>
    </BrowserRouter>
};

function mapStateToProps(state) {
    return {loggedIn: state.login.user};
}

export default connect(mapStateToProps)(App);
