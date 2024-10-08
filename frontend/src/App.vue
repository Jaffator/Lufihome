<template>
  <div v-if="isLoggedIn">
    <Navigation v-on:changeBody="changeMargin($event)" v-bind:updateMargin="marginLeft" />
    <div class="content_wrapper" :style="{ 'margin-left': computedMargin }">
      <router-view />
    </div>
  </div>
  <LoginView v-if="showLogin"></LoginView>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";
import { socket } from "@/socket";
import Navigation from "./components/Navigation.vue";
import LoginView from "./views/LoginView.vue";
// import { test } from "./socket.js";

export default {
  data() {
    return {
      marginLeft: "",
    };
  },
  name: "App",
  components: {
    Navigation,
    LoginView,
  },
  computed: {
    ...mapState(["auth"]),
    isLoggedIn() {
      return this.auth.isLoggedIn;
    },
    showLogin() {
      return this.auth.showLogin;
    },

    computedMargin: function () {
      return this.marginLeft;
    },
  },
  beforeCreate() {
    this.$store.dispatch("auth/checkToken").then(
      (response) => {
        if (response.status == 200) {
          console.log("User is logged in!");
          this.$store.commit("auth/initializeStore");
          this.$store.dispatch("events/getUnreadMsg_alarm");
        }
      },
      (error) => {
        console.log(error);
        this.$store.commit("auth/changeShowLogin", true);
      }
    );
  },
  created() {
    socket.connect();
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();
    // test.connect();
  },

  beforeDestroy() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    onResize() {
      if (window.innerWidth < 600) {
        this.marginLeft = "0px";
      } else {
        this.marginLeft = "85px";
      }
    },
    changeMargin: function (margin) {
      this.marginLeft = margin;
      // console.log(margin);
    },
  },
};
</script>

<style>
@import "./assets/hamburgers.css";
body {
  --bs-body-font-family: Verdana, Geneva, Tahoma, sans-serif;
  padding-right: 0 !important;
}

.content_wrapper {
  margin-top: 57px;
}

/* @media screen and (min-width: 1000px) {
  .fixed-bottom {
    position: relative;
  }
} */
</style>
