export const MESSAGES_PER_PAGE = 50;

export const conditionFormat = {
    "LT": (field, arg1) => `${field} < ${arg1}`,
    "LTE": (field, arg1) => `${field} <= ${arg1}`,
    "GT": (field, arg1) => `${field} > ${arg1}`,
    "GTE": (field, arg1) => `${field} >= ${arg1}`,
    "EQ": (field, arg1) => `${field} == ${arg1}`,
    "NE": (field, arg1) => `${field} != ${arg1}`,
    "BETWEEN": (field, arg1, arg2) => `${arg1} <= ${field} <= ${arg2}`,
    "ANY": (field) => `!!${field}`
};

export const RULE_ACTIONS = {
    SEND_EMAIL: "SEND_EMAIL",
    FORWARD: "FORWARD"
};
