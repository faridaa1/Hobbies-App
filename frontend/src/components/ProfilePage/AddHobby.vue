<template>
    <div class="fs-5">
        <div class="modal-header">
            <h1 class="modal-title fs-5">Add Hobby</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form class="modal-body mb-3 d-flex flex-column">
            <div v-if="hobbySelected" class="d-flex gap-4 mb-4">
                <label class="label">Select a Hobby</label>
                <select class="rounded" v-model="data.newHobby.hobby_id" @input="validate">
                    <option v-for="hobby in filteredHobbies" :key="hobby.hobby_id" :value="hobby.hobby_id">
                        {{ hobby.hobby_name }}
                    </option>   
                </select>
            </div>
            <div v-if="!hobbySelected">
                <div>
                    <label class="label mb-3">Add New Hobby</label>
                    <div class="d-flex mt-3 gap-3">
                        <label>Name <span class="text-danger">*</span></label>
                        <input type="text" @input="validate" v-model="data.newHobby.hobby_name">
                    </div>
                    <p class="text-danger"> {{ errorText.hobby_name }}</p>
                    <div class="d-flex flex-column mt-4 w-75">
                        <label class="mb-2">Description <span class="text-danger">*</span></label>
                        <textarea @input="validate" v-model="data.newHobby.hobby_description"></textarea>
                    </div>
                    <p class="text-danger"> {{ errorText.hobby_description }}</p>
                </div>
        </div>
            <div class="d-flex gap-4 mt-2">
                <label>Level <span class="text-danger">*</span></label>
                <select class="rounded" v-model="data.newUserHobby.level" @input="validate">
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                </select>
            </div>
            <div class="d-flex gap-4 mt-4">
                <label>Start Date <span class="text-danger">*</span></label>
                <input type="date" class="rounded" :max="today" v-model="data.newUserHobby.start_date" @input="validate">
            </div>
            <p class="text-danger"> {{ errorText.start_date }}</p>
            <div class="my-2">
                    <span class="text-danger">*</span> - Required field
                </div>
            <div class="mt-2">
                <button type="button" class="btn btn-secondary" @click="hobbySelected=!hobbySelected">
                    {{ hobbySelected ? 'Add a New Hobby Instead' : 'Select a Hobby Instead' }}
                </button>
            </div>
            <button type="button" class="mt-3 btn btn-primary mx-auto" :disabled="!valid" data-bs-dismiss="modal" @click="submit">Add Hobby</button>
        </form>
    </div>
  </template>
  
  <script lang="ts">
    import { defineComponent } from "vue";
    import { useHobbiesStore } from "../../stores/hobbies";
    import { CustomUser, Hobby, UserHobby } from "../../types";
    import { useUserStore } from "../../stores/user";

    export default defineComponent({
        data(): {
            data: {
                newHobby: Hobby, 
                newUserHobby: UserHobby, 
            }
            hobbySelected: boolean, 
            errorText: {[key: string]: string}, 
            valid: boolean} {
            return {
                hobbySelected: true,
                errorText: {},
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
            validate() {
                // hobby name validation
                if (!this.hobbySelected) {
                    if (!this.data.newHobby.hobby_name || this.data.newHobby.hobby_name.trim().length === 0) {
                        this.errorText.hobby_name = 'Enter a name'
                    } else if (this.data.newHobby.hobby_name.length > 255) {
                        this.errorText.hobby_name = 'Name must be below 255 characters'
                    } else if (this.data.newHobby.hobby_name.match(/^[ ]+.*[ ]*$|[ ]*.*[ ]+$/)) {
                        this.errorText.hobby_name = 'Name cannot start or end in space'
                    } else if (!this.data.newHobby.hobby_name.match(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/)) {
                        this.errorText.hobby_name = 'Only one space between words'
                    } else {
                        this.errorText.hobby_name = ''
                    }

                    // hobby description validation
                    if (!this.data.newHobby.hobby_description || this.data.newHobby.hobby_description.trim().length === 0) {
                        this.errorText.hobby_description = 'Enter a name'
                    } else if (this.data.newHobby.hobby_description.match(/^[ ]+.*[ ]*$|[ ]*.*[ ]+$/)) {
                        this.errorText.hobby_description = 'Description cannot start or end in space'
                    } else if (!this.data.newHobby.hobby_description.match(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/)) {
                        this.errorText.hobby_description = 'Only one space between words'
                    } else {
                        this.errorText.hobby_description = ''
                    }
                }

                // hobby start date validation
                if (this.data.newUserHobby.start_date === undefined || this.data.newUserHobby.start_date === '') {
                    this.errorText.start_date = 'Enter a date'
                } else {
                    this.errorText.start_date = ''
                }

                if (this.errorText.hobby_name === '' && this.errorText.hobby_description === '' && this.errorText.start_date === '') {
                    this.valid = true
                } else if (this.hobbySelected && this.errorText.start_date == '') {
                    this.valid = true

                } else {
                    console.log(this.errorText.hobby_name === '')
                    this.valid = false
                }
            },
            async submit(): Promise<void> {
                if (this.hobbySelected) {
                    const hobby = this.hobbies.find(hobby => hobby.hobby_id === this.data.newHobby.hobby_id)
                    if (hobby) {
                        this.data.newHobby = hobby
                    } else {
                        console.log("Hobby not found")
                    }
                }
                if (this.csrf !== '') {
                    let response = await fetch(`http://localhost:8000/api/user/hobbies/${this.user.id}/`, {
                        method:'POST', 
                        credentials: 'include', 
                        headers: { 
                            'Content-Type': 'application/json',
                            "X-CSRFToken": this.csrf
                        },
                        body: JSON.stringify(this.data),
                    }) 
                    let data = await response.json()
                    let hobby = data.hobby as Hobby
                    const hobbiesStore = useHobbiesStore()
                }
                // // hobbiesStore.addHobby(this.newHobby)
                // const userStore = useUserStore()
                // let user: CustomUser = userStore.user
                // let userHobbies: UserHobby[] = user.hobbies
            }
        },
        computed: {
            user(): CustomUser {
                const userStore = useUserStore()
                let user: CustomUser = userStore.user;
                return user;
            },
            hobbies(): Hobby[] {
                const hobbiesStore = useHobbiesStore()
                return hobbiesStore.hobbies || []
            },
            myHobbies(): Hobby[] {
                const userStore = useUserStore()
                let user: CustomUser = userStore.user;
                let userHobbies: Hobby[] = user.hobbies;
                return userHobbies;
            }, filteredHobbies(): Hobby[] {
                    if (this.hobbies && this.myHobbies) {
                    let hobbiesFiltered = this.hobbies.filter(hobby => !this.myHobbies.some(myHobby => myHobby.hobby_id == hobby.hobby_id))
                    if (hobbiesFiltered.length > 0) {
                        this.data.newHobby.hobby_id = hobbiesFiltered[0].hobby_id
                    }
                    return hobbiesFiltered
                } else {
                    return []
                }
            }, today() : string {
                const today: Date = new Date();
                const year: number = today.getFullYear();
                const month: string = (today.getMonth()+1).toString().padStart(2, '0')
                const day: string = today.getDate().toString().padStart(2, '0')
                return `${year}-${month}-${day}`;
            }, csrf() : string {
                let csrf: string;
                for (let cookie of document.cookie.split(';')) {
                    const csrftoken = cookie.split('=')
                    if (csrftoken[0] === 'csrftoken') {
                        return csrftoken[1]
                    }
                }
                return '';
            }
        },
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
