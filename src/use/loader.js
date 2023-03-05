import axios from "axios"

const useLoader = function() {

    const api = "http://localhost:5000"

    async function get(url, params={}) {
        const what = url.startsWith("/") ? url : "/"+url;
        return axios.get(api+what, { params: params })
            .then(response => response.data)
    }

    async function post(url, body, params={}) {
        const what = url.startsWith("/") ? url : "/"+url;
        return axios.post(api+what, body, { params: params })
            .then(response => response.data)
    }

    return {
        get,
        post
    }
}

export default useLoader;
