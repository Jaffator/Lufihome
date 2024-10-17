<template>
  <!------------ Dialog ----------->
  <Dialog v-model="errorDialog" :dialogtext="errorDialogtext" :color="dialogColor"></Dialog>
  <v-card>
    <v-toolbar dark color="grey-darken-1">
      <v-btn icon dark @click="this.$emit('closeSetting')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-toolbar-title>Alarm settings</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
      <!--  -->
      <!--CARD AREA EDIT------------------------------------------------------------------------------------------------------------------->
      <!--  -->

          <v-container class="pa-1">
          <v-card max-width="550">
            <v-data-table :headers="headers" :items="areas" :sort-by="[{ key: 'AreaName', order: 'asc' }]">
              <template v-slot:top>
                <v-toolbar flat color="indigo-darken-4">
                  <v-icon class="ml-3" icon="mdi mdi-focus-field"></v-icon>
                  <v-toolbar-title>Edit areas</v-toolbar-title>
                  <!--------------- New/Edit item dialog --------------->
                  <v-dialog v-model="dialog" max-width="500px">
                    <template v-slot:activator="{ props }">
                      <v-btn color="grey-lighten-1" @click="newArea()" v-bind="props"> new Area </v-btn>
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="text-h5">{{ formTitle }}</span>
                      </v-card-title>
                      <v-card-text>
                        <v-container class="pa-0">
                          <v-col cols="12" md="8" sm="6">
                            <v-text-field v-model="AreaName" label="Area name"></v-text-field>
                          </v-col>
                          <v-row v-for="(item, index) in sensors" class="mb-n10" no-gutters>
                            <v-col cols="6">
                              <v-checkbox :model-value="item.use" :label="item.Name" @click="useSensor(index)"></v-checkbox>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue-darken-1" variant="text" @click="close"> Cancel </v-btn>
                        <v-btn color="blue-darken-1" variant="text" @click="save()"> Save </v-btn>
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
              <template v-slot:no-data>
                <!-- <v-btn color="primary" @click="initialize"> Reset </v-btn> -->
              </template>
            </v-data-table>
          </v-card>
        </v-container>


          <NightmodeSetting @refreshend="refreshData = false" :refreshNightmode="refreshData"></NightmodeSetting>

          <SensorSetting @sensorRefresh="sensorRefresh()"></SensorSetting>
 
          <OtherSetting></OtherSetting>

          <Outputs></Outputs>
      
   
      
    <!-- <v-spacer></v-spacer> -->
  </v-card>
</template>
<script>
import { mapState } from "vuex";
import Dialog from "../../components/Dialog.vue";
import NightmodeSetting from "../../components/Alarm/NightmodeSetting.vue";
import OtherSetting from "../../components/Alarm/OtherSetting.vue";
import SensorSetting from "../../components/Alarm/SensorSetting.vue";
import Outputs from "../../components/Alarm/Outputs.vue";
import axios from "axios";

export default {
  emits: ["closeSetting"],
  data: () => ({
    dialogColor: false,
    refreshData: false,
    errorDialogtext: "",
    errorDialog: false,
    box: false,
    AreaName: "",
    AreaIDtoDelete: 0,
    formTitle: "",
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        title: "Area name",
        align: "start",
        sortable: false,
        key: "AreaName",
        width: "80%",
      },
      { title: "Actions", key: "actions", sortable: false },
    ],
    areas: [],
    sensors: [],
    areadef: [],
    actualAreaID: 0,
    editedIndex: -1,
  }),
  components: {
    Dialog,
    NightmodeSetting,
    OtherSetting,
    SensorSetting,
    Outputs,
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
    // this.getSensors();
    this.getAreaDef();
    this.getAreas();
  },

  methods: {
    sensorRefresh() {
      this.getAreaDef();
      this.getAreas();
    },
    newArea() {
      this.getSensors();

      this.formTitle = "New Area";
      // this.sensors = JSON.parse(JSON.stringify(this.areadef[item.AreaID]));
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
          for (var key in this.sensors) {
            this.sensors[key].use = false;
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error);
        });
    },
    getAreaDef() {
      axios
        .get("/getAreaDef")
        .then((response) => {
          this.areadef = response.data;
        })
        .catch((error) => {
          this.ShowErrorDialog(error);
        });
    },
    getAreas() {
      axios
        .get("/getAreas")
        .then((response) => {
          this.areas = response.data;
        })
        .catch((error) => {
          this.ShowErrorDialog(error);
        });
    },

    editItem(item) {
      this.actualAreaID = item.AreaID;
      this.AreaName = item.AreaName;
      this.sensors = JSON.parse(JSON.stringify(this.areadef[item.AreaID]));
      this.formTitle = "Edit Area";
      this.dialog = true;
    },
    deleteItem(item) {
      this.AreaIDtoDelete = item.AreaID;
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      axios
        .post("http://192.168.0.107:5000/deleteArea", { AreaID: this.AreaIDtoDelete })
        .then((response) => {
          if (response.data == true) {
            this.getAreaDef();
            this.getAreas();
            this.ShowErrorDialog("Area deleted", true);
            this.refreshData = true;
          } else {
            this.ShowErrorDialog(response.data, false);
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
        });
      this.closeDelete();
    },

    close() {
      this.AreaName = "";
      this.sensors = [];
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
    },

    save() {
      if (this.formTitle == "Edit Area") {
        console.log(this.formTitle);
        axios
          .post("http://192.168.0.107:5000/updateAreaDef", { AreaName: this.AreaName, AreaID: this.actualAreaID, Sensors: this.sensors })
          .then((response) => {
            if (response.data == true) {
              this.getAreas();
              this.getAreaDef();
              this.ShowErrorDialog("Area successfully updated", true);
              this.refreshData = true;
            } else {
              this.ShowErrorDialog(response.data, false);
            }
          })
          .catch((error) => {
            this.ShowErrorDialog(error, false);
          });
      }
      if (this.formTitle == "New Area") {
        axios
          .post("http://192.168.0.107:5000/newAreaDef", { AreaName: this.AreaName, Sensors: this.sensors })
          .then((response) => {
            if (response.data == true) {
              this.getAreas();
              this.getAreaDef();
              this.ShowErrorDialog("New area definition created", true);
              this.refreshData = true;
            } else {
              this.ShowErrorDialog(response.data, false);
            }
          })
          .catch((error) => {
            this.ShowErrorDialog(error, false);
          });
      }
      this.close();
    },
  },
};
</script>
<style>
/* .v-data-table-footer {
  display: None;
} */
</style>
