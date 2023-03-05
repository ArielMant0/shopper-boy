import axios from "axios"

const useLoader = function() {

    const api = "http://localhost:5000"

    async function get(url) {
        const what = url.startsWith("/") ? url : "/"+url;
        return axios.get(api+what).then(response => response.data)
    }

    async function post(url, body) {
        const what = url.startsWith("/") ? url : "/"+url;
        return axios.post(api+what, body).then(response => response.data)
    }

    return {
        get,
        post
    }
}

export default useLoader;
