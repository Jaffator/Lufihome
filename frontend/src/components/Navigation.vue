<template>
  <header>
    <!-- Sidebar -->

    <nav id="sidebarMenu" class="sidebar" v-bind:style="{ width: width }">
      <div class="position-sticky">
        <div class="burgerWrap">
          <button @click="expandSidebar" :class="hamburger" type="button">
            <span class="hamburger-box">
              <span class="hamburger-inner"></span>
            </span>
          </button>
        </div>
        <Sidebar v-bind:display="display" />
      </div>
    </nav>
    <!-- Sidebar -->
    <!-- <v-card>
            <v-btn color="primary" @click.stop="drawer = !drawer"> Toggle </v-btn>
      <v-layout>
        <v-navigation-drawer v-model="drawer" temporary>
          <v-list-item prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg" title="John Leider"></v-list-item>

          <v-divider></v-divider>

          <v-list density="compact" nav>
            <v-list-item prepend-icon="mdi-view-dashboard" title="Home" value="home"></v-list-item>
            <v-list-item prepend-icon="mdi-forum" title="About" value="about"></v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-layout>
    </v-card> -->
    <!-- Navbar -->
    <nav id="main-navbar" class="navbar fixed-top navbar-light bg-dark" v-bind:style="{ 'margin-left': marginLeft }">
      <!-- Container wrapper -->
      <div class="container-fluid">
        <div class="d-flex mb-n1 gap-4 align-items-center">
          <!-- Hamburger button -->
          <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#mobileSidebar" aria-controls="offcanvasExample">
            <span class="hamburger-box">
              <span class="hamburger-inner"></span>
            </span>
          </button>
          <!-- Mobile Offcanvas Sidebar -->
          <div class="offcanvas offcanvas-start text-bg-dark" data-bs-dismiss="offcanvas" tabindex="-1" id="mobileSidebar" aria-labelledby="offcanvasExampleLabel">
            <div class="offcanvas-header">
              <h5 class="offcanvas-title" id="mobileSidebar"><i class="fa-solid fa-house-signal"></i> LufiHome</h5>
            </div>
            <div class="offcanvas-body">
              <Sidebar display="inline" />
            </div>
          </div>

          <!-- Brand -->
          <div class="navbar-brand text-white">
            <span @click="reloadPage" height="25" alt="" loading="lazy">LufiHome</span>
            <v-icon icon="mdi mdi-circle-medium" v-bind:color="socketStatus == true ? 'green' : 'red'"></v-icon>
          </div>
        </div>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-icon @click="next" icon="mdi mdi-account-circle" color="red" v-bind="props"> Activator slot </v-icon>
          </template>
          <v-list>
            <v-list-item v-for="(item, index) in items" :key="index" :value="index">
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <!-- User right icon -->
        <!------------ Edita icon ----------->

        <v-menu min-width="200px" rounded>
          <template v-slot:activator="{ props }"> <v-btn icon="mdi mdi-account" color="primary" size="30" v-bind="props"> </v-btn> </template>
          <v-card>
            <v-card-text>
              <div class="mx-auto text-center">
                <div class="text-h5 font-weight-bold">{{ user.username }}</div>
                <p class="text-caption mt-1">{{ user.role }}</p>
                <v-divider class="my-3"></v-divider>
                <v-btn @click="editaccount" variant="text" rounded> Edit Account </v-btn>
                <v-divider class="my-3"></v-divider>

                <v-btn prepend-icon="mdi mdi-logout" @click="$store.dispatch('auth/logout')" variant="text" color="red" rounded> Logout </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-menu>
      </div>
      <!-- Container wrapper -->
    </nav>
    <!-- Navbar -->
  </header>

  <!-- <v-overlay :model-value="overlay" class="align-center justify-center">
    <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
  </v-overlay> -->
