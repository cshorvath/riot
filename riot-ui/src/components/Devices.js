import React, {useEffect} from "react";
import Table from "react-bootstrap/Table";
import {addDevice, deleteDevice, getDevices, showAddDeviceModal} from "../actions/devices";
import {ErrorAlert, InProgressSpinner} from "./util";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import {connect} from "react-redux";
import DeviceEditModal from "./DeviceEditModal";

function DeviceRow({device, deleteDevice}) {
    return <tr>
        <td>{device.id}</td>
        <td>{device.name}</td>
        <td>{device.description}</td>
        <td>{device.last_message || "N/A"}</td>
        <td>
            <ButtonGroup>
                <Button variant="outline-primary">Üzenetek</Button>
                <Button variant="outline-info">Szabályok</Button>
                <Button variant="outline-secondary">Szerkesztés</Button>
                <Button variant="outline-danger" onClick={() => deleteDevice(device)}>Törlés</Button>
            </ButtonGroup>
        </td>
    </tr>
}

const ConnectedDeviceRow = connect(null, {deleteDevice})(DeviceRow);

function DevicesList({devices, error, isLoading}) {
    if (isLoading || !devices)
        return <InProgressSpinner/>;
    if (error)
        return <ErrorAlert error={error.message}/>;
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
        {devices.map(device => <ConnectedDeviceRow device={device}/>)}
        </tbody>
    </Table>
}

const ConnectedDevicesList = connect(state => ({...state.devices}))(DevicesList);

function Devices({getDevices, showAddDeviceModal}) {
    useEffect(getDevices, []);
    return <>
        <DeviceEditModal />
        <h1>Eszközök</h1>
        <div className="d-flex">
            <ButtonGroup className="mb-3 ml-auto">
                <Button variant="success" onClick={showAddDeviceModal}>Hozzáadás</Button>
                <Button variant="primary" onClick={getDevices}>Frissítés</Button>
            </ButtonGroup>
        </div>
        <ConnectedDevicesList/>
    </>
}

export default connect(null, {getDevices, showAddDeviceModal, addDevice})(Devices)