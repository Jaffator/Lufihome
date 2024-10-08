<template>
  <Dialog v-model="errorDialog" :dialogtext="errorDialogtext" :color="dialogColor"></Dialog>
  <v-col cols="12" sm="4">
    <v-container class="pa-1">
      <v-card elevation="5" max-width="500">
        <v-toolbar dark color="indigo-darken-4">
          <v-toolbar-title> <v-icon class="mr-4" icon="mdi mdi-tune-variant"></v-icon>Others</v-toolbar-title>
          <v-btn color="grey-lighten-1" @click="save()"> Save </v-btn>
        </v-toolbar>
        <v-container>
          <v-row>
            <v-col>
              <v-text-field suffix="s" label="Arm time" v-model="armTime" hide-details variant="solo" type="number" prepend-icon="mdi mdi-timer-lock"></v-text-field>
            </v-col>
            <v-col>
              <v-text-field suffix="s" label="Alert time" v-model="alertTime" hide-details variant="solo" type="number" prepend-icon="mdi mdi-timer-lock"></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-container>
  </v-col>
</template>
<script>
import Dialog from "../../components/Dialog.vue";
import axios from "axios";
export default {
  emits: ["closeSetting", "refreshend"],

  data: () => ({
    dialogColor: false,
    armTime: 0,
    alertTime: 0,
    errorDialogtext: "",
    errorDialog: false,
    dialog: false,
    dialogDelete: false,
  }),
  components: {
    Dialog,
  },

  created() {
    this.getAlarmSetting();
  },

  methods: {
    ShowErrorDialog(dialogText, color) {
      this.dialogColor = color;
      this.errorDialogtext = dialogText;
      this.errorDialog = true;
    },
    getAlarmSetting() {
      axios
        .get("/getAlarmSetting")
        .then((response) => {
          console.log(response.data);
          this.armTime = response.data["armtime"];
          this.alertTime = response.data["alerttime"];
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
        });
    },

    save() {
      axios
        .post("/updateAlarmSetting", { armtime: this.armTime, alerttime: this.alertTime })
        .then((response) => {
          if (response.data == true) {
            this.$store.commit("alarm/changeArmTime", this.armTime);
            this.ShowErrorDialog("New arm time saved", true);
          } else {
            this.ShowErrorDialog(response.data, false);
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
        });
    },
  },
};
</script>
<style scoped>
.v-text-field {
  width: 170px;
}
.v-data-table-footer {
  display: None;
}
</style>
