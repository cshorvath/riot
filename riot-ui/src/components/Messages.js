import React, {useEffect, useState} from "react";
import {withRouter} from "react-router";
import {connect} from "react-redux";
import {getMessages, messagesReset} from "../actions/messages";
import Pagination from "react-bootstrap/Pagination";
import {ErrorAlert, formatDeviceTitle, InProgressSpinner} from "./util";
import Table from "react-bootstrap/Table";
import Chart from "./Chart";
import {MESSAGES_PER_PAGE} from "../reducers/constant";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";
import {RefreshButton} from "./buttons";
import {faChartLine} from "@fortawesome/free-solid-svg-icons/faChartLine";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTable} from "@fortawesome/free-solid-svg-icons/faTable";
import {faInbox} from "@fortawesome/free-solid-svg-icons/faInbox";

function collectRecordKeys(items) {
    const keys = new Set();
    for (const item of items) {
        if (!item.payload)
            continue;
        Object.keys(item.payload).forEach(k => keys.add(k))
    }
    return [...keys];
}

function Paginator({recordCount, page, pageCount, setPage}) {
    if (!recordCount)
        return null;
    return <div className="mt-3">
        <div className="d-flex justify-content-between">
            <div><span className="text-info">{recordCount} üzenet ({pageCount} oldal)</span></div>
            <Pagination>
                <Pagination.First onClick={() => setPage(1)} disabled={page === 1}/>
                <Pagination.Prev onClick={() => setPage(page - 1)} disabled={page === 1}/>
                <Pagination.Item active>{page}</Pagination.Item>
                <Pagination.Next onClick={() => setPage(page + 1)} disabled={page >= pageCount}/>
                <Pagination.Last onClick={() => setPage(pageCount)} disabled={page >= pageCount}/>
            </Pagination>
            <div><span
                className="text-info">{(page - 1) * MESSAGES_PER_PAGE + 1} -
                {page === pageCount ? recordCount : page * MESSAGES_PER_PAGE}</span>
            </div>
        </div>
    </div>;
}

function MessageRow({item, recordKeys}) {
    return <tr>
        <td>{item.timestamp}</td>
        <td>{item.direction}</td>
        {recordKeys.map(k => <td key={`message_${item.id}_${k}`}>{item.payload[k]}</td>)}
    </tr>
}


function MessageTable({isLoading, items, recordKeys}) {
    if (isLoading)
        return <InProgressSpinner/>;
    return <>
        <Table size="sm" className="data-table" hover>
            <thead>
            <tr>
                <th>Időpont</th>
                <th>Irány</th>
                {recordKeys.map(k => <th key={k}>{k}</th>)}
            </tr>
            </thead>
            <tbody>
            {items.map(item => <MessageRow item={item} recordKeys={recordKeys} key={"message_" + item.id}/>)}
            </tbody>
        </Table>
    </>;
}

function MessagesBody({isLoading, items, recordCount, page, pageCount, error, setPage}) {
    const [tab, setTab] = useState("table");
    if (error)
        return <ErrorAlert error={error.detail}/>;
    if (!items.length && !isLoading)
        return <div className="d-flex">
            <h2 className="text-secondary mx-auto">Nincsenek üzenetek</h2>
        </div>;
    const paginator = <Paginator recordCount={recordCount} page={page} pageCount={pageCount} setPage={setPage}/>;
    const recordKeys = collectRecordKeys(items);
    return <>
        {paginator}
        <Tabs id="controlled-tab-example" activeKey={tab} onSelect={k => setTab(k)}>
            <Tab eventKey="table" title={<><FontAwesomeIcon icon={faTable}/>Táblázat</>}>
                <MessageTable isLoading={isLoading} items={items} recordKeys={recordKeys}/>
            </Tab>
            <Tab eventKey="chart" title={<><FontAwesomeIcon icon={faChartLine}/>Grafikon</>}>
                <Chart items={items} recordKeys={recordKeys}/>
            </Tab>
        </Tabs>
        {paginator}
    </>
}

function Messages({match, isLoading, device, items = [], pageCount, recordCount, error, getMessages, messagesReset}) {
    const {deviceId} = match.params;
    const [page, setPage] = useState(1);
    useEffect(() => {
        getMessages(deviceId, page);
        return messagesReset
    }, [page, deviceId, getMessages]);
    return <>
        <div className={"d-flex justify-content-between"}>
            <h1><FontAwesomeIcon icon={faInbox}/> Üzenetek - {formatDeviceTitle(device)}</h1>
            <div className="align-self-center mr-2">
                <RefreshButton onClick={() => getMessages(deviceId, page)}/>
            </div>
        </div>
        <MessagesBody isLoading={isLoading}
                      items={items}
                      page={page}
                      pageCount={pageCount}
                      recordCount={recordCount}
                      error={error}
                      setPage={setPage}/>
    </>
}

export default withRouter(connect(state => state.messages, {getMessages, messagesReset})(Messages));