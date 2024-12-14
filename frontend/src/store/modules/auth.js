import axios from "axios";
import { Promise } from "core-js";
import router from "../../router";

export default {
  namespaced: true,
  state: {
    user: {},
    admin: false,
    isLoggedIn: false,
    showLogin: false,
  },
  getters: {},
  mutations: {
    // udpate gate bottom sensorID
    changeLoggedStatus(state, newVal) {
      state.isLoggedIn = newVal;
    },
    changeShowLogin(state, newVal) {
      state.showLogin = newVal;
    },
    setUser(state, user) {
      localStorage.setItem("user", JSON.stringify(user));
    },
    clearUser(state) {
      state.user = null;
      localStorage.removeItem("user");
    },
    initializeStore(state) {
      state.user = JSON.parse(localStorage.getItem("user"));
      if (state.user["role"] == "admin") {
        state.admin = true;
      } else {
        state.admin = false;
      }
    },
  },
  actions: {
    // ------ get sensors state ------
    logout({ commit }) {
      axios.post("auth/logout").then((response) => {
        console.log(response.data);
      });
      router.push("/");
      commit("changeLoggedStatus", false);
      commit("changeShowLogin", true);
      commit("clearUser");
    },
    checkToken({ commit }) {
      return new Promise((resolve, reject) => {
        axios
          .get("/auth/checktoken")
          .then((response) => {
            if (response.status == 200) {
              commit("changeLoggedStatus", true);
            } else {
              commit("changeLoggedStatus", false);
              console.log(response);
            }
            resolve(response);
          })
          .catch((error) => {
            commit("changeLoggedStatus", false);
            console.log(error);
            reject(error);
          });
      });
    },
  },
  modules: {},
};
