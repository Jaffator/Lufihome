import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import store from "./store/index";
import "./axios";

// loadFonts();

// axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*"
// axios.defaults.baseURL = "https://192.168.0.107:5000";

createApp(App).use(store).use(router).use(vuetify).mount("#app");
