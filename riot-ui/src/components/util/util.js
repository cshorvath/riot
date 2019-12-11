import Alert from "react-bootstrap/Alert";
import React from "react";
import Spinner from "react-bootstrap/Spinner";
import {OPERATOR} from "../../constant";

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
