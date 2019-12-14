import React from "react";
import Navbar from "react-bootstrap/Navbar";
import {Link} from "react-router-dom";
import Nav from "react-bootstrap/Nav";
import Dropdown from "react-bootstrap/Dropdown";
import NavItem from "react-bootstrap/NavItem";
import {connect} from "react-redux";
import {logout} from "../actions/login";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faSignOutAlt} from "@fortawesome/free-solid-svg-icons/faSignOutAlt";
import {faUser} from "@fortawesome/free-solid-svg-icons/faUser";


function UserMenu({user, logout}) {
    if (!user) return null;
    return <Dropdown alignRight as={NavItem}>
        <Dropdown.Toggle as={Nav.Link}><FontAwesomeIcon icon={faUser}/> {user.name} {user.admin ? "(admin)" : ""}</Dropdown.Toggle>
        <Dropdown.Menu>
            <Dropdown.Item onClick={logout}><FontAwesomeIcon icon={faSignOutAlt}/> Kijelentkezés</Dropdown.Item>
        </Dropdown.Menu>
    </Dropdown>;
}

const ConnectedUserMenu = connect(
    (state) => ({user: state.login.user}), {logout})(UserMenu);

const Header = ({user}) =>
    <Navbar bg="dark" variant="dark">
        <Navbar.Brand>
            <Link to="/" className="navbar-brand">rIOT Data Platform</Link>
        </Navbar.Brand>
        <Nav className="ml-auto">
            <ConnectedUserMenu/>
        </Nav>
    </Navbar>;

export default Header;