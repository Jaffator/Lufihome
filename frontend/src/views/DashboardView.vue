<template>
  <!-- Begin Page Content -->
    <AlarmCard />
    <SensorCard/>
    <GarageGateCard/>

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
