import React, {useEffect} from "react";
import Table from "react-bootstrap/Table";
import {addDevice, deleteDevice, getDevices, showAddDeviceModal, showEditDeviceModal} from "../actions/devices";
import {ErrorAlert, InProgressSpinner} from "./util";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import {connect} from "react-redux";
import DeviceEditModal from "./DeviceEditModal";
import {Link} from "react-router-dom";

function DeviceRow({device, deleteDevice, showEditDeviceModal}) {

    function confirmDelete() {
        if (window.confirm(`Biztosan törölni akarod a következő eszközt: ${device.name}? `))
            deleteDevice(device.id)
    }


    return <tr>
        <td>{device.id}</td>
        <td>{device.name}</td>
        <td>{device.description}</td>
        <td>{device.last_message || "N/A"}</td>
        <td>
            <ButtonGroup>
                <Link to={`/device/${device.id}/message`}><Button size="sm" variant="outline-primary">Üzenetek</Button></Link>
                <Button size="sm" variant="outline-info">Szabályok ({device.rule_count})</Button>
                <Button size="sm" variant="outline-secondary"
                        onClick={() => showEditDeviceModal(device)}>Szerkesztés</Button>
                <Button size="sm" variant="outline-danger" onClick={confirmDelete}>Törlés</Button>
            </ButtonGroup>
        </td>
    </tr>
}

const ConnectedDeviceRow = connect(null, {deleteDevice, showEditDeviceModal})(DeviceRow);

function DevicesList({devices, error, isLoading}) {
    if (isLoading || !devices)
        return <InProgressSpinner/>;
    return <>
        {error && <ErrorAlert error={error.message}/>}
        <Table hover bordered className="data-table">
            <colgroup>
                <col style={{"width": "5%"}}/>
                <col style={{"width": "10%"}}/>
                <col style={{"width": "30%"}}/>
                <col style={{"width": "15%"}}/>
                <col style={{"width": "30%"}}/>
            </colgroup>
            <thead>
            <tr>
                <th>Id</th>
                <th>Név</th>
                <th>Megjegyzés</th>
                <th>Utolsó üzenet</th>
                <th>Műveletek</th>
            </tr>
            </thead>
            <tbody>
            {devices.map(device => <ConnectedDeviceRow device={device} key={"device" + device.id}/>)}
            </tbody>
        </Table>
    </>
}

const ConnectedDevicesList = connect(state => ({...state.devices}))(DevicesList);

function Devices({getDevices, showAddDeviceModal}) {
    useEffect(getDevices, []);
    return <>
        <DeviceEditModal/>
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