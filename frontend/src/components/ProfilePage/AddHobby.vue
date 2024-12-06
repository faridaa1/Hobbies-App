<template>
    <div class="fs-5">
        <div class="modal-header">
            <h1 class="modal-title fs-5">Add Hobby</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form class="modal-body mb-3 d-flex flex-column">
            <div v-if="hobbySelected" class="d-flex gap-4 mb-4">
                <label class="label">Select Hobby</label>
                <select class="rounded">
                    <option v-for="hobby in hobbies">
                        {{ hobby.hobby_name }}
                    </option>   
                </select>
            </div>
            <div v-if="!hobbySelected">
                <div>
                    <label class="label mb-3">Add New Hobby</label>
                    <div class="d-flex mt-3 gap-3">
                        <label>Name <span class="text-danger">*</span></label>
                        <input type="text" @input="validate" v-model="newHobby.hobby_name">
                    </div>
                    <p class="text-danger"> {{ errorText.hobby_name }}</p>
                    <div class="d-flex flex-column mt-4 w-75">
                        <label>Description <span class="text-danger">*</span></label>
                        <textarea @input="validate" v-model="newHobby.hobby_description"></textarea>
                    </div>
                    <p class="text-danger"> {{ errorText.hobby_description }}</p>
                </div>
                <div class="my-3">
                    <span class="text-danger">*</span> - Required field
                </div>
            </div>
            <div class="mt-2">
                <button type="button" class="btn btn-secondary" @click="hobbySelected=!hobbySelected">
                    {{ hobbySelected ? 'Add New Hobby Instead' : 'Select Hobby Instead' }}
                </button>
            </div>
            <button type="button" class="mt-3 btn btn-primary mx-auto" :disabled="!valid" data-bs-dismiss="modal">Add Hobby</button>
        </form>
    </div>
  </template>
  
  <script lang="ts">
    import { defineComponent } from "vue";
    import { useHobbiesStore } from "../../stores/hobbies";
    import { CustomUser, Hobby, UserHobby } from "../../types";
    import { useUserStore } from "../../stores/user";

    export default defineComponent({
        data(): {newHobby: Hobby, hobbySelected: boolean, errorText: {[key: string]: string}, valid: boolean} {
            return {
                newHobby: {} as Hobby,
                hobbySelected: true,
                errorText: {},
                valid: false
            }
        },
        methods: {
            validate() {
                // hobby name validation
                if (!this.newHobby.hobby_name || this.newHobby.hobby_name.trim().length === 0) {
                    this.errorText.hobby_name = 'Enter a name'
                } else if (this.newHobby.hobby_name.length > 255) {
                    this.errorText.hobby_name = 'Name must be below 255 characters'
                } else if (this.newHobby.hobby_name.match(/^[ ]+.*[ ]*$|[ ]*.*[ ]+$/)) {
                    this.errorText.hobby_name = 'Name cannot start or end in space'
                } else if (!this.newHobby.hobby_name.match(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/)) {
                    this.errorText.hobby_name = 'Only one space between words'
                } else {
                    this.errorText.hobby_name = ''
                }

                // hobby description validation
                if (!this.newHobby.hobby_description || this.newHobby.hobby_description.trim().length === 0) {
                    this.errorText.hobby_description = 'Enter a name'
                } else if (this.newHobby.hobby_description.match(/^[ ]+.*[ ]*$|[ ]*.*[ ]+$/)) {
                    this.errorText.hobby_description = 'Description cannot start or end in space'
                } else if (!this.newHobby.hobby_description.match(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/)) {
                    this.errorText.hobby_description = 'Only one space between words'
                } else {
                    this.errorText.hobby_description = ''
                }

                if (this.errorText.hobby_name === '' && this.errorText.hobby_description === '') {
                    this.valid = true
                } else {
                    this.valid = false
                }
            }
        },
        computed: {
            hobbies(): Hobby[] {
                const hobbiesStore = useHobbiesStore()
                const userStore = useUserStore()
                let user: CustomUser = userStore.user;
                let userHobbies: UserHobby[] = user.hobbies;
                return hobbiesStore.hobbies;
            }
        }
    })
</script>
  
<style scoped>
.label {
    background-color: #007bff; 
    border-radius: 0.25rem; 
    padding-left: 0.8rem; 
    padding-top: 0.3rem;
    padding-bottom: 0.3rem;
    padding-right: 0.8rem; 
    color: white; 
}
</style>
