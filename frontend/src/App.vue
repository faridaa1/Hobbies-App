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
            <button type="button" class="btn btn-primary ms-5" @click="signout">Sign Out</button>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import { RouterView } from "vue-router";
    import { CustomUser, Hobby, UserHobby } from "./types";
    import { useHobbiesStore } from "./stores/hobbies";
    import { useUserStore } from "./stores/user";
    import { useUsersStore } from "./stores/users";

    export default defineComponent({
        components: { RouterView },
        async mounted(): Promise<void> {
            let userResponse: Response = await fetch("http://localhost:8000/api/user/", {
                method:'GET', 
                credentials: 'include'
            }); 
            let userData: { user: CustomUser } = await userResponse.json();
            let user: CustomUser = userData.user;

            let usersResponse: Response = await fetch("http://localhost:8000/api/users/", {
                method:'GET', 
                credentials: 'include'
            });
            let usersData: { users: CustomUser[] } = await usersResponse.json();
            let users: CustomUser[] = usersData.users;
            useUsersStore().saveUsers(users)

            let hobbiesResponse: Response = await fetch("http://localhost:8000/api/hobbies/", {
                method:'GET', 
                credentials: 'include'
            }); 
            let hobbiesData: { hobbies: Hobby[] } = await hobbiesResponse.json();
            let hobbies: Hobby[] = hobbiesData.hobbies;
            useHobbiesStore().setHobbies(hobbies)
            
            let userHobbies = await fetch(`http://localhost:8000/api/user/hobbies/${user.id}/`, {
                method:'GET', 
                credentials: 'include', 
            }) 
            let userHobbiesResponse: { user_hobbies: UserHobby[] } = await userHobbies.json();
            const userStore = useUserStore()
            userStore.saveUser(user)
            userStore.saveHobbies(userHobbiesResponse)
            
            // extracting csrf token
            for (let cookie of document.cookie.split(';')) {
                const csrftoken: string[] = cookie.split('=')
                if (csrftoken[0] === 'csrftoken') {
                    userStore.csrf = csrftoken[1]
                }
            }
        }, 
        methods: {
            async signout() : Promise<void> {
                let logoutPageResponse: Response = await fetch("http://localhost:8000/logout/", {
                    credentials: 'include', 
                })
                let logoutPage: {'login page' : string} = await logoutPageResponse.json()
                window.location.href = logoutPage["login page"]
            }
        }
    });
</script>

<style scoped>
</style>
