<template>
  <!------------ Dialog ----------->
  <Dialog v-model="errorDialog" :dialogtext="errorDialogtext"></Dialog>
  <!------------ Alarm card ----------->
  <!-- <v-btn class="mt-4" color="red-darken-1" variant="text" @click="posttest"> post </v-btn> -->
  <!-- <v-btn class="mt-4" color="red-darken-1" variant="text" @click="gettest"> get </v-btn> -->
  <v-container class="pa-1 mt-n1" fluid style="width: 100%">
    <v-card :loading="loadingStrip" color="grey-darken-3" elevation="5" max-width="500" class="pa-1">
      <template v-slot:title>
        <v-icon
          class="ml-n1"
          v-bind:icon="state == 'armed' ? 'mdi-shield-lock' : 'mdi-shield-lock-open'"
          v-bind:color="state == 'armed' ? 'green-accent-3' : 'red-lighten-1'"
          size="30"
        ></v-icon>
        <span class="text-subtitle-3 ml-2 pa-0">Home Alarm </span>
      </template>
      <template v-slot:loader="{ isActive }">
        <v-progress-linear :active="isActive" color="red-lighten-1" height="5" indeterminate></v-progress-linear>
      </template>
      <template v-slot:append>
        <!------------ Timer ----------->
        <v-col>
          <v-row class="mr-n4">
            <v-col class="mr-n4"
              ><Transition><Timer @TimesUp="TimesUp" v-if="startTimer"></Timer> </Transition
            ></v-col>
            <!------------ Setting icon ----------->
            <v-dialog v-model="dialog_setting" fullscreen :scrim="false" transition="dialog-bottom-transition">
              <template v-show="false" v-slot:activator="{ props }">
                <v-col><v-btn :disabled="!$store.state.auth.admin" variant="text" v-bind="props" color="grey-darken-1" icon="mdi mdi-cog"></v-btn></v-col>
              </template>
              <AlarmSetting @closeSetting="CloseSetting()"></AlarmSetting>
            </v-dialog>
          </v-row>
        </v-col>
      </template>

      <!------------ Arm/Disarm alarm ------------>
      <v-container class="pa-0 mt-n3">
        <v-col>
          <v-row justify="center">
            <v-dialog v-model="dialog" persistent width="auto">
              <template v-slot:activator="{ props }">
                <v-btn :disabled="disableArmButton" color="grey-darken-1" v-if="arm_btn" @click="Arm">Arm</v-btn>
                <v-btn color="red-lighten-1" v-if="stopArming_btn" @click="stopArming">Stop arming </v-btn>
                <v-btn color="grey-darken-1" v-bind="props" v-if="disarm_btn"> Disarm </v-btn>
              </template>
              <v-card color="grey-lighten-3">
                <v-card-text> <Keyboard @showKeyboard="closeDialog" /></v-card-text>
                <v-card-actions>
                  <v-spacer class="ma-8"></v-spacer>
                  <v-btn class="mt-4" color="red-darken-1" variant="text" @click="dialog = false"> Cancel </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </v-col>

        <!------------ All House ----------->
        <v-col>
          <v-container class="pa-1">
            <v-row class="align-center mb-n11">
              <v-col>
                <text class="text-subtitle-1">All House</text>
              </v-col>
              <v-col cols="5" class="text-right mr-1">
                <v-icon icon="mdi mdi-home" v-bind:color="HouseAll_switch ? 'green-accent-3' : 'grey-darken-1'" class="mr-3 mb-1"></v-icon>
              </v-col>
              <v-col cols="1" class="mr-6 pa-1">
                <v-switch
                  :disabled="disabledSwitch"
                  class="mr-n15"
                  color="green-accent-3"
                  v-model="HouseAll_switch"
                  @change="this.$store.commit('alarm/HouseAll', HouseAll_switch)"
                  hide-details
                ></v-switch>
              </v-col>
            </v-row>
            <v-row class="align-center">
              <v-col>
                <text class="text-subtitle-1">Nightmode</text>
              </v-col>
              <v-col cols="5" class="text-right mr-1">
                <v-icon icon="mdi mdi-weather-night" v-bind:color="Nightmode_switch ? 'light-blue-accent-3' : 'grey-darken-1'" class="mr-3 mb-1"></v-icon>
              </v-col>
              <v-col cols="1" class="mr-6 pa-1">
                <v-switch
                  :disabled="disabledSwitch"
                  class="mr-n15"
                  color="green-accent-3"
                  v-model="Nightmode_switch"
                  @change="this.$store.dispatch('alarm/getNightmode', Nightmode_switch)"
                  hide-details
                ></v-switch>
              </v-col>
            </v-row>
          </v-container>
          <!------------ Areas section ----------->
          <v-row v-for="(area, index) in areaData" :key="area.AreaID" cols="12" sm="4">
            <v-container class="pa-1">
              <v-col>
                <v-row class="align-center mb-n15">
                  <v-col>
                    <text class="text-subtitle-1">{{ area.AreaName }}</text>
                  </v-col>
                  <v-col class="text-right">
                    <v-icon v-bind:color="area.Status == 'alert' ? 'red-lighten-1' : area.Status == 'secured' ? 'green-lighten-1' : 'grey-darken-1'" class="mb-1 mr-1">
                      {{ area.Status == "alert" ? "mdi-alert-circle" : area.Status == "secured" ? "mdi-check-circle" : "mdi-close-circle" }}</v-icon
                    >
                    <text :style="area.Status == 'alert' ? { color: '#EF5350' } : area.Status == 'secured' ? { color: '#66BB6A' } : { color: '#757575' }">{{ area.Status }}</text>
                  </v-col>
                  <v-col cols="1" class="mr-6 pa-1">
                    <v-switch
                      :disabled="disabledSwitch"
                      class="mr-n15"
                      color="green-accent-3"
                      @click="$store.commit('alarm/changeAreaStatus', index)"
                      :model-value="area.Switch == true"
                      hide-details
                    ></v-switch>
                  </v-col>
                </v-row>
              </v-col>
            </v-container>
          </v-row>
        </v-col>
      </v-container>
      <v-container> </v-container>
    </v-card>
  </v-container>

  <!-- <v-text-field v-model="text"></v-text-field>
  <v-btn @click="$store.dispatch('alarm/setSetting', { settingName: 'AlarmState', value: text })"> set alert </v-btn>
  <v-btn @click="$store.dispatch('alarm/pushSetting', ['AlarmState'])"> broadcast status </v-btn>
  <v-btn @click="raise"> Raise Alarm </v-btn>
  <v-btn @click="update"> Update </v-btn>
  <v-btn @click="$store.commit('alarm/changeArea')"> changeAreaArray </v-btn>
   <v-btn @click="change"> CHANGE </v-btn>


  <div>{{ state }}</div>
  <div>{{ house }}</div>
  <div>{{ night }}</div>
  <div>{{ areaData }}</div> -->
  <!-- <div>{{ $store.state.auth.user["role"] }}</div> -->
