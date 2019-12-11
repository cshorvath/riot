import {MESSAGES_ERROR, MESSAGES_LOADED, MESSAGES_LOADING, MESSAGES_RESET} from "../actions/messages";

export default function (state = {}, action) {
    switch (action.type) {
        case MESSAGES_RESET:
            return {};
        case MESSAGES_LOADING:
            return {...state, isLoading: true, error: null};
        case    MESSAGES_LOADED:
            return {device: action.device, isLoading: false, error: null, ...action.data};
        case    MESSAGES_ERROR:
            return {...state, isLoading: false, error: action.error};
        default:
            return state;
    }
}