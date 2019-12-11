import APIClient from "../services/APIClient";

export const RULES_RESET = "RULES_RESET";
export const RULES_LOADING = "MESSAGES_LOADING";
export const RULES_LOADED = "RULES_LOADED";
export const RULE_LOAD_ERROR = "RULE_LOAD_ERROR";
export const RULE_EDIT_ERROR = "RULE_EDIT_ERROR";
export const SHOW_ADD_RULE_MODAL = "SHOW_ADD_RULE_MODAL";
export const SHOW_EDIT_RULE_MODAL = "SHOW_EDIT_RULE_MODAL";
export const HIDE_RULE_MODAL = "HIDE_RULE_MODAL";

export function rulesReset() {
    return {
        type: RULES_RESET
    }
}

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

function ruleLoadError(error) {
    return dispatch => {
        dispatch({type: RULE_LOAD_ERROR, error});
    };
}

function ruleEditError(error) {
    return {
        type: RULE_EDIT_ERROR,
        error
    }
}


export function showAddRuleModal(deviceId) {
    return {
        type: SHOW_ADD_RULE_MODAL,
        deviceId
    }
}

export function showEditRuleModal(deviceId, rule) {
    return {
        type: SHOW_EDIT_RULE_MODAL,
        deviceId,
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
                        error => dispatch(ruleLoadError(error))
                    ),
                error => dispatch(ruleLoadError(error))
            )
    }
}

export function addRule(deviceId, rule) {
    return dispatch => {
        APIClient.addRule(deviceId, rule)
            .then(
                () => {
                    dispatch(hideRuleModal());
                    dispatch(getRules(deviceId));
                },
                error => dispatch(ruleEditError(error)));
    }
}


export function deleteRule(deviceId, ruleId) {
    return dispatch => {
        APIClient.deleteRule(deviceId, ruleId)
            .then(() => dispatch(getRules(deviceId)),
                error => dispatch(ruleLoadError(error)));
    }
}

export function updateRule(deviceId, ruleId, rule) {
    return dispatch => {
        APIClient.updateRule(deviceId, ruleId, rule)
            .then(
                () => {
                    dispatch(hideRuleModal());
                    dispatch(getRules(deviceId));
                },
                error => dispatch(ruleEditError(error)));
    }
}