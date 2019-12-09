import APIClient from "../services/APIClient";

export const MESSAGES_LOADING = "MESSAGES_LOADING";
export const MESSAGES_LOADED = "MESSAGES_LOADED";
export const MESSAGES_ERROR = "MESSAGES_ERROR";

function messagesLoading(page) {
    return {
        type: MESSAGES_LOADING,
        page
    }
}

function messagesLoaded(device, {items, page, page_count, record_count}) {
    return {
        type: MESSAGES_LOADED,
        device: device,
        data: {
            pageCount: page_count,
            recordCount: record_count,
            items,
            page
        }
    }
}

function messagesError(error) {
    return {
        type: MESSAGES_ERROR,
        error
    }
}

export function getMessages(deviceId, page) {
    return dispatch => {
        dispatch(messagesLoading());
        APIClient.getDevice(deviceId)
            .then(
                (device) => APIClient.getMessages(deviceId, page)
                    .then(
                        data => dispatch(messagesLoaded(device, data)),
                        error => dispatch(messagesError(error))
                    ),
                error => dispatch(messagesError(error))
            )
    }
}