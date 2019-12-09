import APIClient from "../services/APIClient";

export const DEVICES_IN_PROGRESS = "GET_DEVICES";
export const DEVICES_LOADED = "DEVICES_LOADED";
export const DEVICE_ERROR = "DEVICE_ERROR";
export const SHOW_ADD_DEVICE_MODAL = "SHOW_ADD_DEVICE_MODAL";
export const SHOW_EDIT_DEVICE_MODAL = "SHOW_EDIT_DEVICE_MODAL";
export const HIDE_DEVICE_MODAL = "HIDE_DEVICE_MODAL";

function devicesLoaded(devices) {
    return {type: DEVICES_LOADED, devices};
}

function deviceError(error) {
    return {type: DEVICE_ERROR, error};
}

function deviceInProgress() {
    return {type: DEVICES_IN_PROGRESS}
}

export function getDevices() {
    return dispatch => {
        dispatch(deviceInProgress());
        APIClient.getDevices().then(
            devices => dispatch(devicesLoaded(devices),
                error => dispatch(deviceError(error)
                )
            )
        );
    }
}

export function deleteDevice(device) {
    if (window.confirm(`Biztosan törölni akarod a következő eszközt: ${device.name}? `))
        return dispatch => {
            dispatch(deviceInProgress());
            APIClient.deleteDevice(device.id)
                .then(() => dispatch(getDevices()),
                    error => dispatch(deviceError(error)));
        }
}

export function addDevice(device) {
    return dispatch => {
        dispatch(deviceInProgress());
        APIClient.addDevice(device)
            .then(
                () => {
                    dispatch(hideDeviceModal());
                    dispatch(getDevices());
                },
                error => dispatch(deviceError(error)));
    }
}

export function updateDevice(device) {
    return dispatch => {
        dispatch(deviceInProgress());
        APIClient.addDevice(device.id)
            .then(
                () => {
                    dispatch(hideDeviceModal());
                    dispatch(getDevices());
                },
                error => dispatch(deviceError(error)));
    }
}

export function showAddDeviceModal(onSubmit) {
    return {
        type: SHOW_ADD_DEVICE_MODAL
    }
}

export function showEditDeviceModal(device) {
    return {
        type: SHOW_EDIT_DEVICE_MODAL,
        device
    }
}

export function hideDeviceModal() {
    return {
        type: HIDE_DEVICE_MODAL
    }
}
