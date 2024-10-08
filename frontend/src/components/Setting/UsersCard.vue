<template>
  <!------------ Dialog ----------->
  <Dialog v-model="errorDialog" :dialogtext="errorDialogtext" :color="dialogColor"></Dialog>
  <!--CARD AREA EDIT------------------------------------------------------------------------------------------------------------------->
  <!--  -->
  <v-container class="pa-1 mt-n1" fluid style="width: 100%">
    <v-card max-width="600" class="text-subtitle-2">
      <v-data-table :headers="headers" :items="users" :sort-by="[{ key: 'UserName', order: 'asc' }]">
        <template v-slot:top>
          <v-toolbar flat color="indigo-darken-4">
            <v-icon class="ml-3" icon="mdi mdi-account-multiple"></v-icon>
            <v-toolbar-title>Users</v-toolbar-title>
            <!--------------- New/Edit item dialog --------------->
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ props }">
                <v-btn color="grey-lighten-1" @click="newUser" v-bind="props">New user</v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="text-h5">{{ formTitle }}</span>
                </v-card-title>
                <v-card-text>
                  <v-container class="pa-0">
                    <v-form v-model="form" @submit.prevent="onSubmit">
                      <!-- user name -->
                      <v-row>
                        <v-text-field :rules="[required]" v-model="editedUser.UserName" label="User name"></v-text-field>
                      </v-row>
                      <!-- email -->
                      <v-row>
                        <v-text-field :rules="[required]" v-model="editedUser.email" label="Email"></v-text-field>
                      </v-row>
                      <!-- passsword -->
                      <v-row>
                        <v-text-field v-if="formTitle == 'New user'" :rules="[required]" type="password" v-model="editedUser.Pass" label="New password"></v-text-field>
                      </v-row>
                      <!-- push bullet token -->
                      <v-row>
                        <v-text-field v-model="editedUser.PushBulletToken" label="PushBulletToken"></v-text-field>
                      </v-row>
                      <!-- account type -->
                      <v-row>
                        <v-select :rules="[required]" label="Account type" v-model="editedUser.AccountType" :items="['user', 'admin']"></v-select>
                      </v-row>
                      <!-- send notifications? -->
                      <v-row>
                        <v-select :rules="[required]" label="Send Notification?" v-model="editedUser.SendMsg" :items="['yes', 'no']"></v-select>
                      </v-row>
                    </v-form>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue-darken-1" variant="text" @click="close"> Cancel </v-btn>
                  <v-btn :disabled="!form" color="blue-darken-1" type="submit" @click="save(props)"> Save </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <!------------ Edit password ---------------->
            <v-dialog v-model="dialogPass" max-width="500px">
              <v-card>
                <v-card-title>
                  <span class="text-h5">{{ formTitle }}</span>
                </v-card-title>
                <v-card-text>
                  <v-container class="pa-0">
                    <!-- passsword -->
                    <v-row>
                      <v-text-field
                        :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append="showPass = !showPass"
                        :type="showPass ? 'text' : 'password'"
                        v-model="newPass"
                        label="New password"
                      ></v-text-field>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue-darken-1" variant="text" @click="closeEditPass"> Cancel </v-btn>
                  <v-btn :disabled="newPass == '' ? true : false" color="blue-darken-1" @click="savePass"> Save </v-btn>
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
          <v-icon size="small" class="mr-3" @click="editItem(item)"> mdi-pencil </v-icon>
          <v-icon size="small" class="mr-3" @click="editPass(item)"> mdi mdi-key-variant </v-icon>
          <v-icon size="small" class="mr-0" @click="deleteItem(item)"> mdi-delete </v-icon>
        </template>
        <template v-slot:item.PushBulletToken="{ value }">
          <v-icon size="small" class="ml-2" :icon="getIcon(value)"></v-icon>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
  <!-- {{ users }} -->
