<template>
  <v-img class="mx-auto my-2 mt-15" max-width="50" src="@/assets/logo2.png"></v-img>
  <p class="text-center text-h6 font-weight-medium text-high-emphasis">Lufihome</p>
  <v-container>
    <div :class="{ shake: disabled }">
      <v-slide-y-transition>
        <v-card v-show="show" class="mx-auto pa-7 pb-8" color="white" elevation="5" max-width="448" rounded="lg">
          <div class="text-subtitle-1">Account</div>

          <v-text-field
            v-model="username"
            bg-color="white"
            density="compact"
            placeholder="Enter your username"
            prepend-inner-icon="mdi-email-outline"
            variant="outlined"
          ></v-text-field>

          <div class="text-subtitle-1 d-flex align-center justify-space-between">Password</div>

          <v-text-field
            bg-color="white"
            v-model="password"
            :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
            :type="visible ? 'text' : 'password'"
            density="compact"
            placeholder="Enter your password"
            prepend-inner-icon="mdi-lock-outline"
            variant="outlined"
            @click:append-inner="visible = !visible"
          ></v-text-field>

          <v-btn @click="Login" class="mb-5 mt-5" color="blue" size="large" block>Log In</v-btn>
          <!-- <v-btn @click="Logout" class="mb-5 mt-5" color="red" size="large" variant="tonal" block>Logout</v-btn> -->
          <!-- <v-btn @click="testJWT" class="mb-5 mt-5" color="green" size="large" variant="tonal" block>test JWT 1</v-btn> -->
        </v-card>
      </v-slide-y-transition>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import { authService } from "@/api";
import { mapState } from "vuex";
export default {
  data() {
    return {
      visible: false,
      password: "",
      username: "",
      show: false,
      disabled: false,
    };
  },
  computed: {
    ...mapState(["auth"]),
    user() {
      return this.auth.user;
    },
  },
  methods: {
    loginFailed() {
      this.disabled = true;
      setTimeout(() => {
        this.disabled = false;
      }, 1500);
    },
    async Login() {
      try {
        const response = await authService.post("/auth/login", { username: this.username, password: this.password });
        await new Promise((resolve) => setTimeout(resolve, 200));
        if (response.status == 201) {
          this.$store.commit("auth/setUser", response.data);
          window.location.reload();
        }
      } catch (error) {
        console.error("Login failed", error);
        this.loginFailed();
      }
    },
    async Logout() {
      const response = await authService.post("/auth/logout", {}).catch((error) => {
        console.log(error);
      });
      console.log(response);
      this.$store.dispatch("auth/logout");
    },
    async testJWT() {
      const response = await axios.get("/auth/checktoken", {}).catch((error) => {
        console.log(error);
      });
      console.log(response);
    },
  },
  mounted() {
    this.show = true;
  },
};
</script>
<style>
.shake {
  animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  transform: translate3d(0, 0, 0);
}

@keyframes shake {
  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }

  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%,
  60% {
    transform: translate3d(4px, 0, 0);
  }
}
</style>
