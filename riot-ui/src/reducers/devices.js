import {DEVICE_ERROR, DEVICES_LOADED, GET_DEVICES} from "../actions/devices";

export default function (state = {}, action) {
    switch (action.type) {
        case GET_DEVICES:
            return {devices: [], isLoading: true, error: null};
        case DEVICES_LOADED:
            return {devices: action.devices, isLoading: false, error: null};
        case DEVICE_ERROR:
            return {...state, isLoading: false, error: action.error};
        default:
            return state;
    }
}