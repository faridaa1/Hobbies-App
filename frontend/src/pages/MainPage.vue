<template>
  <div class="h1">
    {{ title }}
  </div>
  <!-- <h1>Current User: {{ user }}</h1> -->
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUserStore } from "../stores/user";

const user = useUserStore();

export default defineComponent({
  data() {
    return {
      title: "Main Page",
    }
  }
})
</script>

<style scoped></style>
