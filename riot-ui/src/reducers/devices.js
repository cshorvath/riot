import {
    DEVICE_LOAD_ERROR,
    DEVICES_IN_PROGRESS,
    DEVICES_LOADED,
    HIDE_DEVICE_MODAL,
    SHOW_ADD_DEVICE_MODAL,
    SHOW_EDIT_DEVICE_MODAL
} from "../actions/devices";

const initialState = {modal: {}};

export default function (state = initialState, action) {
    switch (action.type) {
        case SHOW_ADD_DEVICE_MODAL:
            return {
                ...state,
                modal: {show: true, inProgress: false}
            };
        case SHOW_EDIT_DEVICE_MODAL:
            return {
                ...state,
                modal: {show: true, device: action.device, inProgress: false}
            };
        case HIDE_DEVICE_MODAL:
            return {
                ...state,
                modal: {...state.modal, show: false, inProgress: false}
            };
        case DEVICES_IN_PROGRESS:
            return {devices: [], isLoading: true, error: null};
        case DEVICES_LOADED:
            return {devices: action.devices, isLoading: false, error: null};
        case DEVICE_LOAD_ERROR:
            return {...state, isLoading: false, error: action.error};
        default:
            return state;
    }
}