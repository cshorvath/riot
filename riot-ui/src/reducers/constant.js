export const MESSAGES_PER_PAGE = 50;


export const OPERATOR = {
    LT: {
        id: "LT",
        displayName: "<",
        argCount: 1,
        formatter: (field, arg1) => `${field} < ${arg1}`
    },
    LTE: {
        id: "LTE",
        displayName: "<=",
        argCount: 1,
        formatter: (field, arg1) => `${field} <= ${arg1}`
    },
    GT: {
        id: "GT",
        displayName: ">",
        argCount: 1,
        formatter: (field, arg1) => `${field} > ${arg1}`
    },
    GTE: {
        id: "GTE",
        displayName: ">=",
        argCount: 1,
        formatter: (field, arg1) => `${field} >= ${arg1}`
    },
    EQ: {
        id: "EQ",
        displayName: "==",
        argCount: 1,
        formatter: (field, arg1) => `${field} == ${arg1}`
    },
    NE: {
        id: "NE",
        displayName: "!=",
        argCount: 1,
        formatter: (field, arg1) => `${field} != ${arg1}`
    },
    BETWEEN: {
        id: "BETWEEN",
        displayName: "KÖZÖTT",
        argCount: 2,
        formatter: (field, arg1, arg2) => `${arg1} <= ${field} <= ${arg2}`
    },
    ANY: {
        id: "ANY",
        displayName: "BÁRMI",
        argCount: 0,
        formatter: (field) => `!!${field}}`
    }
};

export const RULE_ACTIONS = {
    SEND_EMAIL: "SEND_EMAIL",
    FORWARD: "FORWARD"
};
