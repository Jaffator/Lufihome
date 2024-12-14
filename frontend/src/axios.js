import axios from "axios";
import store from "./store";

function getCookie() {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; csrf_access_token=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

axios.defaults.baseURL = "http://www.lufihome.cz/api/";
// axios.defaults.baseURL = "http://95.85.210.12/";
// axios.defaults.baseURL = "http://192.168.0.107:5000/api/";
axios.defaults.withCredentials = true;

// must use interceptors if function getCookie() works for very request! -> this interceptor send x-csrf-token to every request header
axios.interceptors.request.use(
  (config) => {
    const token = getCookie(); // Adjust the cookie name if needed
    if (token) {
      config.headers["X-CSRF-TOKEN"] = token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// this interceptor check every response if it autorized response or not
axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response.status === 401) {
      //place your reentry code
      store.dispatch("auth/logout");
    }
    return Promise.reject(error);
  }
);
