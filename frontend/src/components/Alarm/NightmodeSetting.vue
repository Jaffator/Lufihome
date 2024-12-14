<template>
  <Dialog v-model="errorDialog" :dialogtext="errorDialogtext" :color="dialogColor"></Dialog>
  <v-container class="pa-1">
    <v-card max-width="550">
      <v-data-table :headers="headers" :items="nightmodeAreas" :sort-by="[{ key: 'AreaName', order: 'asc' }]">
        <template v-slot:top>
          <v-toolbar color="indigo-darken-4">
            <v-icon class="ml-3" icon="mdi mdi-weather-night"></v-icon>
            <v-toolbar-title>Nightmode</v-toolbar-title>
            <!--------------- New/Edit item dialog --------------->
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ props }">
                <v-btn color="grey-lighten-1" @click="addNightmode()" v-bind="props"> Add </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="text-h5">{{ formTitle }}</span>
                </v-card-title>
                <v-card-text>
                  <v-container class="pa-0">
                    <v-row v-for="(item, index) in areas" class="mb-n10" no-gutters>
                      <v-col cols="10">
                        <v-checkbox :model-value="item.use" :label="item.AreaName" @click="useArea(index)"></v-checkbox>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue-darken-1" variant="text" @click="close"> Cancel </v-btn>
                  <v-btn color="blue-darken-1" variant="text" @click="save"> Save </v-btn>
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
          <v-icon class="ml-8" size="small" @click="deleteItem(item)"> mdi-delete </v-icon>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>
<script>
import Dialog from "../../components/Dialog.vue";
import axios from "axios";
export default {
  emits: ["closeSetting", "refreshend"],
  props: ["refreshNightmode"],
  data: () => ({
    dialogColor: false,
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
    nightmodeAreas: [],
    actualAreaID: 0,
  }),
  components: {
    Dialog,
  },
  computed: {
    refreshSetting() {
      return this.refreshNightmode;
    },
  },
  watch: {
    refreshSetting(newVal) {
      if (newVal == true) {
        this.getAreas();
        this.getNightmode();
        this.$emit("refreshend");
      }
    },
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    // this.getSensors();
    this.getNightmode();
    this.getAreas();
  },

  methods: {
    useArea(index) {
      this.areas[index].use = !this.areas[index].use;
    },
    addNightmode() {
      var use = false;
      for (var keyArea in this.areas) {
        use = false;
        for (var keyNight in this.nightmodeAreas) {
          if (this.nightmodeAreas[keyNight].AreaID == this.areas[keyArea].AreaID) {
            this.areas[keyArea].use = true;
            use = true;
          }
        }
        if (use == false) {
          this.areas[keyArea].use = false;
        }
      }
    },
    ShowErrorDialog(dialogText, color) {
      this.dialogColor = color;
      this.errorDialogtext = dialogText;
      this.errorDialog = true;
    },
    getNightmode() {
      axios
        .get("/getNightmode")
        .then((response) => {
          this.nightmodeAreas = response.data;
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
        });
    },
    getAreas() {
      axios
        .get("/getAreas")
        .then((response) => {
          this.areas = response.data;
          for (var key in this.areas) {
            this.areas[key].use = false;
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
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
        .post("/deleteNightmodeArea", { AreaID: this.AreaIDtoDelete })
        .then((response) => {
          if (response.data == true) {
            this.getNightmode();
            this.getAreas();
            this.ShowErrorDialog("Deleted", true);
          } else {
            this.ShowErrorDialog(response.data, false);
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error);
        });
      this.closeDelete();
    },
    close() {
      this.dialog = false;
    },
    closeDelete() {
      this.dialogDelete = false;
    },

    save() {
      axios
        .post("/updateNightmode", this.areas)
        .then((response) => {
          if (response.data == true) {
            this.getNightmode();
            this.getAreas();
            this.ShowErrorDialog("Successfully updated", true);
          } else {
            this.ShowErrorDialog(response.data, false);
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
        });

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
