import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import {InProgressSpinner} from "./util/util";
import {connect} from "react-redux";
import {addDevice, hideDeviceModal, updateDevice} from "../actions/devices";

function handleSubmit(event, onSubmit) {
    event.preventDefault();
    const data = new FormData(event.target);
    const device = {name: data.get("name"), description: data.get("description")};
    if (device.name.trim())
        onSubmit(device)
}

function DeviceEditModal({show, device, inProgress, addDevice, updateDevice, hideDeviceModal}) {

    const name = device ? device.name : null;
    const description = device ? device.description : null;

    const onSubmit = device ?
        deviceData => updateDevice(device.id, deviceData)
        : deviceData => addDevice(deviceData);

    const title = device ? "Eszköz szerkesztése" : "Eszköz hozzáadása";

    return <Modal
        show={show}
        onHide={hideDeviceModal}
        size="lg"
        centered>
        <Modal.Header closeButton>
            <Modal.Title id="contained-modal-title-vcenter">
                {title}
            </Modal.Title>
        </Modal.Header>
        <Form onSubmit={e => handleSubmit(e, onSubmit)}>
            <Modal.Body>
                <Form.Group as={Row} controlId="name">
                    <Form.Label column md="3">
                        Név
                    </Form.Label>
                    <Col md="9">
                        <Form.Control name="name" type="text" defaultValue={name} required="required" minLength={3}/>
                    </Col>
                </Form.Group>

                <Form.Group as={Row} controlId="description">
                    <Form.Label column md="3">
                        Megjegyzés
                    </Form.Label>
                    <Col md="9">
                        <Form.Control name="description" type="text" defaultValue={description} required="required"/>
                    </Col>
                </Form.Group>
            </Modal.Body>
            <Modal.Footer>
                <Button type="submit">{inProgress ? <InProgressSpinner show={inProgress}/> : "Mentés"}</Button>
            </Modal.Footer>
        </Form>
    </Modal>
}

export default connect(state => state.devices.modal, {addDevice, updateDevice, hideDeviceModal})(DeviceEditModal)