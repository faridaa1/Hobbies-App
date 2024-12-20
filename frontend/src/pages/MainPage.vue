<template>
  <div class="h1">
    {{ title }}
  </div>
  <h1>Current User details: {{ user.user }}</h1>
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
  computed: {
    user() {
      const store: ReturnType<typeof useUserStore> = useUserStore()
      return store
    }
  }
})
</script>

<style scoped></style>
