import {withRouter} from "react-router";
import {connect} from "react-redux";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Button from "react-bootstrap/Button";
import React, {useEffect} from "react";
import {deleteRule, getRules, showAddRuleModal, showEditRuleModal} from "../actions/rules";
import {conditionFormatter, ErrorAlert, formatDeviceTitle, InProgressSpinner} from "./util";
import Table from "react-bootstrap/Table";

function RuleRow({deviceId, rule, deleteRule, showEditRuleModal}) {

    function confirmDelete() {
        if (window.confirm(`Biztosan törölni akarod a következő szabályt: ${rule.name}? `))
            deleteRule(deviceId, rule.id)
    }

    return <tr>
        <td>{rule.id}</td>
        <td>{rule.name}</td>
        <td>{rule.creator.name}</td>
        <td>{conditionFormatter(rule.operator, rule.message_field, rule.operator_arg_1, rule.operator_arg_2)}</td>
        <td>{conditionFormatter(rule.operator, rule.message_field, rule.operator_arg_1, rule.operator_arg_2)}</td>
        <td>
            <ButtonGroup>
                <Button size="sm" variant="outline-secondary"
                        onClick={() => showEditRuleModal(rule)}>Szerkesztés</Button>
                <Button size="sm" variant="outline-danger" onClick={confirmDelete}>Törlés</Button>
            </ButtonGroup>
        </td>
    </tr>
}

const ConnectedRuleRow = connect(null, {deleteRule, showEditRuleModal})(RuleRow);

function RulesList({deviceId, rules, error, isLoading}) {
    if (isLoading)
        return <InProgressSpinner/>;
    if (!rules.length)
        return <>
            {error && <ErrorAlert error={error.message}/>}
            <div className="d-flex">
                <h2 className="text-secondary mx-auto">Nincsenek hozzáadott szabályok</h2>
            </div>
        </>;
    return <>
        {error && <ErrorAlert error={error.message}/>}
        <Table hover bordered className="data-table">
            <thead>
            <tr>
                <th>Id</th>
                <th>Név</th>
                <th>Létrehozó</th>
                <th>Feltétel</th>
                <th>Akció</th>
                <th>Műveletek</th>
            </tr>
            </thead>
            <tbody>
            {rules.map(rule => <ConnectedRuleRow deviceId={deviceId} rule={rule} key={"rule_" + rule.id}/>)}
            </tbody>
        </Table>
    </>
}

const ConnectedRulesList = connect(state =>
    ({
        rules: state.rules.rules,
        error: state.rules.error,
        isLoading: state.rules.isLoading
    }))(RulesList);

function Rules({match, device, getRules, showAddRuleModal}) {
    const deviceId = match.params.deviceId;
    useEffect(() => getRules(deviceId), [deviceId, getRules]);
    return <>
        {/*<DeviceEditModal/>*/}
        <h1>Szabályok - {formatDeviceTitle(device)}</h1>
        <div className="d-flex">
            <ButtonGroup className="mb-3 ml-auto">
                <Button variant="success" onClick={showAddRuleModal}>Hozzáadás</Button>
                <Button variant="primary" onClick={() => getRules(deviceId)}>Frissítés</Button>
            </ButtonGroup>
        </div>
        <ConnectedRulesList deviceId={device.id}/>
    </>
}

export default withRouter(
    connect(state => ({device: state.rules.device || {}}), {getRules, showAddRuleModal})(Rules));