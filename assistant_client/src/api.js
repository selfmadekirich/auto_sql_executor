import axios from "axios"
import { ACCESS_TOKEN } from "./constants"

console.log(process.env.REACT_APP_BACK_API_URL)

const api = axios.create({
    baseURL: process.env.REACT_APP_BACK_API_URL
})

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token){
            config.headers.Authorization = `Bearer ${token}`
        }

        config.headers.set("Access-Control-Allow-Origin", "*");
        config.headers.set("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");

        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default api