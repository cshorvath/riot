import {combineReducers} from "redux";
import login from "./login";
import devices from "./devices";
import messages from "./messages";
import rules from "./rules";
import users from "./users";


export default combineReducers({
        login,
        devices,
        messages,
        rules,
        users
    }
)