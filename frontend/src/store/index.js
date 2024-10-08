import { createStore } from "vuex";
import alarm from "./modules/alarm";
import sensors from "./modules/sensors";
import auth from "./modules/auth";
import events from "./modules/events";
import socketPlugin from "@/plugins/socketToStore";

export default createStore({
  plugins: [socketPlugin()],
  modules: {
    alarm,
    sensors,
    auth,
    events,
  },
});
