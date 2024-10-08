<template>
  <!------------ Dialog ----------->
  <Dialog v-model="errorDialog" :dialogtext="errorDialogtext" :color="dialogColor"></Dialog>
  <v-card>
    <v-toolbar dark color="grey-darken-1">
      <v-btn icon dark @click="this.$emit('closeSetting')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-toolbar-title>Gate settings</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-col cols="12" sm="4">
    <v-container class="pa-1">
      <v-card elevation="5" max-width="500">
        <v-toolbar dark color="indigo-darken-4">
          <v-toolbar-title> <v-icon class="mr-4" icon="mdi mdi-tune-variant"></v-icon>I/O</v-toolbar-title>
          <v-btn color="grey-lighten-1" @click="save()"> Save </v-btn>
        </v-toolbar>
        <v-container>
          <v-row align="center" no-gutters>
            <v-col>
              <v-select v-model="sensorDown" :item-props="itemProps" :items="sensorsState" label="Gate sensor Down"></v-select>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col>
              <v-select v-model="sensorUp" :item-props="itemProps" :items="sensorsState" label="Gate sensor Up"></v-select>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-container>
  </v-col>
  </v-card>
</template>
<script>
import { mapState } from "vuex";
import Dialog from "../../components/Dialog.vue";
import axios from "axios";

export default {
  emits: ["closeSetting"],
  data: () => ({
    dialogColor: false,
    refreshData: false,
    errorDialogtext: "",
    errorDialog: false,
    sensorDown: [],
    sensorUp: [],
  }),
  mounted(){
    this.showGateSetting()
  },
  components: {
    Dialog,

  },
  computed: {
    ...mapState(["sensors"]),
    sensorsState() {
      return this.sensors.sensorState;
    },
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete(); 
    },
  },
  methods: {
    showGateSetting(){
      for (var item in this.sensorsState){
            if (this.sensors.gateSensorUpID == this.sensorsState[item].SensorID){
              this.sensorUp = this.sensorsState[item]
            }
            if (this.sensors.gateSensorDownID == this.sensorsState[item].SensorID){
              this.sensorDown = this.sensorsState[item]
            }
          }
    },
    save(){
      axios
          .post("http://192.168.0.107:5000/saveGateSensors", {gateUp: this.sensorUp.SensorID, gateDown: this.sensorDown.SensorID})
          .then((response) => {
            if (response.data == true) {
              this.ShowErrorDialog('Gate sensor saved', true);
              this.$store.commit("sensors/gateSensorUp", this.sensorUp.SensorID)
              this.$store.commit("sensors/gateSensorDown", this.sensorDown.SensorID)
            } else {
              this.ShowErrorDialog(response.data, false);
            }
          })
          .catch((error) => {
            this.ShowErrorDialog(error, false);
          });
    },
    check(){
      console.log(itemProps)
    },
    itemProps (sensorsState) {
        return {
          title: sensorsState.Name,
          subtitle: sensorsState.Type,
        }
    },
    ShowErrorDialog(dialogText, color) {
      this.dialogColor = color;
      this.errorDialogtext = dialogText;
      this.errorDialog = true;
    },
  },
};
</script>
<style>
.v-data-table-footer {
  display: None;
}
</style>
