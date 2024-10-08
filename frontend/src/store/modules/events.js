import axios from "axios";
import { Promise } from "core-js";
import { socket } from "@/socket";

export default {
  namespaced: true,
  state: {
    alarmEvent: { msgcount: 0, latestDate: "2024", oldestDate: "2024" },
  },
  getters: {},
  mutations: {
    changeBadgeInline(state, newVal) {
      state.badgeInline = newVal;
    },
    updateAlarmEvent(state, newVal) {
      state.alarmEvent = newVal;
    },
  },
  actions: {
    async getUnreadMsg_alarm({ commit }) {
      try {
        const username = JSON.parse(localStorage.getItem("user"))["username"];
        const response = await axios.post("/system/getUnreadAlarmMsg", { username: username });
        if (response.status == 200) {
          commit("updateAlarmEvent", response.data);
        }
      } catch (error) {
        console.error("getUnreadMsg failed", error);
      }
    },
  },
  modules: {},
};
