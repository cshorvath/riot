import React from "react";
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import App from "./components/App";
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import store from "./store/store";
import {Provider} from "react-redux";


ReactDOM.render(
    <Provider store={store}>
        <App/>
    </Provider>,
    document.getElementById('root'));

serviceWorker.unregister();
