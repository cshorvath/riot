import APIClient from "../services/APIClient";

export const RULES_LOADING = "MESSAGES_LOADING";
export const RULES_LOADED = "RULES_LOADED";
export const RULE_LOAD_ERROR = "RULE_LOAD_ERROR";
export const SHOW_ADD_RULE_MODAL = "SHOW_ADD_RULE_MODAL";
export const SHOW_EDIT_RULE_MODAL = "SHOW_EDIT_RULE_MODAL";
export const HIDE_RULE_MODAL = "HIDE_RULE_MODAL";

function rulesLoading() {
    return {
        type: RULES_LOADING
    }
}

function rulesLoaded(device, rules) {
    return {
        type: RULES_LOADED,
        device,
        rules
    }
}

function rulesError(error) {
    return dispatch => {
        dispatch(hideRuleModal());
        dispatch({type: RULE_LOAD_ERROR, error});
    };
}


export function showAddRuleModal() {
    return {
        type: SHOW_ADD_RULE_MODAL
    }
}

export function showEditRuleModal(deviceId, rule) {
    return {
        type: SHOW_EDIT_RULE_MODAL,
        rule
    }
}

export function hideRuleModal() {
    return {
        type: HIDE_RULE_MODAL
    }
}

export function getRules(deviceId) {
    return dispatch => {
        dispatch(rulesLoading());
        APIClient.getDevice(deviceId)
            .then(
                (device) => APIClient.getRules(deviceId)
                    .then(
                        rules => dispatch(rulesLoaded(device, rules)),
                        error => dispatch(rulesError(error))
                    ),
                error => dispatch(rulesError(error))
            )
    }
}

export function addRule(deviceId, rule) {
    return dispatch => {
        APIClient.addRule(deviceId, rule)
            .then(
                () => {
                    dispatch(hideRuleModal());
                    dispatch(getRules());
                },
                error => dispatch(rulesError(error)));
    }
}


export function deleteRule(deviceId, ruleId) {
    return dispatch => {
        APIClient.deleteRule(deviceId, ruleId)
            .then(() => dispatch(getRules(deviceId)),
                error => dispatch(rulesError(error)));
    }
}

export function updateRule(deviceId, ruleId, rule) {
    return dispatch => {
        APIClient.updateRule(deviceId, ruleId, rule)
            .then(
                () => {
                    dispatch(hideRuleModal());
                    dispatch(getRules());
                },
                error => dispatch(rulesError(error)));
    }
}