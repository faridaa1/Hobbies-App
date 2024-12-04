<template>
  <div class="h1">
    {{ title }}
  </div>
  <h1>Current User details: {{ user }}</h1>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUserStore } from "../stores/user";

export default defineComponent({
  data() {
    return {
      title: "Main Page",
    }
  },
  async mounted() {
    const store = useUserStore()
    store.getUser()
  },
  computed: {
    user() {
      const store = useUserStore()
      return store.user
    }
  }
})
</script>

<style scoped></style>
