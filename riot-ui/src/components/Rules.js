import {withRouter} from "react-router";
import {connect} from "react-redux";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import React, {useEffect} from "react";
import {deleteRule, getRules, rulesReset, showAddRuleModal, showEditRuleModal} from "../actions/rules";
import {conditionFormatter, ErrorAlert, formatDeviceTitle, InProgressSpinner} from "./util/util";
import Table from "react-bootstrap/Table";
import {AddButton, DeleteButton, EditButton, RefreshButton} from "./util/buttons";
import RuleEditModal from "./RuleEditModal";
import {faCogs} from "@fortawesome/free-solid-svg-icons/faCogs";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {RULE_ACTIONS} from "../constant";
import {faEnvelope} from "@fortawesome/free-solid-svg-icons/faEnvelope";
import {faForward} from "@fortawesome/free-solid-svg-icons/faForward";

function RuleAction({actionType, targetDevice, actionArg}) {
    switch (actionType) {
        case RULE_ACTIONS.SEND_EMAIL:
            return <><FontAwesomeIcon icon={faEnvelope}/> {actionArg}</>;
        case RULE_ACTIONS.FORWARD:
            return <><FontAwesomeIcon icon={faForward}/> {formatDeviceTitle(targetDevice)}</>;
        default:
            return <>"N/A"</>
    }
}


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
        <td>
            <RuleAction actionArg={rule.action_arg} actionType={rule.action_type} targetDevice={rule.target_device}/>
        </td>
        <td>
            <ButtonGroup>
                <EditButton onClick={() => showEditRuleModal(deviceId, rule)}/>
                <DeleteButton onClick={confirmDelete}/>
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
        <Table size={"sm"} hover bordered className="data-table">
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

function Rules({match, device, getRules, rulesReset, showAddRuleModal}) {
    const deviceId = match.params.deviceId;
    useEffect(() => {
        getRules(deviceId);
        return rulesReset
    }, [deviceId, getRules]);
    return <>
        <RuleEditModal deviceId={deviceId}/>
        <h1><FontAwesomeIcon icon={faCogs}/> Szabályok - {formatDeviceTitle(device)}</h1>
        <div className="d-flex">
            <ButtonGroup className="mb-3 ml-auto">
                <AddButton onClick={showAddRuleModal}/>
                <RefreshButton onClick={() => getRules(deviceId)}/>
            </ButtonGroup>
        </div>
        <ConnectedRulesList deviceId={device.id}/>
    </>
}

export default withRouter(
    connect(state => ({device: state.rules.device || {}}), {getRules, rulesReset, showAddRuleModal})(Rules));