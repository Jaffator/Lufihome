<template>
  <!-- Begin Page Content -->
  <v-container class="pa-0">
    <!-- <v-row no-gutters>
      <v-col cols="3">
        <AlarmCard />
      </v-col >
      <v-col cols="3">
        <SensorCard/>
      </v-col>
      <v-col cols="3">
        <GarageGateCard/>
      </v-col>
    </v-row> -->
    
    <AlarmCard />
    <SensorCard/>
    <GarageGateCard/>


  </v-container>

 






</template>

<script>
import AlarmCard from "../components/Alarm/AlarmCard.vue";
import SensorCard from "../components/SensorCard/SensorCard.vue";
import GarageGateCard from "../components/GarageGateCard/GarageGateCard.vue";

export default {

  components: {
    AlarmCard,
    SensorCard,
    GarageGateCard,
  },
};
</script>


<style>
.offcanvas {
  transition: 0.5s;
}
</style>
