<template>
    <div class="fs-4 mt-4 border rounded p-3 ps-5 mb-5 w-100">
        <div class="d-flex justify-content-between">
            <h1>My Hobbies</h1>
            <button 
                type="button" 
                class="border-0 bg-transparent text-primary"
                :data-bs-toggle="'modal'"
                :data-bs-target="'#addHobby'"
                >
                <i class="bi bi-plus-circle-fill fs-1 bluebtn"></i>
            </button>
        </div>
        <div class="modal fade" :id="'addHobby'">
            <div class="modal-dialog">
                <div class="modal-content">
                    <AddHobby />
                </div>
            </div>
        </div>
        <div class="fs-4 mt-4 d-flex flex-row gap-5 w-100" v-if="hobbies.length" v-for="(userHobby, index) in hobbies">
            <div class="d-flex flex-column w-100">
                <div>Name</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ userHobby.hobby.hobby_name }}</div>
            </div>
            <div class="d-flex flex-column w-100">
                <div>Description</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ userHobby.hobby.hobby_description }}</div>
            </div>
            <div class="d-flex flex-column w-100">
                <div>Level</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ userHobby.level }}</div>
            </div>
            <div class="d-flex flex-column w-100">
                <div>Start Date</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ userHobby.start_date }}</div>
            </div>
            <button class="text-primary border-0 bg-white fs-1">
                <i class="bi bi-trash-fill darken-hover bluebtn"></i>
            </button>
        </div>
    </div>
  </template>
  
  <script lang="ts">
    import { defineComponent, toRaw } from "vue";
    import { CustomUser, UserHobby, UserHobbies } from "../../types";
    import { useUserStore } from "../../stores/user";
    import AddHobby from "./AddHobby.vue";

    export default defineComponent({
        components: {
            AddHobby
        },
        data(): {userHobbies: UserHobby[] } {
            return {
                userHobbies: [] as UserHobby[]
            }
        },
        computed: {
            hobbies(): UserHobby[] {
                let hobbies: UserHobbies = useUserStore().hobbies
                return hobbies.user_hobbies || []; 
            }, 
            user(): CustomUser {
                return useUserStore().user;
            }
        },
    })
</script>
  
<style scoped>
    .bluebtn:hover {
        color: darkblue;
    }
</style>
