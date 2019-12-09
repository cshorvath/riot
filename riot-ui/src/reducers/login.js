import {LOGIN_ERROR, LOGIN_REQUEST, LOGIN_SUCCESS, LOGOUT} from "../actions/login";

export default function (state={}, action) {
    switch (action.type) {
        case LOGIN_REQUEST:
            return {inProgress: true};
        case LOGIN_SUCCESS:
            return {inProgress: false, user: action.user};
        case LOGIN_ERROR:
            return {inProgress: false, error: action.error};
        case LOGOUT:
            return {inProgress: false, user: null};
        default:
            return state;
    }
}