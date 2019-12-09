import {DEVICE_ERROR, DEVICES_LOADED, DEVICES_IN_PROGRESS, SHOW_ADD_DEVICE_MODAL} from "../actions/devices";

export default function (state = {}, action) {
    switch (action.type) {
        case SHOW_ADD_DEVICE_MODAL:
            return {
                ...state,
                modal: {show: true, inProgress: false}
            };
        case DEVICES_IN_PROGRESS:
            return {devices: [], isLoading: true, error: null};
        case DEVICES_LOADED:
            return {devices: action.devices, isLoading: false, error: null};
        case DEVICE_ERROR:
            return {...state, isLoading: false, error: action.error};
        default:
            return state;
    }
}