</template>

<script>
import AlarmSetting from "./AlarmSetting.vue";
import Keyboard from "./Keyboard.vue";
import Dialog from "../../components/Dialog.vue";
import Timer from "../../components/Timer.vue";
import axios from "axios";
import { mapState } from "vuex";
export default {
  data() {
    return {
      disabledSwitch: false,
      arm_btn: true,
      stopArming_btn: false,
      disarm_btn: false,
      loadingStrip: false,
      startTimer: false,
      HouseAll_switch: false,
      Nightmode_switch: false,
      dialog_setting: false,
      dialog: false,
      errorDialogtext: "",
      errorDialog: false,
      text: "",
      armButtonText: "arm",
      areas: [],
      disableArmButton: true,
      statusColor: "#81C784",
    };
  },
  components: {
    Timer,
    Keyboard,
    Dialog,
    AlarmSetting,
  },
  // ***
  // ---------------------------------------------------------------- Mounted ----------------------------------------------------------------
  // ***
  mounted() {
    this.$store.dispatch("alarm/getSetting", ["AlarmState", "Nightmode", "AllHouse"]).then(
      (response) => {
        for (var key in response.data) {
          if (response.data[key].Name == "AlarmState") {
            this.$store.commit("alarm/changeAlarmState", response.data[key].Value);
          }
          if (response.data[key].Name == "AllHouse") {
            var status;
            if (response.data[key].Value == 0) {
              status = false;
            } else {
              status = true;
            }
            this.HouseAll_switch = status;
          }
          if (response.data[key].Name == "Nightmode") {
            if (response.data[key].Value == 0) {
              status = false;
            } else {
              status = true;
            }
            this.Nightmode_switch = status;
          }
        }
      },
      (error) => {
        this.$store.commit("alarm/changeAlarmState", "disarm");
        this.ShowErrorDialog(error);
      }
    );
    this.$store.dispatch("alarm/getAreas");
    this.$store.dispatch("alarm/getArmTime");
    this.checkAlarmState_changeUI(this.alarm.alarmState);
  },
  // ***
  // ---------------------------------------------------------------- Methods ----------------------------------------------------------------
  // ***
  methods: {
    async posttest() {
      try {
        const response = await axios.post("/testpost", { number: 1 });
        console.log(response);
      } catch (error) {
        console.log(error);
      }
    },
    gettest() {
      axios
        .get("/testget")
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // ---------- Armed state ----------
    state_armed() {
      this.disabledSwitch = true;
      this.stopArming_btn = false;
      this.arm_btn = false;
      this.disarm_btn = true;
      this.loadingStrip = false;
      this.startTimer = false;
    },
    // ---------- Arming state ----------
    state_arming() {
      this.stopArming_btn = true;
      this.arm_btn = false;
      this.disarm_btn = false;
      this.loadingStrip = true;
      this.startTimer = true;
      this.disabledSwitch = true;
    },
    // ---------- Disarm state ----------
    state_disarm(type) {
      if (type == "onChange") {
        this.$store.commit("alarm/HouseAll", false);
        this.$store.commit("alarm/nightmodeSwitch", false);
        this.disabledSwitch = false;
        this.Nightmode_switch = false;
        this.HouseAll_switch = false;
        this.stopArming_btn = false;
        this.arm_btn = true;
        this.disarm_btn = false;
        this.loadingStrip = false;
        this.startTimer = false;
        this.$store.dispatch("alarm/resetOrigin");
        this.$store
          .dispatch("alarm/setSetting", [
            { settingName: "AlarmState", value: "disarm" },
            { settingName: "AllHouse", value: this.HouseAll_switch },
            { settingName: "Nightmode", value: this.Nightmode_switch },
          ])
          .then((response) => {
            if (response.data == true) {
              this.$store.dispatch("alarm/pushSetting", ["AlarmState", "Nightmode", "AllHouse"]);
            }
          });
      }
      if (type == "check") {
        this.disabledSwitch = false;
        this.Nightmode_switch = false;
        this.HouseAll_switch = false;
        this.stopArming_btn = false;
        this.arm_btn = true;
        this.disarm_btn = false;
        this.loadingStrip = false;
        this.startTimer = false;
      }
    },
    // ---------- Alert state ----------
    state_alert() {
      this.loadingStrip = true;
    },
    checkAlarmState_changeUI(AlarmState) {
      if (AlarmState == "arming") {
        this.state_arming();
      }
      if (AlarmState == "disarm") {
        this.state_disarm("check");
      }
      if (AlarmState == "armed") {
        this.state_armed();
      }
      if (AlarmState == "alert") {
        this.state_alert();
      }
    },

    CloseSetting() {
      this.$store.dispatch("alarm/getAreas");
      this.dialog_setting = false;
    },
    raise() {
      this.$store.dispatch("alarm/setSetting", { settingName: "AlarmState", value: "alert" }).then((response) => {
        this.$store.dispatch("alarm/pushSetting", ["AlarmState"]);
      });
      this.$store.dispatch("alarm/testAlarm");
    },
    stopArming() {
      // this.$store.commit('alarm/changeAlarmState', 'disarm')
      this.$store.dispatch("alarm/startBeeping", false);
      this.$store.dispatch("alarm/disarm");
    },
    Arm() {
      this.$store.dispatch("alarm/startBeeping", true);
      this.$store.dispatch("alarm/setSetting", { settingName: "AlarmState", value: "arming" }).then(
        (response) => {
          if (response.data == true) {
            this.$store.commit("alarm/changeOrigin", true);
            this.$store.commit("alarm/changeAlarmState", "arming");
            this.$store.dispatch("alarm/pushSetting", ["AlarmState"]);
          } else {
            this.ShowErrorDialog(response.data);
          }
        },
        (error) => {
          this.ShowErrorDialog(error);
        }
      );
    },
    ShowErrorDialog(dialogText) {
      this.errorDialogtext = dialogText;
      this.errorDialog = true;
    },
    TimesUp() {
      this.$store.dispatch("alarm/sendUpdateAreas").then(
        (response) => {
          if (response.data.errorstatus) {
            this.$store.commit("alarm/changeAlarmState", "armed");
            this.$store.dispatch("alarm/resetOrigin");
            this.$store
              .dispatch("alarm/setSetting", [
                { settingName: "AllHouse", value: this.HouseAll_switch },
                { settingName: "Nightmode", value: this.Nightmode_switch },
                { settingName: "AlarmState", value: "armed" },
              ])
              .then((response) => {
                this.$store.dispatch("alarm/pushSetting", ["AlarmState", "Nightmode", "AllHouse"]);
              });
          } else {
            this.$store.commit("alarm/changeAlarmState", "disarm");
            this.ShowErrorDialog(response.data.errortext);
          }
        },
        (error) => {
          this.ShowErrorDialog(error);
        }
      );
    },
    change() {
      this.$store.state.alarm.alarmState = this.text;
      this.showArmButton = !this.showArmButton;
    },
    closeDialog() {
      this.dialog = false;
    },
    reserve() {
      this.arming = true;
      setTimeout(() => (this.arming = false), 5000);
    },
  },
  // ***
  // ---------------------------------------------------------------- Computed ----------------------------------------------------------------
  // ***
  computed: {
    getuser() {
      return this.$store.state.auth.user;
    },
    ...mapState(["alarm"]),
    state() {
      return this.alarm.alarmState;
    },
    house() {
      return this.alarm.houseSwitch;
    },
    night() {
      return this.alarm.nightmodeSwitch;
    },
    orig() {
      return this.alarm.origin;
    },
    areaData() {
      this.areas = this.alarm.areaData;
      return this.alarm.areaData;
    },
  },
  // ***
  // ---------------------------------------------------------------- Watch ----------------------------------------------------------------
  // ***
  watch: {
    // look on houseall and nightmode switches for changes
    house(newVal) {
      this.HouseAll_switch = newVal;
    },
    night(newVal) {
      this.Nightmode_switch = newVal;
    },
    areas: {
      // look for areas array and depen on swicth state disable/enable arm button
      handler(newVal) {
        for (var key in newVal) {
          if (newVal[key].Switch) {
            this.disableArmButton = false;
            break;
          } else {
            this.disableArmButton = true;
          }
        }
      },
      deep: true,
    },
    // look on alarm state on change
    state(newVal) {
      if (newVal == "arming") {
        this.state_arming();
      }
      if (newVal == "disarm") {
        this.state_disarm("onChange");
      }
      if (newVal == "armed") {
        this.state_armed();
      }
      if (newVal == "alert") {
        this.state_alert();
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
