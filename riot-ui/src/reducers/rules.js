import {
    HIDE_RULE_MODAL,
    RULE_EDIT_ERROR,
    RULE_LOAD_ERROR,
    RULES_LOADED,
    RULES_LOADING,
    RULES_RESET,
    SHOW_ADD_RULE_MODAL,
    SHOW_EDIT_RULE_MODAL
} from "../actions/rules";

const initialState = {
    isLoading: false,
    modal: {rule: null, show: false},
    error: null,
    rules: [],
    device: null
};

export default function (state = initialState, action) {
    switch (action.type) {
        case RULES_RESET:
            return {...initialState};
        case HIDE_RULE_MODAL:
            return {...state, modal: {show: false, rule: null}};
        case RULE_LOAD_ERROR:
            return {...state, isLoading: false, error: action.error};
        case RULES_LOADED:
            return {...state, rules: action.rules, device: action.device, error: null, isLoading: false};
        case RULE_EDIT_ERROR:
            return {...state, modal: {...state.modal, error: action.error}};
        case RULES_LOADING:
            return {...state, isLoading: true};
        case SHOW_ADD_RULE_MODAL:
            return {...state, modal: {show: true, rule: null}};
        case SHOW_EDIT_RULE_MODAL:
            return {...state, modal: {show: true, rule: action.rule}};
        default:
            return state
    }
}