</template>
<script>
import { mapState } from "vuex";
import Dialog from "../../components/Dialog.vue";
import axios from "axios";
export default {
  // emits: ["sensorRefresh"],
  data: () => ({
    newPass: "",
    showPass: false,
    form: false,
    dialogColor: false,
    errorDialogtext: "",
    errorDialog: false,
    dialog: false,
    dialogPass: false,
    dialogDelete: false,
    headers: [
      { title: "User name", align: "start", sortable: false, key: "UserName" },
      { title: "Email", align: "start", key: "email", sortable: false },
      { title: "Use msg", key: "SendMsg", sortable: false },
      { title: "Token msg", key: "PushBulletToken", sortable: false },
      { title: "Actions", key: "actions", sortable: false, width: "120px" },
    ],
    users: [],
    formTitle: "",
    editedUser: JSON,
    editedUserID: 0,
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
    this.getUsers();
  },

  methods: {
    savePass() {
      axios
        .post("/updateUserPass", { UserID: this.editedUserID, NewPass: this.newPass })
        .then((response) => {
          if (response.status == 200) {
            this.ShowErrorDialog(response.data["msg"], true);
          }
        })
        .catch((error) => {
          this.ShowErrorDialog(error.data["msg"], false);
        });
      this.dialogPass = false;
    },
    closeEditPass() {
      this.dialogPass = false;
      this.newPass = "";
    },
    editPass(item) {
      this.editedUserID = item["UserID"];
      this.formTitle = "Edit password";
      this.dialogPass = true;
    },
    onSubmit() {
      if (!this.form) return;
      this.loading = true;
      setTimeout(() => (this.loading = false), 2000);
    },
    required(v) {
      return !!v || "Field is required";
    },
    getIcon(item) {
      if (item.length === 0) {
        return "mdi mdi-cancel";
      } else {
        return "mdi mdi-check";
      }
    },
    newUser() {
      this.formTitle = "New user";
    },
    ShowErrorDialog(dialogText, color) {
      this.dialogColor = color;
      this.errorDialogtext = dialogText;
      this.errorDialog = true;
    },
    getUsers() {
      axios
        .get("/getUsers")
        .then((response) => {
          this.users = response.data;
        })
        .catch((error) => {
          this.ShowErrorDialog(error, false);
        });
    },

    editItem(item) {
      this.formTitle = "Edit user";
      this.editedUser = JSON.parse(JSON.stringify(item));
      this.dialog = true;
    },
    deleteItem(item) {
      this.editedUserID = item["UserID"];
      this.dialogDelete = true;
    },
    deleteItemConfirm() {
      axios
        .post("/deleteUser", { UserID: this.editedUserID })
        .then((response) => {
          if (response.data == true) {
            this.getUsers();
            // this.ShowErrorDialog("New", false);
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
      this.editedUser = [];
      this.dialog = false;
    },

    closeDelete() {
      this.dialogDelete = false;
    },

    save() {
      var payload = JSON;
      if (this.formTitle == "Edit user") {
        axios
          .post("/updateUser", this.editedUser)
          .then((response) => {
            if (response.status == 200) {
              this.getUsers();
              this.ShowErrorDialog(response.data["msg"], true);
            }
          })
          .catch((error) => {
            this.ShowErrorDialog(error, false);
          });
      }
      if (this.formTitle == "New user") {
        if (this.editedUser.PushBulletToken == null) {
          payload["PushBulletToken"] = "";
        } else {
          payload["PushBulletToken"] = this.editedUser.PushBulletToken;
        }
        payload["UserName"] = this.editedUser.UserName;
        payload["Email"] = this.editedUser.email;
        payload["Pass"] = this.editedUser.Pass;
        payload["SendMsg"] = this.editedUser.SendMsg;
        payload["AccountType"] = this.editedUser.AccountType;
        axios
          .post("/newUser", payload)
          .then((response) => {
            if (response.status === 200) {
              this.getUsers();
              this.ShowErrorDialog(response.data["msg"], true);
            }
          })
          .catch((error) => {
            console.log(error);
            this.ShowErrorDialog(error.response.data["msg"], false);
          });
      }
      this.close();
    },
  },
};
</script>
<style>
.v-data-table-footer {
  display: None;
}
</style>
