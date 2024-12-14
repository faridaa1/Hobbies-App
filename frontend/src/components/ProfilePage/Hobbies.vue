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
                <i class="bi bi-plus-circle-fill fs-1 bluebtn d-flex"></i>
            </button>
        </div>
        <hr>
        <div class="modal fade" :id="'addHobby'">
            <div class="modal-dialog">
                <div class="modal-content">
                    <AddHobby :today=today />
                </div>
            </div>
        </div>
        <div class="fs-4 mt-4 d-flex flex-row gap-5 w-100" v-if="hobbies.length" v-for="userHobby in hobbies">
            <div class="d-flex gap-1 flex-column w-100">
                <div>Name</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ userHobby.hobby.hobby_name }}</div>
            </div>
            <div class="d-flex gap-1 flex-column w-100">
                <div>Description</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ userHobby.hobby.hobby_description }}</div>
            </div>
            <div class="d-flex gap-1 flex-column w-100">
                <div>Level</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ userHobby.level }}</div>
            </div>
            <div class="d-flex gap-1 flex-column w-100">
                <div>Start Date</div>
                <div class="p-2 rounded w-100" style="background-color: lightgray;">{{ userHobby.start_date }}</div>
            </div>
            <button class="text-primary border-0 bg-white fs-1" @click="deleteHobby(userHobby)">
                <i class="bi bi-trash-fill darken-hover bluebtn"></i>
            </button>
        </div>
    </div>
</template>
  
<script lang="ts">
    import { defineComponent } from "vue";
    import { UserHobby, UserHobbies } from "../../types";
    import { useUserStore } from "../../stores/user";
    import AddHobby from "./AddHobby.vue";

    export default defineComponent({
        props: {
            today: {
                type: String,
                required: true
            }
        },
        components: { AddHobby },
        data(): {userHobbies: UserHobby[] } {
            return {
                userHobbies: [] as UserHobby[]
            }
        },
        methods: {
            async deleteHobby(userHobby: UserHobby) {
                if (useUserStore().csrf !== '') {
                    let response: Response = await fetch(`http://localhost:8000/api/user/hobbies/${useUserStore().user.id}&${userHobby.hobby.hobby_id}/`, {
                        method:'DELETE', 
                        credentials: 'include', 
                        headers: { 
                            'Content-Type': 'application/json',
                            "X-CSRFToken": useUserStore().csrf
                        },
                    }) 
                    if (response.ok) {
                        useUserStore().deleteHobby(userHobby)
                    } else {
                        console.log("Error deleting hobby")
                    }
                }
            }
        },
        computed: {
            hobbies(): UserHobby[] {
                let hobbies: UserHobbies = useUserStore().hobbies
                return hobbies.user_hobbies || []; 
            }
        },
    })
</script>
  
<style scoped>
    .bluebtn:hover {
        color: darkblue;
    }
</style>
