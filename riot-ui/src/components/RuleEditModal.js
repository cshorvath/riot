import {connect} from "react-redux";
import {addRule, hideRuleModal, updateRule} from "../actions/rules";
import React, {useEffect, useState} from "react";
import {OPERATOR, RULE_ACTIONS} from "../constant";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import {ErrorAlert, formatDeviceTitle} from "./util/util";
import {getDevices} from "../actions/devices";

function handleSubmit(event, onSubmit) {
    event.preventDefault();
    const data = new FormData(event.target);
    const submittedRule = {
        name: data.get("name"),
        message_field: data.get("message_field"),
        action_type: data.get("action_type"),
        action_arg: data.get("action_arg"),
        operator: data.get("operator"),
        operator_arg_1: data.get("operator_arg_1"),
        operator_arg_2: data.get("operator_arg_2"),
        target_device_id: data.get("target_device_id")
    };
    console.log(submittedRule);
    onSubmit(submittedRule)
}

function operatorArgInputs(operator, editedRule) {
    const inputs = [];
    for (let i = 1; i <= operator.argCount; ++i) {
        const inputName = "operator_arg_" + i;
        inputs.push(
            <Form.Group as={Row} controlId={inputName} key={inputName}>
                <Form.Label column md="3">
                    Operátor argumentum {i}
                </Form.Label>
                <Col md="9">
                    <Form.Control name={inputName} defaultValue={editedRule[inputName]} type="number"
                                  required="required"/>
                </Col>
            </Form.Group>
        )
    }
    return inputs;

}

function actionArgInputs(actionType, editedRule, devices) {
    if (actionType === RULE_ACTIONS.SEND_EMAIL)
        return <Form.Group as={Row} controlId="action_arg">
            <Form.Label column md="3">
                E-mail cím
            </Form.Label>
            <Col md="9">
                <Form.Control name="action_arg" type="email" defaultValue={editedRule.action_arg} required="required"/>
            </Col>
        </Form.Group>;
    if (actionType === RULE_ACTIONS.FORWARD)
        return <>
            <Form.Group as={Row} controlId="action_arg">
                <Form.Label column md="3">
                    Üzenet formátum
                </Form.Label>
                <Col md="9">
                    <Form.Control name="action_arg" type="text" defaultValue={editedRule.action_arg}
                                  required="required"/>
                </Col>
            </Form.Group>
            <Form.Group as={Row} controlId="targetDevice">
                <Form.Label column md="3">
                    Céleszköz
                </Form.Label>
                <Col md="9">
                    <Form.Control as="select" name="target_device_id">
                        {
                            devices.map(
                                device => <option key={"target_device_" + device.id}
                                                  value={device.id}>{formatDeviceTitle(device)}</option>
                            )
                        };
                    </Form.Control>
                </Col>
            </Form.Group>
        </>
}


function RuleEditModal({deviceId, show, rule, devices, error, addRule, updateRule, hideRuleModal, getDevices}) {
    useEffect(getDevices, []);
    const [actionType, setActionType] = useState(RULE_ACTIONS.SEND_EMAIL);
    const editedRule = rule || {};
    const [operator, setOperator] = useState(editedRule.operator ? OPERATOR[editedRule.operator] : OPERATOR["LT"]);
    const onSubmit = rule ?
        data => updateRule(deviceId, rule.id, data)
        : data => addRule(deviceId, data);
    const title = rule ? "Szabály szerkesztése" : "Szabály hozzáadása";
    const errorComponent = error && <ErrorAlert error={error.message}/>
    return <Modal
        show={show}
        onHide={hideRuleModal}
        size="xl"
        centered>
        <Modal.Header closeButton>
            <Modal.Title id="contained-modal-title-vcenter">
                {title}
            </Modal.Title>
        </Modal.Header>
        {errorComponent}
        <Form onSubmit={e => handleSubmit(e, onSubmit)}>
            <Modal.Body>
                <Form.Group as={Row} controlId="name">
                    <Form.Label column md="3">
                        Név
                    </Form.Label>
                    <Col md="9">
                        <Form.Control name="name" type="text" defaultValue={editedRule.name} required="required"
                                      minLength={3}/>
                    </Col>
                </Form.Group>

                <Form.Group as={Row} controlId="messageField">
                    <Form.Label column md="3">
                        Üzenet mező
                    </Form.Label>
                    <Col md="9">
                        <Form.Control name="message_field" type="text" defaultValue={editedRule.message_field}
                                      required="required"/>
                    </Col>
                </Form.Group>
                <Form.Group as={Row} controlId="operator">
                    <Form.Label column md="3">
                        Operátor
                    </Form.Label>
                    <Col md="9">
                        <Form.Control as="select" name="operator" defaultValue={editedRule.operator}
                                      onChange={(e) => setOperator(OPERATOR[e.target.value])}>
                            {
                                Object.values(OPERATOR).map(
                                    op => <option key={op.id} value={op.id}>{op.displayName}</option>
                                )
                            };
                        </Form.Control>
                    </Col>
                </Form.Group>
                {operatorArgInputs(operator, editedRule)}
                <Form.Group as={Row} controlId="action_type">
                    <Form.Label column md="3">
                        Operátor
                    </Form.Label>
                    <Col md="9">
                        <Form.Control as="select" name="action_type" defaultValue={editedRule.action_type}
                                      onChange={(e) => setActionType(e.target.value)}>
                            <option value={RULE_ACTIONS.SEND_EMAIL}>E-mail küldése</option>
                            <option value={RULE_ACTIONS.FORWARD}>Üzenet továbbítása</option>
                        </Form.Control>
                    </Col>
                </Form.Group>
                {actionArgInputs(actionType, editedRule, devices)}
            </Modal.Body>
            <Modal.Footer>
                <Button type="submit">Mentés</Button>
            </Modal.Footer>
        </Form>
    </Modal>

}


export default connect(
    state => ({
        devices: state.devices.devices,
        show: state.rules.modal.show,
        rule: state.rules.modal.rule
    }), {addRule, updateRule, getDevices, hideRuleModal})(RuleEditModal);