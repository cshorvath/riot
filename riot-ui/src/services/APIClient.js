import axios from "axios";
import {API_URL, ERRORS} from "../constant";


class APIError extends Error {
    constructor(detail, status) {
        super(`${status}: ${detail}`);
        this.status = status;
        this.detail = detail;
    }
}

class APIClient {

    constructor(baseUrl) {
        this._baseUrl = baseUrl;
    }

    async login(user, password) {
        const data = new FormData();
        data.set("username", user);
        data.set("password", password);
        const response = await this.callAPI("POST", "/token", null, data);
        localStorage.setItem("token", response.data.access_token);
    }


    async getCurrentUser() {
        return (await (this.callAPI("GET", "/user/me"))).data
    }

    async loginAndGetUser(user, password) {
        await this.login(user, password);
        return this.getCurrentUser();
    }

    async getDevices() {
        return (await this.callAPI("GET", "/device")).data
    }


    async getDevice(deviceId) {
        return (await this.callAPI("GET", "/device/" + deviceId)).data
    }

    async addDevice(device) {
        return this.callAPI("POST", "/device", null, device);
    }

    static _formatMessage(response) {
        if (!response) return "Hálózati hiba";
        return ERRORS[response.status] || response.statusText;
    }

    async deleteDevice(deviceId) {
        return this.callAPI("DELETE", "/device/" + deviceId)
    }

    async getMessages(deviceId, page, recordsPerPage) {
        return (
            await this.callAPI("GET", `/device/${deviceId}/message`,
                {page, records_per_page: recordsPerPage})
        ).data;
    }

    async getRules(deviceId) {
        return (await this.callAPI("GET", `/device/${deviceId}/rule`)).data;
    }

    async addRule(deviceId, rule) {
        return (await this.callAPI("POST", `/device/${deviceId}/rule`, null, rule));
    }

    async deleteRule(deviceId, ruleId) {
        return this.callAPI("DELETE", `/device/${deviceId}/rule/${ruleId}`);
    }

    async updateDevice(deviceId, deviceData) {
        return this.callAPI("PUT", "/device/" + deviceId, null, deviceData);
    }

    async updateRule(deviceId, ruleId, rule) {
        return (await this.callAPI("PUT", `/device/${deviceId}/rule/${ruleId}`, null, rule));
    }

    logout() {
        localStorage.setItem("token", null);
    }

    async callAPI(method, url, params = null, body = null) {
        try {
            return await axios.request({
                url: this._baseUrl + url,
                method,
                params,
                data: body,
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem("token")
                }
            });
        } catch (e) {
            throw new APIError(APIClient._formatMessage(e.response), e.response ? e.response.status : null)
        }
    }
}

export default new APIClient(API_URL);