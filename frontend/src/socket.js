import { reactive } from "vue";
// import { io } from "socket.io-client";

export const state = reactive({
  connected: false,
});

// // "undefined" means the URL will be computed from the `window.location` object
// const URL = process.env.NODE_ENV === "production" ? undefined : "http://95.85.210.12";
const URL = process.env.NODE_ENV === "production" ? undefined : "http://192.168.0.107:5000";

export const socket = io(URL);

socket.on("connect", () => {
  state.connected = socket.connected;
});

socket.on("disconnect", () => {
  state.connected = false;
});