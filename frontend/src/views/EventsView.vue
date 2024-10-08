<template>
  <v-container class="pa-1 mt-n1" fluid style="width: 100%">
    <v-card color="grey-darken-3" elevation="5" max-width="500" class="pa-1">
      <v-card-title class="pa-1">Alarm events</v-card-title>
      <v-container class="pa-1" fluid style="margin: 0px; padding: 0px; width: 420px">
        <v-row justify="start" dense>
          <v-col>
            <span class="text-caption">Start date</span>
            <VueDatePicker v-model="startDate" format="dd/MM/yyyy" :teleport="true" position="left"></VueDatePicker>
          </v-col>
          <v-col>
            <span class="text-caption">End date</span>
            <VueDatePicker v-model="endDate" format="dd/MM/yyyy" :teleport="true" position="left"></VueDatePicker>
          </v-col>
          <v-col>
            <v-btn class="mt-6" color="#5865f2" density="default" size="small" @click="getLogsbyDate()">show</v-btn>
          </v-col>
        </v-row>
        <!-- <div>{{ sensorsState }}</div> -->
      </v-container>

      <v-container fluid class="pa-1 mt-2">
        <v-row no-gutters>
          <v-col cols="3">
            <text :style="{ color: '#757575', fontSize: '14px' }">Sensor</text>
          </v-col>
          <v-col cols="3">
            <text :style="{ color: '#757575', fontSize: '14px' }">Area</text>
          </v-col>
          <v-col>
            <text :style="{ color: '#757575', fontSize: '14px' }">Timestamp</text>
          </v-col>
        </v-row>
        <v-spacer class="mb-2"></v-spacer>
        <v-row v-for="(log, index) in alarmLogs" :key="log.AlarmEventID" no-gutters class="mt-n1">
          <v-col cols="3">
            <text class="text-body-2">{{ log.SensorName }}</text>
          </v-col>
          <v-col cols="3">
            <text class="text-body-2">{{ log.AreaName }}</text>
          </v-col>
          <v-col>
            <text class="text-body-2">{{ showFormattedDate(log.TimeStamp) }}</text>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-container>
  <!---------- show snackbar message if new alarm event it's available ---------->
  <div class="text-center ma-2">
    <v-snackbar v-model="snackbar" :timeout="3000" color="deep-purple-accent-4" elevation="24">
      {{ text }}
      <template v-slot:actions>
        <v-btn color="yellow" variant="text" @click="snackbar = false"> Close </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import axios from "axios";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { mapState } from "vuex";
export default {
  components: { VueDatePicker },
  data() {
    return {
      startDate: new Date(),
      endDate: new Date(),
      alarmLogs: [],
      snackbar: false,
      text: ``,
    };
  },
  mounted() {
    let msgcount = this.$store.state.events.alarmEvent["msgcount"];
    if (msgcount != 0) {
      this.endDate = new Date(this.$store.state.events.alarmEvent["latestDate"]);
      this.startDate = new Date(this.$store.state.events.alarmEvent["oldestDate"]);
      this.snackbar = true;
      this.getLogsbyDate();
      this.text = `Showing new ${msgcount} alarm events logs`;
      this.deleteUnreadAlarmMsg();
    } else {
      this.getLogsbyDate();
    }
  },
  computed: {
    ...mapState(["sensors"]),
    sensorsState() {
      return this.sensors.sensorState;
    },
  },
  methods: {
    showFormattedDate(date) {
      return new Date(date).toISOString().replace("T", " ").replace("Z", "").slice(0, -4);
    },
    dateFormat(date) {
      var tzo = -date.getTimezoneOffset(),
        dif = tzo >= 0 ? "+" : "-",
        pad = function (num) {
          return (num < 10 ? "0" : "") + num;
        };
      let offsettime = date.getFullYear() + "-" + pad(date.getMonth() + 1) + "-" + pad(date.getDate());
      // + "T" + pad(date.getHours()) + ":" + pad(date.getMinutes()) + ":" + pad(date.getSeconds() *this line add time
      return offsettime.replace("T", " ");
    },
    async getLogsbyDate() {
      try {
        const response = await axios.post("/system/getLogs", { startdate: this.dateFormat(this.startDate), enddate: this.dateFormat(this.endDate) });
        if (response.status == 200) {
          this.alarmLogs = response.data;
          // console.log(new Date(date).toISOString().replace("T", " ").replace("Z", "").slice(0, -4));
        }
      } catch (error) {
        console.error("something failed", error);
      }
    },
    async deleteUnreadAlarmMsg() {
      try {
        const username = this.$store.state.auth.user["username"];
        const response = await axios.post("/system/deleteUnreadAlarmMsg", { username: username });
        if (response.status == 200) {
          this.$store.commit("events/updateAlarmEvent", { msgcount: 0, latestDate: new Date(), oldestDate: new Date() });
        }
      } catch (error) {
        console.error("something failed", error);
      }
    },
  },
};
</script>
<style>
.v-btn--size-small {
  --v-btn-height: 30px;
}

.dp__input {
  font-size: 12px;
  line-height: 12px;
}
.dp--clear-btn {
  display: none !important;
}
</style>
