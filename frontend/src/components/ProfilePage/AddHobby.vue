<template>
    <div class="fs-5">
        <div class="modal-header">
            <h1 class="modal-title fs-5">Add Hobby</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="resetFields"></button>
        </div>
        <form class="modal-body mb-3 d-flex flex-column">
            <label class="label mb-4 text-center bg-primary rounded text-white p-1">{{ hobbySelected ? 'Select Hobby' : 'Add New Hobby' }}</label>
            <div v-if="hobbySelected" class="d-flex flex-column gap-2 mb-3">
                <label>Select Hobby</label>
                <select class="rounded" v-model="data.newHobby.hobby_id" @input="valid = false">
                    <option v-for="hobby in filteredHobbies" :key="hobby.hobby_id" :value="hobby.hobby_id">
                        {{ hobby.hobby_name }}
                    </option>   
                </select>
                <p class="text-danger"> {{ errorText.hobby_name }}</p>
            </div>
            <div v-if="!hobbySelected">
                <div>
                    <div class="d-flex flex-column gap-2">
                        <label>Name <span class="text-danger">*</span></label>
                        <input name="hobby_name" type="text" @input="valid = false" v-model="data.newHobby.hobby_name">
                    </div>
                    <p class="text-danger"> {{ errorText.hobby_name }}</p>
                    <div class="d-flex flex-column gap-2 mt-2">
                        <label>Description <span class="text-danger">*</span></label>
                        <textarea name="hobby_description" @input="valid = false" v-model="data.newHobby.hobby_description"></textarea>
                    </div>
                    <p class="text-danger"> {{ errorText.hobby_description }}</p>
                </div>
        </div>
            <div class="d-flex flex-column gap-2">
                <label>Level <span class="text-danger">*</span></label>
                <select name="level" class="rounded" v-model="data.newUserHobby.level" @input="valid = false">
                    <option value="Beginner">Beginner</option>
                    <option name="level_option" value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                </select>
            </div>
            <div class="d-flex flex-column gap-2 mt-4">
                <label>Start Date <span class="text-danger">*</span></label>
                <input name="hobby_start_date" type="date" class="rounded" :max="today" v-model="data.newUserHobby.start_date" @input="valid = false">
            </div>
            <p class="text-danger"> {{ errorText.start_date }}</p>
            <div class="my-2">
                    <span class="text-danger">*</span> - Required field
                </div>
            <div class="mt-2" v-if="filteredHobbies.length > 1">
                <button type="button" class="btn btn-secondary" @click="updateHobbySelected">
                    {{ hobbySelected ? 'Add a New Hobby Instead' : 'Select a Hobby Instead' }}
                </button>
            </div>
            <button name="check_hobby" v-if="!valid" type="button" class="mt-3 btn btn-warning mx-auto" @click="validate">Check</button>
            <button name="save_hobby" v-if="valid" type="button" class="mt-3 btn btn-primary mx-auto" data-bs-dismiss="modal" @click="submit">Add Hobby</button>
        </form>
    </div>
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import { useHobbiesStore } from "../../stores/hobbies";
    import { CustomUser, Hobby, UserHobby } from "../../types";
    import { useUserStore } from "../../stores/user";

    export default defineComponent({
        props: {
            today: {
                type: String,
                required: true
            }
        },
        data(): {
            data: {
                newHobby: Hobby, 
                newUserHobby: UserHobby, 
            },
            hobbySelected: boolean, 
            errorText: {
                hobby_name: string,
                hobby_description: string,
                start_date: string
            }, 
            valid: boolean 
        }{ return {
                hobbySelected: true,
                errorText: {
                    hobby_name: "",
                    hobby_description: "",
                    start_date: ""
                },
                valid: false,
                data: {
                    newHobby: {} as Hobby,
                    newUserHobby: {
                        level: 'Beginner' // setting default level
                    } as UserHobby,
                }
            }
        },
        methods: {
            updateHobbySelected() : void {
                this.hobbySelected = !this.hobbySelected
                if (!this.hobbySelected) {
                    this.data.newHobby.hobby_description = ""
                    this.data.newHobby.hobby_name = ""
                }
                this.errorText = {
                    hobby_name: "",
                    hobby_description: "",
                    start_date: ""
                }
            },
            resetFields() : void {
                this.errorText = {
                    hobby_name: "",
                    hobby_description: "",
                    start_date: ""
                },
                this.data = {
                    newHobby: {} as Hobby,
                    newUserHobby: {
                        level: 'Beginner'
                    } as UserHobby,
                }
            },
            hobbyExists(): boolean {
                if (this.hobbies.find(hobby => hobby.hobby_name.toLowerCase() === this.data.newHobby.hobby_name.toLowerCase())) {
                    return true
                }
                return false
            },
            validate(): void {
                // hobby name validation
                if (!this.hobbySelected) {
                    if (!this.data.newHobby.hobby_name || this.data.newHobby.hobby_name.trim().length === 0) {
                        this.errorText.hobby_name = 'Enter hobby name'
                    } else if (this.data.newHobby.hobby_name.length > 255) {
                        this.errorText.hobby_name = 'Name must be below 255 characters'
                    } else if (this.data.newHobby.hobby_name.match(/^[ ]+.*[ ]*$|[ ]*.*[ ]+$/)) {
                        this.errorText.hobby_name = 'Name cannot start or end in space'
                    } else if (this.data.newHobby.hobby_name.includes(".")) {
                        this.errorText.hobby_name = 'Name cannot contain a full stop'
                    } else if (this.data.newHobby.hobby_name.match(/[^a-zA-Z0-9 .]/)) {
                        this.errorText.hobby_name = 'No special characters'
                    } else if (!this.data.newHobby.hobby_name.match(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/)) {
                        this.errorText.hobby_name = 'Only one space between words'
                    } else if (this.hobbyExists()) {
                        this.errorText.hobby_name = 'Hobby already exists'
                    } else {
                        this.errorText.hobby_name = ''
                    }

                    // hobby description validation
                    if (!this.data.newHobby.hobby_description || this.data.newHobby.hobby_description.trim().length === 0) {
                        this.errorText.hobby_description = 'Enter a description'
                    } else if (this.data.newHobby.hobby_description.match(/[^a-zA-Z0-9 \.]/)) {
                        this.errorText.hobby_description = 'No special characters'
                    } 
                    else if (!this.data.newHobby.hobby_description.match(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*\.?$/)) {
                        this.errorText.hobby_description = 'Invalid format'
                    } else {
                        this.errorText.hobby_description = ''
                    }
                } else if (this.hobbySelected && Object.keys(this.data.newHobby).length === 0) {
                    this.errorText.hobby_name = 'Select a Hobby'
                } 

                // hobby start date validation
                if (this.data.newUserHobby.start_date === undefined || this.data.newUserHobby.start_date === '') {
                    this.errorText.start_date = 'Enter a date'
                } else {
                    this.errorText.start_date = ''
                }
                
                if (this.errorText.hobby_name === '' && this.errorText.hobby_description === '' && this.errorText.start_date === '' 
                    || this.hobbySelected && this.errorText.start_date === '' ) 
                {
                    this.valid = true
                } else {
                    this.valid = false
                }
            },
            async submit(): Promise<void> {
                if (this.hobbySelected) {
                    const hobby: Hobby | undefined = this.hobbies.find(hobby => hobby.hobby_id === this.data.newHobby.hobby_id)
                    if (hobby) {
                        this.data.newHobby = hobby
                    } else {
                        confirm("Hobby not found")
                    }
                } else {
                    this.data.newHobby.hobby_id = -1
                }
                if (useUserStore().csrf !== '') {
                    let response: Response = await fetch(`http://localhost:8000/api/user/hobbies/${this.user.id}/`, {
                        method:'POST', 
                        credentials: 'include', 
                        headers: { 
                            'Content-Type': 'application/json',
                            "X-CSRFToken": useUserStore().csrf
                        },
                        body: JSON.stringify(this.data),
                    }) 
                    let userHobby: {user_hobbies: UserHobby} = await response.json()
                    if (Object.keys(userHobby.user_hobbies).length === 0) {
                        window.confirm('Failed to make changes')
                        return
                    }
                    if (this.data.newHobby.hobby_id === -1) {
                        // update with recently added hobby
                        useHobbiesStore().addHobby(userHobby.user_hobbies.hobby)
                    } 
                    useUserStore().addHobby(userHobby.user_hobbies)

                    // resetting values
                    this.data = {
                        newHobby: {} as Hobby,
                        newUserHobby: {
                            level: 'Beginner' 
                        } as UserHobby,
                    }
                }
                this.valid = false
            }
        },
        computed: {
            user(): CustomUser {
                return useUserStore().user;
            },
            hobbies(): Hobby[] {
                return useHobbiesStore().hobbies
            },
            myHobbies(): UserHobby[] {
                return useUserStore().hobbies.user_hobbies;
            }, 
            filteredHobbies(): Hobby[] {
                if (this.hobbies && this.myHobbies) {
                    let hobbiesFiltered: Hobby[] = this.hobbies.filter(hobby => !this.myHobbies.some(myHobby => myHobby.hobby.hobby_id === hobby.hobby_id))
                    if (hobbiesFiltered.length > 0) {
                        this.data.newHobby.hobby_id = hobbiesFiltered[0].hobby_id
                    }
                    return hobbiesFiltered
                } 
                return []
            }
        },
        watch: {
            filteredHobbies(newHobbies): void {
                this.hobbySelected = newHobbies.length > 1
            }
        }
    })
</script>
  
<style scoped>
</style>
