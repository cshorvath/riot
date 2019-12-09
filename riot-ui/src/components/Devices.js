import {connect} from "react-redux";
import React from "react";
import * as PropTypes from "prop-types";
import Table from "react-bootstrap/Table";
import {getDevices} from "../actions/devices";
import {ErrorAlert, InProgressSpinner} from "./util";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";

class DevicesList extends React.Component {
    componentDidMount() {
        this.props.getDevices();
    }

    render() {
        const {devices, error, isLoading} = this.props;
        window.devices = devices;
        if (isLoading || !devices)
            return <InProgressSpinner/>;
        if (error)
            return <ErrorAlert error={error}/>;
        return <Table striped>
            <colgroup>
                <col className="col-md-1"/>
                <col className="col-md-2"/>
                <col className="col-md-3"/>
                <col className="col-md-2"/>
                <col className="col-md-4"/>
            </colgroup>
            <thead>
            <th>Id</th>
            <th>Név</th>
            <th>Megjegyzés</th>
            <th>Utolsó üzenet</th>
            <th>Műveletek</th>
            </thead>
            <tbody>
            {devices.map(this.getRow)}
            </tbody>
        </Table>
    }

    getRow(device) {
        return <tr>
            <td>{device.id}</td>
            <td>{device.name}</td>
            <td>{device.description}</td>
            <td>{device.last_message || "N/A"}</td>
            <td>
                <ButtonGroup className="mr-auto">
                    <Button variant="outline-primary">Üzenetek</Button>
                    <Button variant="outline-info">Szabályok</Button>
                    <Button variant="outline-secondary">Szerkesztés</Button>
                    <Button variant="outline-danger">Törlés</Button>
                </ButtonGroup>
            </td>
        </tr>
    }
}

DevicesList.propTypes = {
    devices: PropTypes.arrayOf(PropTypes.object),
    error: PropTypes.string,
    isLoading: PropTypes.bool,
    getDevices: PropTypes.func
};

const ConnectedDevicesLis = connect(mapStateToProps, {getDevices})(DevicesList);

function mapStateToProps(state) {
    return {...state.devices};
}

function Devices({getDevices}) {
    return <>
        <h1>Eszközök</h1>
        <div className="d-flex">
            <ButtonGroup className="mb-3 ml-auto">
                <Button variant="success">Hozzáadás</Button>
                <Button variant="primary" onClick={getDevices}>Frissítés</Button>
            </ButtonGroup>
        </div>

        <ConnectedDevicesLis/>
    </>
}

export default connect(null, {getDevices})(Devices)