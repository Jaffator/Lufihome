import axios from "axios";

const authService = axios.create({
  baseURL: "http://192.168.0.107:5000/",
  withCredentials: true,
  xsrfCookieName: "csrf_access_token",
});
export { authService };