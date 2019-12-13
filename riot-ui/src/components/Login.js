import {connect} from "react-redux";
import React, {useEffect} from "react";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import {getUserWithStoredToken, loginRequest} from "../actions/login";
import {ErrorAlert, InProgressSpinner} from "./util/util";

function handleSubmit(event, loginRequest) {
    event.preventDefault();
    const data = new FormData(event.target);
    loginRequest(data.get("user"), data.get("password"));
}


function Login({inProgress, error, loginRequest, getUserWithStoredToken}) {
    useEffect(getUserWithStoredToken, []);
    return <Col md={8} className="mx-auto">
        <Card className="login-card mx-auto">
            <Card.Header>Bejelentkezés</Card.Header>
            <Card.Body>
                {error && <ErrorAlert error={error.detail}/>}
                <Form onSubmit={event => handleSubmit(event, loginRequest)}>
                    <Form.Group as={Row} controlId="formPlaintextEmail">
                        <Form.Label column md="3">
                            Felhasználónév
                        </Form.Label>
                        <Col md="9">
                            <Form.Control name="user" type="text" required="required"/>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId="formPlaintextPassword">
                        <Form.Label column md="3">
                            Jelszó
                        </Form.Label>
                        <Col md="9">
                            <Form.Control name="password" type="password" required="required"/>
                        </Col>
                    </Form.Group>
                    <Form.Group as={Row} className="justify-content-md-center">
                        <Button variant="primary" type="submit">
                            {inProgress ? <InProgressSpinner show={inProgress}/> : "Bejelentkezés"}
                        </Button>
                    </Form.Group>
                </Form>
            </Card.Body>
        </Card>
    </Col>
}

function mapStateToProps(state) {
    return {inProgress: state.login.inProgress, error: state.login.error, user: state.login.user}
}

export default connect(mapStateToProps, {loginRequest, getUserWithStoredToken})(Login)