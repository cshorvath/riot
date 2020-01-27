import C3Chart from "react-c3js";
import 'c3/c3.css';
import React from "react";

const axis = {
    x: {
        type: 'timeseries',
        tick: {
            format: '%Y-%m-%dT%H:%M:%S'
        }
    }
};

export default function Chart({items, recordKeys}) {
    const data = {
        x: "x",
        xFormat: '%Y-%m-%dT%H:%M:%S',
        columns: recordKeys.map(key => {
            const ret = new Array(items.length + 1);
            ret[0] = key;
            return ret;
        }),
        unload: true
    };
    const timestamps = new Array(items.length + 1);
    timestamps[0] = "x";
    data.columns.push(timestamps);
    items.forEach((item, itemIdx) => {
            recordKeys.forEach((key, keyIdx) => data.columns[keyIdx][itemIdx + 1] = item.payload[key] || 0);
            data.columns[recordKeys.length][itemIdx + 1] = item.timestamp;
        }
    );
    return <C3Chart data={data} axis={axis} />
}