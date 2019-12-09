import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import {InProgressSpinner} from "./util";
import {connect} from "react-redux";
import {addDevice, updateDevice} from "../actions/devices";


function DeviceEditModal({show, device, inProgress, addDevice, updateDevice}) {

    const name = device ? device.name : null;
    const description = device ? device.description : null;

    const onSubmit = device ?
        deviceData => updateDevice(device.id, deviceData)
        : deviceData => addDevice(deviceData);

    const title = device ? "Eszköz szerkesztése" : "Eszköz hozzáadása";

    function handleSubmit(event) {
        event.preventDefault();
        const data = new FormData(event.target);
        const device = {name: data.get("name"), description: data.get("description")};
        onSubmit(device)
    }

    return <Modal
        show={show}
        onHide={() => {
        }}
        size="lg"
        centered>
        <Modal.Header closeButton>
            <Modal.Title id="contained-modal-title-vcenter">
                {title}
            </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
            <Modal.Body>
                <Form.Group as={Row} controlId="name">
                    <Form.Label column md="3">
                        Név
                    </Form.Label>
                    <Col md="9">
                        <Form.Control name="name" type="text" value={name}/>
                    </Col>
                </Form.Group>

                <Form.Group as={Row} controlId="description">
                    <Form.Label column md="3">
                        Megjegyzés
                    </Form.Label>
                    <Col md="9">
                        <Form.Control name="description" type="text" value={description}/>
                    </Col>
                </Form.Group>
            </Modal.Body>
            <Modal.Footer>
                <Button type="submit">{inProgress ? <InProgressSpinner show={inProgress}/> : "Mentés"}</Button>
            </Modal.Footer>
        </Form>
    </Modal>
}

export default connect(state => state.devices.modal, {addDevice, updateDevice})(DeviceEditModal)