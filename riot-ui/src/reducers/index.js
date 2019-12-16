import {combineReducers} from "redux";
import login from "./login";
import devices from "./devices";
import messages from "./messages";
import rules from "./rules";


export default combineReducers({
        login,
        devices,
        messages,
        rules,
    }
)