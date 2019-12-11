import React, {useEffect} from "react";
import Table from "react-bootstrap/Table";
import {deleteDevice, getDevices, showAddDeviceModal, showEditDeviceModal} from "../actions/devices";
import {ErrorAlert, InProgressSpinner} from "./util";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import {connect} from "react-redux";
import DeviceEditModal from "./DeviceEditModal";
import {LinkContainer} from 'react-router-bootstrap'
import {AddButton, DeleteButton, EditButton, MessagesButton, RefreshButton, RulesButton} from "./buttons";
import {faBroadcastTower} from "@fortawesome/free-solid-svg-icons/faBroadcastTower";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

function DeviceRow({device, deleteDevice, showEditDeviceModal}) {

    function confirmDelete() {
        if (window.confirm(`Biztosan törölni akarod a következő eszközt: ${device.name}? `))
            deleteDevice(device.id)
    }


    return <tr>
        <td>{device.id}</td>
        <td>{device.name}</td>
        <td>{device.description}</td>
        <td>
            <ButtonGroup>
                <LinkContainer to={`/device/${device.id}/message`}><MessagesButton/></LinkContainer>
                <LinkContainer to={`/device/${device.id}/rule`}><RulesButton count={device.rule_count}/></LinkContainer>
                <EditButton onClick={() => showEditDeviceModal(device)}/>
                <DeleteButton onClick={confirmDelete}/>
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
        <Table size={"sm"} hover bordered className="data-table">
            <colgroup>
                <col style={{"width": "5%"}}/>
                <col style={{"width": "20%"}}/>
                <col/>
                <col style={{"width": "20%"}}/>
            </colgroup>
            <thead>
            <tr>
                <th>Id</th>
                <th>Név</th>
                <th>Megjegyzés</th>
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
        <h1><FontAwesomeIcon icon={faBroadcastTower}/> Eszközök</h1>
        <div className="d-flex">
            <ButtonGroup className="mb-3 ml-auto">
                <AddButton onClick={showAddDeviceModal}/>
                <RefreshButton onClick={getDevices}/>
            </ButtonGroup>
        </div>
        <ConnectedDevicesList/>
    </>
}

export default connect(null, {getDevices, showAddDeviceModal})(Devices)