<style>
    @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css");
</style>
<template>
    <main class="container pt-4">
        <div>
            <router-link :to="{name: 'Main Page'}">
                Main Page
            </router-link>
            |
            <router-link :to="{name: 'Other Page'}">
                Other Page
            </router-link>
            |
            <router-link :to="{name: 'Profile Page'}">
                My Profile
            </router-link>
            <!-- <button type="button" class="btn btn-primary ms-5">Sign Out</button> -->
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
    import { useUsersStore } from "./stores/users";

    export default defineComponent({
        components: { RouterView },
        async mounted() {
            let usersResponse = await fetch("http://localhost:8000/api/users/");
            let usersData = await usersResponse.json();
            let users = usersData.users as CustomUser[];
            useUsersStore().saveUsers(users)

            let hobbiesResponse = await fetch("http://localhost:8000/api/hobbies/");
            let hobbiesData = await hobbiesResponse.json();
            let hobbies = hobbiesData.hobbies as Hobby[];
            const hobbiesStore = useHobbiesStore()
            hobbiesStore.setHobbies(hobbies)

            let userResponse = await fetch("http://localhost:8000/api/user/", {method:'GET', credentials: 'include',}); 
            let userData = await userResponse.json();
            let user = userData.user as CustomUser;
            let userHobbies = await fetch(`http://localhost:8000/api/user/hobbies/${user.id}/`, {
                method:'GET', 
                credentials: 'include', 
            }) 
            let userHobbiesResponse = await userHobbies.json();
            const userStore = useUserStore()
            userStore.saveUser(user)
            userStore.saveHobbies(userHobbiesResponse)
            console.log(document.querySelector("input[name=csrfmiddlewaretoken]").value)
        }
    });
</script>

<style scoped>
</style>
