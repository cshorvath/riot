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
