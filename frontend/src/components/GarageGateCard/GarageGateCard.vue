<template>
  <!------------ Sensor card ----------->
  <Dialog v-model="errorDialog" :dialogtext="errorDialogtext"></Dialog>

  <v-container class="pa-1 mt-n1" fluid style="width: 100%">
    <v-card :loading="loadingStrip" color="grey-darken-3" elevation="5" max-width="500" class="pa-0">
      <template v-slot:title>
        <v-icon class="ml-n1 mt-n2" icon="mdi mdi-garage" size="30"></v-icon>
        <text class="text-subtitle-3 ml-2">Garage gate</text>
      </template>

      <template v-slot:loader="{ isActive }">
        <v-progress-linear :active="isActive" :model-value="progressBar" color="green-accent-3" height="8"></v-progress-linear>
      </template>
      <template v-slot:append>
        <v-dialog v-model="dialog_setting" fullscreen :scrim="false" transition="dialog-bottom-transition">
          <template v-slot:activator="{ props }">
            <v-col><v-btn :disabled="!$store.state.auth.admin" variant="text" v-bind="props" color="grey-darken-1" icon="mdi mdi-cog"></v-btn></v-col>
          </template>
          <GarageGateSetting @closeSetting="CloseSetting()"></GarageGateSetting>
        </v-dialog>
      </template>
      <!------------ Sensors section ----------->
      <v-container class="pa-1 mt-n6">
        <v-row align="center" justify="end" no-gutters>
          <v-col cols="6" align="center">
            <v-btn color="blue-grey-darken-1" class="rounded-pill" size="70" @pointerdown="isHolding = true" @pointerup="isHolding = false">
              <v-icon icon="mdi mdi-gesture-tap-hold" size="32" color=""></v-icon>
            </v-btn>
          </v-col>
          <v-col align="start" cols="1">
            <v-icon class="mt-n2 ml-n7" size="30" :icon="garageIcon" :style="garageText"></v-icon>
          </v-col>
          <v-col align="start" cols="2">
            <text class="ml-n5" :style="garageText">{{ garageState }}</text>
          </v-col>
        </v-row>
      </v-container>
      <v-spacer class="mb-4"></v-spacer>
    </v-card>
    <v-spacer></v-spacer>
  </v-container>
</template>

<script>
let t;
import axios from "axios";
import { mapState } from "vuex";
import GarageGateSetting from "./GarageGateSetting.vue";
import Dialog from "../../components/Dialog.vue";
export default {
  data() {
    return {
      dialogColor: false,
      errorDialogtext: "",
      errorDialog: false,
      data: [],
      isHolding: false,
      loadingStrip: false,
      timer: false,
      garageIcon: "",
      garageText: "",
      dialog_setting: false,
      output: "",
      progressBar: 0,
      interval: null,
      timeout: null,
    };
  },
  components: {
    GarageGateSetting,
    Dialog,
  },
  mounted() {
    this.getGateSetting(["GateSensorUp", "GateSensorDown", "GateState"]);
  },

  methods: {
    ShowErrorDialog(dialogText, color) {
      this.dialogColor = color;
      this.errorDialogtext = dialogText;
      this.errorDialog = true;
    },
    changeGateState(state) {
      if (state == "Open") {
        this.garageIcon = "mdi mdi-garage-alert-variant";
        this.garageText = { color: "#EF5350" };
      }
      if (state == "Opening") {
        this.garageIcon = "mdi mdi-arrow-up-bold";
        this.garageText = { color: "#FDD835" };
      }
      if (state == "Close") {
        this.garageIcon = "mdi mdi-garage-variant-lock";
        this.garageText = { color: "#00E676" };
      }
      if (state == "Closing") {
        this.garageIcon = "mdi mdi-arrow-down-bold";
        this.garageText = { color: "#FDD835" };
      }
    },
    getGateSetting(payload) {
      axios
        .post("/getSetting", payload)
        .then((response) => {
          for (var key in response.data) {
            if (response.data[key].Name == "GateSensorUp") {
              this.$store.commit("sensors/gateSensorUp", response.data[key].Value);
            }
            if (response.data[key].Name == "GateSensorDown") {
              this.$store.commit("sensors/gateSensorDown", response.data[key].Value);
            }
            if (response.data[key].Name == "GateState") {
              this.$store.commit("sensors/updateGateState", response.data[key].Value);
              this.changeGateState(response.data[key].Value);
            }
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error, true);
        });
    },
    CloseSetting() {
      this.dialog_setting = false;
      this.getGateSetting(["GateSensorUp", "GateSensorDown"]);
    },
    openGate() {
      axios
        .get("/gateSwitch")
        .then((response) => {
          if (response.data != true) {
            this.ShowErrorDialog(response.data, true);
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error, true);
        });
    },
    resetProgress() {
      clearInterval(this.interval);
      clearTimeout(this.timeout);
      this.progressBar = 0;
    },
    startTimerPushButton() {
      const intervalDuration = 100; // Update progress every 100 milliseconds
      const steps = 1800 / intervalDuration;
      const stepSize = 100 / steps;

      this.interval = setInterval(() => {
        this.progressBar += stepSize;
        if (this.progressBar >= 100) {
          clearInterval(this.interval);
        }
      }, intervalDuration);

      this.timer = true;
      this.timeout = setTimeout(() => {
        if (this.isHolding == true) {
          clearInterval(this.interval);
          this.openGate();
          window.navigator.vibrate([300, 30, 300]);
        }
        this.timer = false;
        this.loadingStrip = false;
      }, 2000);
    },
  },
  computed: {
    ...mapState(["sensors"]),
    sensorsState() {
      return this.sensors.sensorState;
    },
    sensorUp() {
      var result = this.sensorsState.filter((obj) => obj.SensorID == this.sensors.gateSensorUpID);
      return result[0];
    },
    sensorDown() {
      var result = this.sensorsState.filter((obj) => obj.SensorID == this.sensors.gateSensorDownID);
      return result[0];
    },
    sensorsState() {
      return this.sensors.sensorState;
    },
    button_state() {
      return this.isHolding;
    },
    garageState() {
      return this.sensors.gateStatus;
    },
  },
  watch: {
    garageState(newVal) {
      this.changeGateState(newVal);
    },
    button_state(newVal) {
      if (newVal == true) {
        this.resetProgress();
        this.startTimerPushButton();
        this.loadingStrip = true;
      }
      if (newVal == false) {
        this.resetProgress();
        this.loadingStrip = false;
        clearTimeout(t);
      }
    },
  },
};
</script>
<style>
.v-switch__track {
  background-color: #757575;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}
.v-card-item {
  padding-top: 0px;
  margin-top: -5px;
  margin-right: -15px;
}
.v-enter-from,
.v-leave-to {
  opacity: 0;
}
button.v-btn[disabled] {
  opacity: 0.6;
}
.dialog-bottom-transition-enter-active,
.dialog-bottom-transition-leave-active {
  transition: transform 0.2s ease-in-out;
}
</style>
