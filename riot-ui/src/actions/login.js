import APIClient from "../services/APIClient";

export const LOGIN_INIT = "LOGIN_INIT";
export const LOGIN_REQUEST = "LOGIN_REQUEST";
export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export const LOGIN_ERROR = "LOGIN_ERROR";
export const LOGOUT = "LOGIN_ERROR";

function loginSuccess(user) {
    return {
        type: LOGIN_SUCCESS,
        user
    }
}

function loginError(error) {
    return {
        type: LOGIN_ERROR,
        error
    }
}

function loginInit() {
    return {
        type: LOGIN_INIT,
    }
}

function login(user, password) {
    return dispatch => APIClient.loginAndGetUser(user, password)
        .then(
            user => dispatch(loginSuccess(user)),
            error => dispatch(loginError(error))
        );
}

export function getUserWithStoredToken() {
    return dispatch => {
        dispatch({type: LOGIN_REQUEST});
        dispatch(dispatch => {
            APIClient.getCurrentUser()
                .then(
                    user => dispatch(loginSuccess(user)),
                    () => dispatch(loginInit())
                );
        });
    }
}


export function loginRequest(user, password) {
    return dispatch => {
        dispatch({type: LOGIN_REQUEST});
        dispatch(login(user, password));
    }
}

export function logout() {
    APIClient.logout();
    return {
        type: LOGOUT
    }
}
