import {BrowserRouter, Route, Switch} from "react-router-dom";
import React from "react";
import Container from "react-bootstrap/Container";
import Header from "./Header";
import Devices from "./Devices";
import Login from "./Login";
import {Redirect} from "react-router";
import {connect} from "react-redux";
import Messages from "./Messages";



const App = function ({loggedIn}) {

    function authReq(Component) {
        return loggedIn ? Component : Login;
    }

    return <BrowserRouter>
        <Header/>
        <Container className="mt-3" fluid>
            <Switch>
                <Route exact path="/"><Redirect to="/device"/></Route>
                <Route exact path="/device" component={authReq(Devices)}/>
                <Route exact path="/device/:deviceId/message" component={authReq(Messages)}/>
            </Switch>
        </Container>
    </BrowserRouter>
};

function mapStateToProps(state) {
    return {loggedIn: state.login.user};
}

export default connect(mapStateToProps)(App);
