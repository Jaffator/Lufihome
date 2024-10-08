<template>
  <!------------ Sensor card ----------->

  <v-container class="pa-1">
    <v-card color="grey-darken-3" elevation="5" max-width="500" class="pa-1">
      <template v-slot:title>
        <v-spacer class="mt-3"></v-spacer>
        <span class="text-subtitle-3 mr-2 pa-0">Sensors</span>
        <v-icon icon="mdi mdi-transit-connection-horizontal" size="35"></v-icon>
      </template>
      <template v-slot:append>
       
       
      </template>
      <!------------ Sensors section ----------->
      <v-container class="pa-1 mt-n3 ml-3">
          <v-row no-gutters>
            <v-col cols="5">
              <text :style="{ color: '#757575' }">Name</text>
            </v-col>
            <v-col cols="5">
              <text :style="{ color: '#757575' }">Type</text>
            </v-col>
            <v-col>
              <text :style="{ color: '#757575' }">State</text>
            </v-col>
          </v-row>
          <v-spacer class="mb-2"></v-spacer>
          <v-row v-for="(sensor, index) in sensorsState" :key="sensor.SensorID" no-gutters class="mt-n1">
              <v-col cols="5">
                    <text class="text-subtitle-1">{{ sensor.Name }}</text>
              </v-col>
              <v-col cols="5">
                    <text class="text-subtitle-2">{{ sensor.Type }}</text>
              </v-col>
              <v-col>
                <v-icon v-if="sensor.Type != 'temp' " icon="mdi mdi-circle-medium" size="35" v-bind:color="sensor.sensorData ? 'green-accent-3' : 'grey-darken-1'"  class="mt-n1 mb-n1"></v-icon>
                <text v-if="sensor.Type == 'temp'" class="text-subtitle-2">{{ sensor.sensorData }}</text>
              </v-col>
          </v-row>
      </v-container>
    </v-card> 
  </v-container>
</template>

<script>
// import axios from "axios";
import { mapState } from "vuex";

export default {
  data() {
    return {
      data: [],
    };
  },
  mounted(){
    this.$store.dispatch("sensors/getSensorsState")
  },
  computed: {
    ...mapState(["sensors"]),
    sensorsState() {
      this.sensorsData = this.sensors.sensorState;
      return this.sensors.sensorState;
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
