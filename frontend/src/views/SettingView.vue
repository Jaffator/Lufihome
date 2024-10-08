<template>
  <UserCard />
</template>

<script>
import { defineComponent } from 'vue';

// Components
import UserCard from '../components/Setting/UsersCard.vue';

export default defineComponent({
  name: 'HomeView',

  components: {
    UserCard,
  },
});
</script>
