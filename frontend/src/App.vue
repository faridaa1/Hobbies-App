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
import { CustomUser, Hobby } from "./types";
import { useHobbiesStore } from "./stores/hobbies";
import { useUserStore } from "./stores/user";

export default defineComponent({
    components: { RouterView },
    async mounted() {
        let hobbiesResponse = await fetch("http://localhost:8000/api/hobbies/");
        let hobbiesData = await hobbiesResponse.json();
        let hobbies = hobbiesData.hobbies as Hobby[];
        const hobbiesStore = useHobbiesStore()
        hobbiesStore.setHobbies(hobbies)

        let userResponse = await fetch("http://localhost:8000/api/user/");
        let userData = await userResponse.json();
        let user = userData.hobbies as CustomUser;
        const userStore = useUserStore()
        userStore.saveUser(user)
    }
});

</script>

<style scoped>
</style>
