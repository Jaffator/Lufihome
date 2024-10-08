import axios from "axios";
import { Promise } from "core-js";
import { socket } from "@/socket";

export default {
  namespaced: true,
  state: {
    houseSwitch: false,
    nightmodeSwitch: false,
    alarmState: "disarm",
    origin: false,
    armTime: 0,
    areaData: [],
    test: [{ test: true, test1: "ahoj" }],
  },
  getters: {},
  mutations: {
    houseSwitch(state, newVal) {
      state.houseSwitch = newVal;
    },
    nightmodeSwitch(state, newVal) {
      state.nightmodeSwitch = newVal;
    },
    changeOrigin(state, newVal) {
      state.origin = newVal;
    },
    changeAlarmState(state, newAlarmState) {
      state.alarmState = newAlarmState;
    },
    changeArmTime(state, newArmTime) {
      state.armTime = newArmTime;
    },
    updateAreas(state, newAreas) {
      state.areaData = newAreas;
    },
    HouseAll(state, newSwitchState) {
      for (var key in state.areaData) {
        state.areaData[key].Switch = newSwitchState;
      }
      state.houseSwitch = newSwitchState;
    },
    changeAreaStatus(state, index) {
      for (var key in state.areaData) {
        if (key == index) {
          state.areaData[key].Switch = !state.areaData[key].Switch;
        }
      }
    },
    nigthmodeAreas(state, { NightAreaID, switchState }) {
      for (var key in state.areaData) {
        if (NightAreaID == state.areaData[key].AreaID) {
          state.areaData[key].Switch = switchState;
        }
      }
    },
  },
  actions: {
    reinit_alarm() {
      axios
        .post("/reinit_alarm")
        .then((response) => {})
        .catch((error) => {
          console.log(error);
        });
    },
    getArmTime({ commit }) {
      axios
        .get("/getAlarmSetting")
        .then((response) => {
          commit("changeArmTime", response.data["armtime"]);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    testAlarm() {
      socket.emit("testAlarm");
    },
    nightmode({ commit, state }) {
      socket.emit("nightmode", state.nightmodeSwitch);
    },
    houseall({ commit, state }) {
      socket.emit("houseall", state.houseSwitch);
    },
    getNightmode({ commit, state }, newSwitchState) {
      commit("nightmodeSwitch", newSwitchState);
      axios
        .get("/getNightmode")
        .then((response) => {
          for (var key in response.data) {
            commit("nigthmodeAreas", { NightAreaID: response.data[key].AreaID, switchState: newSwitchState });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    sendUpdateAreas({ commit, state }) {
      return new Promise((resolve, reject) => {
        axios
          .post("/updateAreas", state.areaData)
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    pushSetting({ commit }, selectSetting) {
      return new Promise((resolve, reject) => {
        axios
          .post("/pushSetting", selectSetting)
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    resetOrigin({ commit }) {
      socket.emit("resetOrigin");
    },
    checkAlarmCode({ commit }, alarmCode) {
      return new Promise((resolve, reject) => {
        axios
          .post("/checkAlarmCode", { alarmCode: alarmCode })
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },

    // ------ get SETTING ------
    getSetting({ commit }, payload) {
      return new Promise((resolve, reject) => {
        axios
          .post("/getSetting", payload)
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    // ------ set SETTING ------
    setSetting({ commit }, payload) {
      return new Promise((resolve, reject) => {
        axios
          .post("/setSetting", payload)
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            resolve(error);
          });
      });
    },
    // ------ get AREAS ------
    getAreas({ commit }) {
      axios
        .get("/getAreas")
        .then((response) => {
          commit("updateAreas", response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // ------ start beeping sound ------
    startBeeping({ commit }, payload) {
      console.log(payload);
      axios
        .post("/startBeeping", { beep: payload })
        .then((response) => {})
        .catch((error) => {
          console.log(error);
        });
    },
    turnOffSirene({ commit }) {
      axios
        .post("/turnOffSirene")
        .then((response) => {})
        .catch((error) => {
          console.log(error);
        });
    },
    disarm({ commit }) {
      axios
        .post("/disarm")
        .then((response) => {})
        .catch((error) => {
          console.log(error);
        });
    },
  },
  modules: {},
};
