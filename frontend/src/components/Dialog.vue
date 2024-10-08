<template>
  <v-dialog width="auto" :value="value" @input="$emit('input')">
    <v-card class="pa-2" prepend-icon="mdi mdi-check-bold" max-width="600" v-bind:title="dialogtext" v-bind:color="color == false ? 'deep-orange-darken-4' : 'green-lighten-1'">
      <!-- <v-card-text> </v-card-text> -->
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ["value", "dialogtext", "color"],
};
</script>
