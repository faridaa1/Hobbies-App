<template>
    <div class="fs-4 mt-4 border rounded p-3 ps-5 mb-5 w-100">
        <div class="d-flex justify-content-between">
            <h1>My Hobbies</h1>
            <button
                name = "add_hobby" 
                type="button" 
                class="border-0 bg-transparent text-primary"
                :data-bs-toggle="'modal'"
                :data-bs-target="'#addHobby'"
                >
                <i class="bi bi-plus-circle-fill fs-1 bluebtn d-flex"></i>
            </button>
        </div>
        <hr>
        <div class="text-secondary text-center" v-if="hobbies.length === 0">
            <p>No Hobbies</p>
        </div>
        <div class="modal fade" :id="'addHobby'">
            <div class="modal-dialog">
                <div class="modal-content">
                    <AddHobby :today=today :base_url="base_url" />
                </div>
            </div>
        </div>
        <div class="fs-4 mt-4 d-flex flex-row gap-5 w-100" v-if="hobbies.length" v-for="userHobby in displayedHobbies">
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
            <button name="delete_hobby" class="text-primary border-0 bg-white fs-1" @click="deleteHobby(userHobby)">
                <i class="bi bi-trash-fill darken-hover bluebtn"></i>
            </button>
        </div>
        <div class="mt-4 d-flex gap-2 justify-content-center">
            <button type="button" class="btn btn-secondary" v-if="hobbyIndex > 0" @click="prevPage">Previous</button>
            <button type="button" class="btn btn-secondary" v-if="hobbyIndex+10 < hobbies.length" @click="nextPage">Next</button>
        </div>
    </div>
</template>
  
<script lang="ts">
    import { defineComponent } from "vue";
    import { UserHobby } from "../../types";
    import { useUserStore } from "../../stores/user";
    import AddHobby from "./AddHobby.vue";

    export default defineComponent({
        props: {
            today: {
                type: String,
                required: true
            }, 
            base_url: {
                type: String,
                required: true
            }
        },
        components: { AddHobby },
        data(): {userHobbies: UserHobby[], hobbyIndex: number } {
            return {
                userHobbies: [],
                hobbyIndex: 0
            }
        },
        methods: {
            prevPage() : void {
                this.hobbyIndex -= 10
            },
            nextPage() : void {
                this.hobbyIndex += 10
            },
            async deleteHobby(userHobby: UserHobby): Promise<void> {
                if (useUserStore().csrf !== '') {
                    let response: Response = await fetch(`${this.base_url}/api/user/hobbies/${useUserStore().user.id}&${userHobby.hobby.hobby_id}/`, {
                        method:'DELETE', 
                        credentials: 'include', 
                        headers: { 
                            'Content-Type': 'application/json',
                            "X-CSRFToken": useUserStore().csrf
                        },
                    }) 
                    if (response.ok) {
                        useUserStore().deleteHobby(userHobby)
                        if (this.displayedHobbies.length === 0 && this.hobbies.length !== 0) {
                            this.hobbyIndex -= 10
                        }
                    } else {
                        confirm("Error deleting hobby")
                    }
                }
            }
        },
        computed: {
            hobbies(): UserHobby[] {
                let hobbies: { user_hobbies: UserHobby[] } = useUserStore().hobbies
                if (hobbies && hobbies.user_hobbies) { 
                    return hobbies.user_hobbies
                } else return []
            }, displayedHobbies() : UserHobby[] {
                return this.hobbies.slice(this.hobbyIndex, this.hobbyIndex+10)
            }
        },
    })
</script>
  
<style scoped>
    .bluebtn:hover {
        color: darkblue;
    }
</style>
