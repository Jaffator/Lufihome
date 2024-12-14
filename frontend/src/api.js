import axios from "axios";

const lufihomeUr = process.env.NODE_ENV === "production" ? "http://www.lufihome.cz/api/" : "http://192.168.0.107:5000/api/";
const authService = axios.create({
  baseURL: "http://www.lufihome.cz/api/",
  // baseURL: "http://95.85.210.12/",
  // baseURL: "http://192.168.0.107:5000/api/",
  withCredentials: true,
  xsrfCookieName: "csrf_access_token",
});
export { authService };
