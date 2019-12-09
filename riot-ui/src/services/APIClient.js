import axios from "axios";


class APIError extends Error {
    constructor(detail, statusCode) {
        super(`${statusCode}: ${detail}`);
        this.statusCode = statusCode;
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
        return (await this.callAPI("GET", "/device/")).data
    }


    async addDevice(device) {
        return this.callAPI("POST", "/device/", null, device);
    }

    async deleteDevice(deviceId) {
        return this.callAPI("DELETE", "/device/" + deviceId)
    }

    async callAPI(method, url, params = null, body = null) {
        try {
            const response = await axios.request({
                url: this._baseUrl + url,
                method,
                params,
                data: body,
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem("token")
                }
            });
            console.log(response);
            return response;
        } catch (e) {
            if (!e.response) {
                throw new APIError("Network error")
            }
            throw new APIError(e.response.statusText, e.response.status)
        }
    }

    logout() {
        localStorage.setItem("token", null);
    }
}

export default new APIClient("http://localhost:8000");