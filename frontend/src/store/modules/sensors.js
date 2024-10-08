import axios from "axios";
import { Promise } from "core-js";
import { socket } from "@/socket";

export default {
  namespaced: true,
  state: {
    gateStatus: "close",
    sensorState: [],
    gateSensorUpID: 0,
    gateSensorDownID: 0,
  },
  getters: {},
  mutations: {
    updateSensorState(state, newVal) {
      state.sensorState = newVal;
    },
    updateGateState(state, newVal) {
      state.gateStatus = newVal;
    },
    // udpate gate upper sensorID
    gateSensorUp(state, newVal) {
      state.gateSensorUpID = newVal;
    },
    // udpate gate bottom sensorID
    gateSensorDown(state, newVal) {
      state.gateSensorDownID = newVal;
    },
  },
  actions: {
    // ------ get sensors state ------
    getSensorsState({ commit }) {
      return new Promise((resolve, reject) => {
        axios
          .post("/getSensorsState")
          .then((response) => {
            commit("updateSensorState", response.data);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
  },
  modules: {},
};
