<template>
  <!------------ Dialog ----------->
  <Dialog v-model="errorDialog" :dialogtext="errorDialogtext" :color="dialogColor"></Dialog>
  <!--CARD AREA EDIT------------------------------------------------------------------------------------------------------------------->
  <!--  -->
    <v-container class="pa-1">
      <v-card max-width="550">
        <v-data-table :headers="headers" :items="outputs" :sort-by="[{ key: 'Name', order: 'asc' }]">
          <template v-slot:top>
            <v-toolbar flat color="indigo-darken-4">
              <v-icon class="ml-3" icon="mdi mdi-export"></v-icon>
              <v-toolbar-title>Outputs</v-toolbar-title>
              <!--------------- New/Edit item dialog --------------->
              <v-dialog v-model="dialog" max-width="500px">
                <template v-slot:activator="{ props }">
                  <v-btn color="grey-lighten-1" @click="newOutput" v-bind="props">New Output</v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>
                  <v-card-text>
                    <v-container class="pa-0">
                      <v-col cols="12" md="8" sm="6">
                        <v-text-field v-model="editedOutput.Name" label="Output name"></v-text-field>
                      </v-col>
                      <v-col cols="12" md="8" sm="6">
                        <v-text-field v-model="editedOutput.DigitalPin" type="number" label="Digital pin"></v-text-field>
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
          <template v-slot:no-data> </template>
        </v-data-table>
      </v-card>
    </v-container>
</template>
<script>
import { mapState } from "vuex";
import Dialog from "../../components/Dialog.vue";
import axios from "axios";
export default {
  data: () => ({
    dialogColor: false,
    errorDialogtext: "",
    errorDialog: false,
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        title: "Output name",
        align: "start",
        sortable: false,
        key: "Name",
        width: "80%",
      },

      { title: "DIpin", key: "DigitalPin", sortable: false },
      { title: "Actions", key: "actions", sortable: false },
    ],
    outputs: [],
    formTitle: "",
    editedOutput: [],
    OutputIDtoDelete: 0,
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
    this.getAlarmOutputs();
    // this.getSensors();
  },

  methods: {
    newOutput() {
      this.formTitle = "New Output";
    },
    ShowErrorDialog(dialogText, color) {
      console.log(color);
      this.dialogColor = color;
      this.errorDialogtext = dialogText;
      this.errorDialog = true;
    },
    useSensor(index) {
      this.outputs[index].use = !this.outputs[index].use;
    },
    getAlarmOutputs() {
      axios
        .get("http://192.168.0.107:5000/getAlarmOutputs")
        .then((response) => {
          this.outputs = response.data;
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
        });
    },

    editItem(item) {
      this.formTitle = "Edit Output";
      this.editedOutput = JSON.parse(JSON.stringify(item));
      this.dialog = true;
    },
    deleteItem(item) {
      this.OutputIDtoDelete = item["OutputID"];
      this.dialogDelete = true;
    },
    deleteItemConfirm() {
      axios
        .post("http://192.168.0.107:5000/deleteAlarmOutput", { OutputID: this.OutputIDtoDelete })
        .then((response) => {
          if (response.data == true) {
            this.getAlarmOutputs();
            this.ShowErrorDialog("Output deleted", true);
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
      this.editedOutput = [];
      this.dialog = false;
    },

    closeDelete() {
      this.dialogDelete = false;
    },

    save() {
      var payload = JSON;
      if (this.formTitle == "Edit Output") {
        console.log(this.editedOutput);
        axios
          .post("http://192.168.0.107:5000/updateAlarmOutput", this.editedOutput)
          .then((response) => {
            if (response.data == true) {
              this.getAlarmOutputs();
              // this.ShowErrorDialog("Output successfully edited", true);
            } else {
              this.ShowErrorDialog(response.data, false);
            }
          })
          .catch((error) => {
            this.ShowErrorDialog(error, false);
          });
      }
      if (this.formTitle == "New Output") {
        console.log("new output");
        if (this.editedOutput.hasOwnProperty("Name") == true && this.editedOutput.hasOwnProperty("DigitalPin") == true) {
          payload["Name"] = this.editedOutput.Name;
          payload["DigitalPin"] = this.editedOutput.DigitalPin;
          axios
            .post("http://192.168.0.107:5000/newAlarmOutput", payload)
            .then((response) => {
              if (response.data == true) {
                this.getAlarmOutputs();
                // this.ShowErrorDialog("New output successfully saved", true);
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
  display: None;
} */
</style>