</template>
<!-------------------------------------------------------- Script -------------------------------------------------------->
<script>
import Topbar from "./Topbar.vue";
import Sidebar from "./Sidebar.vue";
import { socket } from "@/socket";
import axios from "axios";
import { mapState } from "vuex";
export default {
  props: ["updateMargin"],
  data() {
    return {
      drawer: null,
      hamburger: "hamburger hamburger--arrow",
      active_hamburger: false,
      itemSidebar: "list-group-item list-group-item-action py-2 ripple",
      width: "85px",
      display: "none",
      marginLeft: "",
      socketStatus: false,
      checkCount: 1,
      overlay: false,
      dialog_setting: false,
    };
  },

  components: {
    Topbar,
    Sidebar,
  },
  mounted() {
    this.checkSocket();
    // this.checkConnection();
  },
  watch: {
    updateMargin: function (marginValue) {
      this.marginLeft = marginValue;
    },
  },
  computed: {
    ...mapState(["auth"]),
    user() {
      return this.auth.user;
    },
    computedVisible: function () {
      return this.display;
    },
  },
  methods: {
    editaccount() {
      this.$router.push("/editaccount");
    },
    getcookie() {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; csrf_access_token=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
    },
    check() {
      console.log(this.getcookie());
    },
    reloadPage() {
      this.$router.push("/").then(() => {
        location.reload();
      });
    },
    checkConnection() {
      setTimeout(() => {
        axios
          .get("http://192.168.0.107:5000/checkConnection")
          .then((response) => {
            if (response.data == true) {
              this.socketStatus = true;
              this.checkConnection();
            } else {
              this.socketStatus = false;
              this.checkConnection();
            }
          })
          .catch((error) => {
            this.socketStatus = false;
            this.checkConnection();
          });
      }, 5000);
    },
    checkSocket() {
      setTimeout(() => {
        this.status();
        if (this.socketStatus == false) {
          this.overlay = true;
          console.log("--- try connect to Socketio for " + this.checkCount + " time ---");
          socket.connect();
          this.checkCount = this.checkCount + 1;
          console.log("--- try connect to Socketio for " + this.checkCount + " time ---");
          if (this.checkCount < 4) {
            this.checkSocket();
          } else {
            this.checkCount = 0;
            this.overlay = false;
            console.log("-- unable to connect Socketio --");
          }
        } else {
          this.checkCount = 0;
          this.overlay = false;
        }
      }, 2000);
    },
    status() {
      this.socketStatus = socket.connected;
    },
    expandSidebar() {
      console.log(this.active_hamburger);
      this.active_hamburger = !this.active_hamburger;

      if (this.active_hamburger) {
        this.$store.commit("events/changeBadgeInline", true);
        this.$emit("changeBody", "220px");
        this.width = "220px";
        this.hamburger = "hamburger hamburger--arrow is-active";
        this.display = "inline";
        this.marginLeft = "220px";
      } else {
        this.$store.commit("events/changeBadgeInline", false);
        this.$emit("changeBody", "85px");
        this.width = "85px";
        this.hamburger = "hamburger hamburger--arrow";
        this.display = "none";
        this.marginLeft = "85px";
      }
    },
  },
};
</script>
<!-------------------------------------------------------- Style -------------------------------------------------------->

<style>
.element.style {
  overflow: auto;
  padding-right: 0 !important;
}
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap");
* {
  font-family: "Poppins", sans-serif;
}
/* --------- Mobile screen --------- */
@media only screen and (max-width: 600px) {
  .navbar {
    margin-left: 0px;
    padding-right: 0 !important;
  }
  .sidebar {
    display: none;
  }
  .navbar-toggler {
    display: inline;
  }
}

/* --------- Big screen --------- */
@media only screen and (min-width: 600px) {
  .navbar {
    margin-left: 85px;
  }
  .sidebar {
    display: inline;
  }
  .navbar-toggler {
    display: none;
  }
}
.offcanvas-header {
  margin-top: 5px;
  margin-left: 32px;
}

.offcanvas {
  --bs-offcanvas-padding-x: 0.4rem;
  --bs-offcanvas-padding-y: 0.6rem;
  --bs-offcanvas-width: 220px;
}
.navbar {
  --bs-navbar-toggler-focus-width: 0rem;
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}
#sidebar a {
  color: #0d6efd;
}
.navbar-brand {
  margin-left: 0px;
}
.fa-house-signal {
  color: rgb(21, 253, 13);
}
.router-link-exact-active {
  background: #0d6efd;
  border-radius: 5px;
  box-shadow: 0 2px 5px 0 rgb(0 0 0 / 16%), 0 2px 10px 0 rgb(0 0 0 / 12%);
}
.list-group {
  --bs-list-group-color: #242424;
  --bs-list-group-bg: #242424;
  --bs-list-group-border-color: #242424;
  --bs-list-group-action-color: var(--bs-secondary-color);
  --bs-list-group-action-hover-color: #0d6efd;
  --bs-list-group-action-hover-bg: #0d6efd;
  --bs-list-group-action-active-color: var(--bs-body-color);
  --bs-list-group-action-active-bg: #0d6efd;
  --bs-list-group-disabled-color: var(--bs-secondary-color);
  --bs-list-group-disabled-bg: var(--bs-body-bg);
  --bs-list-group-active-color: #f7f7f7;
  --bs-list-group-active-bg: #0d6efd;
  --bs-list-group-active-border-color: #0d6efd;
  --bs-list-group-border-radius: 5px;
}

.list-group-item:hover {
  border-radius: 5px;
}

.fas {
  color: #f7f7f7;
}
.itemsidebar {
  /* display: none; */
  color: #f7f7f7;
}

/* Sidebar */
.sidebar {
  background-color: #242424;
  left: 0px;
  position: fixed;
  /* float: left; */
  height: 100vh;
  top: 0;
  bottom: 0;
  left: 0;
  /* box-shadow: 0 2px 5px 0 rgb(0 0 0 / 5%), 0 2px 10px 0 rgb(0 0 0 / 5%); */
  z-index: 600;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
}

.sidebar-sticky {
  position: relative;
  top: 0;
  height: 100vh;
  padding-top: 0;
  overflow-x: hidden;
  overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
}
</style>
