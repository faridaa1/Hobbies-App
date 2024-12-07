<template>
    <div class="h3">
        {{ title }}
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUserStore } from "../stores/user";

export default defineComponent({
    data() {
        return {
            title: "Other Page",
        }
    },
    async mounted() {
        const store = useUserStore()
        store.getUser()
    },
})
</script>

<style scoped></style>