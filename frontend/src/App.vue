<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css");
</style>
<template>
    <main class="container pt-4">
        <div>
            <router-link
                class=""
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Profile Page'}"
            >
                My Profile
            </router-link>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import { Hobby } from "./types";
import { useHobbiesStore } from "./stores/hobbies";

export default defineComponent({
    components: { RouterView },
    async mounted() {
        let response = await fetch("http://localhost:8000/api/hobbies/");
        let data = await response.json();
        let hobbies = data.hobbies as Hobby[];
        const hobbiesStore = useHobbiesStore()
        hobbiesStore.setHobbies(hobbies)
    }
});

</script>

<style scoped>
</style>
