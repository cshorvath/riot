import Alert from "react-bootstrap/Alert";
import React from "react";
import Spinner from "react-bootstrap/Spinner";
import {OPERATOR, RULE_ACTIONS} from "../reducers/constant";
import {faEnvelope} from "@fortawesome/free-solid-svg-icons/faEnvelope";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faForward} from "@fortawesome/free-solid-svg-icons/faForward";

export function ErrorAlert({error}) {
    if (error)
        return <Alert variant="danger">
            {error}
        </Alert>;
    return null;
}

export function visible(child) {
    return ({show = true}) => {
        if (show) return child;
        return null;
    }
}

export const InProgressSpinner = visible(
    <div className="text-center">
        <Spinner animation={"grow"}/>
    </div>
);


export function formatDeviceTitle(device) {
    if (!device || !device.name || !device.id) return "";
    return `${device.name}[${device.id}]`;
}

export function conditionFormatter(operator, field, arg1, arg2) {
    const op = OPERATOR[operator];
    if (!op) return "N/A";
    return op.formatter(field, arg1, arg2);
}

export function RuleAction({actionType, targetDevice, actionArg}) {
    switch (actionType) {
        case RULE_ACTIONS.SEND_EMAIL:
            return <><FontAwesomeIcon icon={faEnvelope}/> {actionArg}</>;
        case RULE_ACTIONS.FORWARD:
            return <><FontAwesomeIcon icon={faForward}/> {formatDeviceTitle(targetDevice)}</>;
        default:
            return <>"N/A"</>
    }

}