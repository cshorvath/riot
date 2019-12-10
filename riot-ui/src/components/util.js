import Alert from "react-bootstrap/Alert";
import React from "react";
import Spinner from "react-bootstrap/Spinner";

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

const conditionFormat = {
    "LT": (field, arg1) => `${field} < ${arg1}`,
    "LTE": (field, arg1) => `${field} <= ${arg1}`,
    "GT": (field, arg1) => `${field} > ${arg1}`,
    "GTE": (field, arg1) => `${field} >= ${arg1}`,
    "EQ": (field, arg1) => `${field} == ${arg1}`,
    "NE": (field, arg1) => `${field} != ${arg1}`,
    "BETWEEN": (field, arg1, arg2) => `${arg1} <= ${field} <= ${arg2}`,
    "ANY": (field) => `!!${field}`
};

export function conditionFormatter(operator, field, arg1, arg2) {
    const formatter = conditionFormat[operator];
    if (!formatter) return "N/A";
    return formatter(field, arg1, arg2);

}