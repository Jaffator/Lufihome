<template>
  <v-container class="keyboard">
    <v-col>
      <v-row justify="center">
        <v-col cols="5" class="ml-16">
          <v-text-field :bg-color="passColor" v-model="passValue" class="centered-input" variant="outlined" hide-details density="compact" type="password" readonly></v-text-field>
        </v-col>
        <v-col cols="3" class="mt-1">
          <v-progress-circular v-if="checking" indeterminate color="primary"></v-progress-circular>
          <div v-if="showError" class="errorstyle">Error</div>
        </v-col>
      </v-row>
      <v-row>
        <v-col align="center">
          <v-btn @click="pressKey(1)" color="grey-darken-2">1</v-btn>
        </v-col>
        <v-col align="center">
          <v-btn @click="pressKey(2)" color="grey-darken-2">2</v-btn>
        </v-col>
        <v-col align="center">
          <v-btn @click="pressKey(3)" color="grey-darken-2">3</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col align="center">
          <v-btn @click="pressKey(4)" color="grey-darken-2">4</v-btn>
        </v-col>
        <v-col align="center">
          <v-btn @click="pressKey(5)" color="grey-darken-2">5</v-btn>
        </v-col>
        <v-col align="center">
          <v-btn @click="pressKey(6)" color="grey-darken-2">6</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col align="center">
          <v-btn @click="pressKey(7)" color="grey-darken-2">7</v-btn>
        </v-col>
        <v-col align="center">
          <v-btn @click="pressKey(8)" color="grey-darken-2">8</v-btn>
        </v-col>
        <v-col align="center">
          <v-btn @click="pressKey(9)" color="grey-darken-2">9</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col align="center">
          <v-spacer></v-spacer>
        </v-col>
        <v-col align="center">
          <v-btn @click="pressKey(0)" color="grey-darken-2">0</v-btn>
        </v-col>
        <v-col align="center">
          <v-icon @click="deleteValue" class="mt-3" icon="mdi mdi-backspace-outline" color="grey-darken-2" size="40"></v-icon>
        </v-col>
      </v-row>
    </v-col>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      showError: false,
      checking: false,
      passValue: "",
      passColor: "cyan-lighten-5",
    };
  },
  methods: {
    deleteValue() {
      this.showError = false;
      this.passValue = this.passValue.slice(0, -1);
    },
    pressKey(btnVal) {
      if (this.passValue.length < 4) {
        this.passValue = this.passValue + btnVal;
      }
      if (this.passValue.length == 4) {
        this.checkPass();
      }
    },
    checkPass() {
      this.checking = true;
      this.$store.dispatch("alarm/checkAlarmCode", this.passValue).then(
        (response) => {
          this.checking = false;
          console.log(response.data);
          if (response.data) {
            this.passColor = "green-lighten-2";
            this.$store.commit("alarm/HouseAll", false);
            // this.$store.dispatch("alarm/sendUpdateAreas");
            this.$store.dispatch("alarm/disarm");
            this.$store.dispatch("alarm/turnOffSirene");
            this.$store.commit("alarm/changeAlarmState", "disarm");
            this.$emit("showKeyboard");
          } else {
            this.passColor = "red-lighten-3";
            this.wait();
          }
        },
        (error) => {
          this.checking = false;
          this.showError = true;
          console.error(error);
        }
      );
    },
    wait() {
      let timeout;
      timeout = setTimeout(this.clearField, 400);
    },
    clearField() {
      this.passValue = new String();
      this.passColor = "cyan-lighten-5";
    },
  },
  computed: {
    ...mapState(["alarm"]),
    state() {
      return this.alarm.validAlarmCode;
    },
  },
};
</script>

<style scoped>
.errorstyle {
  color: crimson;
}
.v-btn--size-default {
  --v-btn-size: aliceblue;
  --v-btn-height: 60px;
  font-size: var(--v-btn-size);
  min-width: 60px;
  padding: 0 16px;
}
.keyboard {
  width: 300px;
  height: 380px;
}
.centered-input >>> input {
  text-align: center;
}
</style>
