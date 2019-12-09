import APIClient from "../services/APIClient";

export const GET_DEVICES = "GET_DEVICES";
export const DEVICES_LOADED = "DEVICES_LOADED";
export const DEVICE_ERROR = "DEVICE_ERROR";

function devicesLoaded(devices) {
    return {type: DEVICES_LOADED, devices};
}

function deviceError(error) {
    return {type: DEVICE_ERROR, error};
}

export function getDevices() {
    return dispatch => {
        dispatch({type: GET_DEVICES});
        APIClient.getDevices().then(
            devices => dispatch(devicesLoaded(devices),
                error => dispatch(deviceError(error)
                )
            )
        );
    }

}