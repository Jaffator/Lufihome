<template>
  <div id="sidebar" class="list-group mx-3 mt-1">
    <router-link class="list-group-item list-group-item-action py-2 ripple" to="/"
      ><v-icon icon="mdi mdi-view-dashboard" color="blue-grey-lighten-5" class="mr-3 mb-1"></v-icon
      ><span class="itemsidebar" v-bind:style="{ display: display }">Dashboard</span></router-link
    >
    <!-- v-bind:inline="changeType"  -->

    <router-link class="list-group-item list-group-item-action py-2 ripple" to="/events"
      ><v-badge v-bind:inline="display == 'inline' ? true : false" color="error" :model-value="itemsCount > 0" :content="itemsCount">
        <v-icon icon="mdi mdi-shield-edit" color="blue-grey-lighten-5" class="mr-2 mb-1"></v-icon>
      </v-badge>
      <span class="itemsidebar" v-bind:style="{ display: display }">Alarm log</span></router-link
    >
    <router-link class="list-group-item list-group-item-action py-2 ripple" to="/templog"
      ><v-icon icon="mdi mdi-thermometer" color="blue-grey-lighten-5" class="mr-3 mb-1"></v-icon
      ><span class="itemsidebar" v-bind:style="{ display: display }">TempLog</span></router-link
    >
    <router-link v-if="$store.state.auth.admin" class="list-group-item list-group-item-action py-2 ripple" to="/setting"
      ><v-icon icon="mdi mdi-cogs" color="blue-grey-lighten-5" class="mr-3 mb-1"></v-icon><span class="itemsidebar" v-bind:style="{ display: display }">Setting</span></router-link
    >
  </div>
</template>

<script>
export default {
  props: ["display"],
  data() {
    return {};
  },
  computed: {
    itemsCount() {
      return this.$store.state.events.alarmEvent["msgcount"];
    },
  },
};
</script>

<style>
/* Ripple effect */
.ripple {
  background-position: center;
  transition: background 0.5s;
}
/* .ripple:hover {
  background: #47a7f5 radial-gradient(circle, transparent 1%, #47a7f5 1%) center/15000%;
} */
.ripple:active {
  background-color: #6eb9f7;
  background-size: 100%;
  transition: background 0s;
}
</style>
