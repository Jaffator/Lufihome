<template>
  <!------------ Dialog ----------->
  <Dialog v-model="errorDialog" :dialogtext="errorDialogtext" :color="dialogColor"></Dialog>

  <v-container class="pa-1">
    <v-card max-width="550">
      <v-data-table :headers="headers" :items="sensors" items-per-page="5" :sort-by="[{ key: 'DigitalPin', order: 'asc' }]">
        <template v-slot:top>
          <v-toolbar flat color="indigo-darken-4">
            <v-icon class="ml-3" icon="mdi mdi-motion-sensor"></v-icon>
            <v-toolbar-title>Sensors</v-toolbar-title>
            <!--------------- New/Edit item dialog --------------->
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ props }">
                <v-btn color="grey-lighten-1" @click="newSensor" v-bind="props">New sensor </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="text-h5">{{ formTitle }}</span>
                </v-card-title>
                <v-card-text>
                  <v-container class="pa-0">
                    <v-col cols="12" md="8" sm="6">
                      <v-text-field v-model="editedSensor.Name" label="Sensor name"></v-text-field>
                    </v-col>
                    <v-col cols="12" md="8" sm="6">
                      <v-text-field v-model="editedSensor.DigitalPin" type="number" label="Digital pin"></v-text-field>
                    </v-col>
                    <v-col cols="12" md="8" sm="6">
                      <v-select label="Select" v-model="editedSensor.Type" :items="['magnet', 'pir', 'remote alarm ON', 'remote alarm OFF']"></v-select>
                    </v-col>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue-darken-1" variant="text" @click="close"> Cancel </v-btn>
                  <v-btn color="blue-darken-1" variant="text" @click="save(props)"> Save </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <!--------------- Delete dialog --------------->
            <v-dialog v-model="dialogDelete" max-width="500px">
              <v-card>
                <v-card-title class="text-subtitle-2">Are you sure you want to delete this item?</v-card-title>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancel</v-btn>
                  <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">OK</v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon size="small" class="ml-2" @click="editItem(item)"> mdi-pencil </v-icon>
          <v-icon size="small" class="ml-2" @click="deleteItem(item)"> mdi-delete </v-icon>
        </template>
        <template v-slot:footer> </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>
<script>
import { mapState } from "vuex";
import Dialog from "../../components/Dialog.vue";
import axios from "axios";
export default {
  emits: ["sensorRefresh"],
  data: () => ({
    dialogColor: false,
    errorDialogtext: "",
    errorDialog: false,
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        title: "Sensor name",
        align: "start",
        sortable: false,
        key: "Name",
        width: "80%",
      },
      { title: "Type", key: "Type", sortable: false },
      { title: "DIpin", key: "DigitalPin", sortable: false },
      { title: "Actions", key: "actions", sortable: false },
    ],
    sensors: [],
    formTitle: "",
    editedSensor: [],
    SensorIDtoDelete: 0,
  }),
  components: {
    Dialog,
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.getSensors();
    // this.getSensors();
  },

  methods: {
    newSensor() {
      this.formTitle = "New sensor";
    },
    ShowErrorDialog(dialogText, color) {
      this.dialogColor = color;
      this.errorDialogtext = dialogText;
      this.errorDialog = true;
    },
    useSensor(index) {
      this.sensors[index].use = !this.sensors[index].use;
    },
    getSensors() {
      axios
        .get("/getSensors")
        .then((response) => {
          this.sensors = response.data;
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
        });
    },

    editItem(item) {
      this.formTitle = "Edit sensor";
      this.editedSensor = JSON.parse(JSON.stringify(item));
      this.dialog = true;
    },
    deleteItem(item) {
      this.SensorIDtoDelete = item["SensorID"];
      this.dialogDelete = true;
    },
    deleteItemConfirm() {
      axios
        .post("/deleteSensor", { SensorID: this.SensorIDtoDelete })
        .then((response) => {
          if (response.data == true) {
            this.getSensors();
            this.$emit("sensorRefresh");
            this.$store.dispatch("sensors/getSensorsState");
            this.ShowErrorDialog("Sensor deleted", true);
          } else {
            this.ShowErrorDialog(response.data, false);
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
        });
      this.closeDelete();
      console.log("delete");
      this.$store.dispatch("sensors/getSensorsState");
    },

    close() {
      this.editedSensor = [];
      this.dialog = false;
    },

    closeDelete() {
      this.dialogDelete = false;
    },

    save() {
      var payload = JSON;
      if (this.formTitle == "Edit sensor") {
        console.log(this.editedSensor);
        axios
          .post("/updateSensor", this.editedSensor)
          .then((response) => {
            if (response.data == true) {
              this.getSensors();
              this.$emit("sensorRefresh");
              this.$store.dispatch("sensors/getSensorsState");
              // this.ShowErrorDialog("Sensor successfully edited", true);
            } else {
              this.ShowErrorDialog(response.data, false);
            }
          })
          .catch((error) => {
            this.ShowErrorDialog(error, false);
          });
      }
      if (this.formTitle == "New sensor") {
        if (this.editedSensor.hasOwnProperty("Name") == true && this.editedSensor.hasOwnProperty("DigitalPin") == true && this.editedSensor.hasOwnProperty("Type") == true) {
          payload["Name"] = this.editedSensor.Name;
          payload["Type"] = this.editedSensor.Type;
          payload["DigitalPin"] = this.editedSensor.DigitalPin;
          axios
            .post("/newSensor", payload)
            .then((response) => {
              if (response.data == true) {
                this.getSensors();
                this.$emit("sensorRefresh");
                this.$store.dispatch("sensors/getSensorsState");
                // this.ShowErrorDialog("New sensor successfully saved", true);
              } else {
                this.ShowErrorDialog(response.data, false);
              }
            })
            .catch((error) => {
              this.ShowErrorDialog(error, false);
            });
        } else {
          this.ShowErrorDialog("Every field must be filled", false);
        }
      }
      this.close();
    },
  },
};
</script>
<style>
/* .v-data-table-footer {
  display: inline;
} */
</style>
