import React, {useEffect, useState} from "react";
import {withRouter} from "react-router";
import {connect} from "react-redux";
import {getMessages} from "../actions/messages";
import Pagination from "react-bootstrap/Pagination";
import {InProgressSpinner} from "./util";
import Table from "react-bootstrap/Table";


function Paginator({recordCount, page, pageCount, setPage}) {
    return <div className="mt-3">
        <div className="d-flex">
            <div className="mr-auto"><span className="text-info">{recordCount} üzenet</span></div>
            <Pagination className="mx-auto">
                <Pagination.First onClick={() => setPage(1)} disabled={page === 1}/>
                <Pagination.Prev onClick={() => setPage(page - 1)} disabled={page === 1}/>
                <Pagination.Item active>{page}</Pagination.Item>
                <Pagination.Next onClick={() => setPage(page + 1)} disabled={page >= pageCount}/>
                <Pagination.Last onClick={() => setPage(pageCount)} disabled={page >= pageCount}/>
            </Pagination>
            <div className="ml-auto"><span
                className="text-info">{(page - 1) * 100 + 1} - {page === pageCount ? recordCount : page * 100}</span>
            </div>
        </div>
    </div>;
}

function collectRecordKeys(items) {
    const keys = new Set();
    for (const item of items) {
        if (!item.payload)
            continue;
        Object.keys(item.payload).forEach(k => keys.add(k))
    }
    return [...keys];
}

function MessageRow({item, recordKeys}) {
    return <tr>
        <td>{item.timestamp}</td>
        <td>{item.direction}</td>
        {recordKeys.map(k => <td>{item.payload[k]}</td>)}
    </tr>
}

function MessageTable({isLoading, items}) {
    const recordKeys = collectRecordKeys(items);
    if (isLoading)
        return <InProgressSpinner/>;
    return <Table className="message-table" striped>
        <thead>
        <tr>
            <th>Időpont</th>
            <th>Irány</th>
            {recordKeys.map(k => <th>{k}</th>)}
        </tr>
        </thead>
        <tbody>
        {items.map(item => <MessageRow item={item} recordKeys={recordKeys}/>)}
        </tbody>
    </Table>;
}

function Messages({match, isLoading, device, items = [], pageCount, recordCount, error, getMessages}) {
    const {deviceId} = match.params;
    const [page, setPage] = useState(1);
    useEffect(() => {
            getMessages(deviceId, page);
        },
        [page]);
    const paginator = <Paginator recordCount={recordCount} page={page} pageCount={pageCount} setPage={setPage}/>;
    return <>
        <h1 className="mb-5">Üzenetek - {device && device.name}</h1>
        {paginator}
        <MessageTable isLoading={isLoading} items={items}/>
        {!!recordCount && !isLoading && paginator}
    </>
}

export default withRouter(connect(state => state.messages, {getMessages})(Messages));