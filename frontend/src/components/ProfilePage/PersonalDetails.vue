<template>
    <div class="fs-4 mt-4 d-flex flex-row border rounded p-3 ps-5 align-items-center gap-5 w-100">
        <div class="d-flex fs-5 gap-4 flex-column align-items-center w-100">
            <div class="position-relative">
                <img v-if="user.profile_picture" style="width: 150px; height:150px; object-fit: cover;" class="rounded-circle" :src="`http://localhost:8000${user.profile_picture}`" alt="Profile Picture">
                <i v-if="!user.profile_picture" class="bi bi-person-circle" style="font-size: 150px; line-height: 0;"></i>
                <button type="button" class="text-danger border-0 bg-transparent position-absolute top-0" style="right: -0.5rem" v-if="user.profile_picture" @click="(event) => { isEditingProfilePicture=true; updateProfile(event); }"><i class="bi bi-x fs-1"></i></button>
            </div>
            <div class="d-flex align-items-center">
                <input class="d-none" type="file" accept=".png" @change="(event) => { isEditingProfilePicture=true; updateProfile(event); }" id="file">
                <label for="file" class="btn btn-primary">Select</label>
                <span v-if="user.profile_picture" class="ms-2 text-success">File Selected</span>
                <span v-if="!user.profile_picture" class="ms-2 text-danger">No File Selected</span>
            </div>
        </div>
        <div class="d-flex flex-column w-100">
            <div class="d-flex">
                <div class="label me-3">Name</div>
                <input class="border border-secondary rounded px-2 me-2" type="text" :disabled="!isEditingName" v-model="name" @input="validateName">
                <button type="button" v-if="!isEditingName"class="btn btn-primary px-2 py-0 d-flex" @click="isEditingName = true"><i class="bi bi-pencil pencil"></i></button>
                <button type="button" :disabled="!validName" v-if="isEditingName"class="btn btn-success" @click="(event) => { updateProfile(event); isEditingName=false; }">Save</button>
                <button type="button" v-if="isEditingName"class="btn btn-danger px-2 py-1 ms-1" @click="name=user.name; errorText.name=''; isEditingName=false;"><i class="bi bi-arrow-counterclockwise fs-5"></i></button>
            </div>
            <div v-if="errorText.name" class="text-danger fs-5">{{ errorText.name }}</div>
            <form class="d-flex mt-3" @submit="validateEmail">
                <div class="label me-3">Email</div>
                <input class="border border-secondary rounded px-2 me-2" type="email" ref="email" :disabled="!isEditingEmail" v-model="email" @input="validEmail=false">
                <button type="button" v-if="!isEditingEmail" class="btn btn-primary px-2 py-0 d-flex" @click="isEditingEmail = true"><i class="bi bi-pencil pencil"></i></button>
                <button type="submit" v-if="isEditingEmail && !validEmail"class="btn btn-secondary">Check</button>
                <button type="submit" v-if="isEditingEmail && validEmail"class="btn btn-success" @click="(event) => { updateProfile(event); isEditingEmail=false; }">Save</button>
                <button type="button" v-if="isEditingEmail"class="btn btn-danger px-2 py-1 ms-1" @click="email=user.email; errorText.email=''; isEditingEmail=false;"><i class="bi bi-arrow-counterclockwise fs-5"></i></button>
            </form>
            <div v-if="errorText.email" class="text-danger fs-5">{{ errorText.email }}</div>
            <div class="d-flex mt-3">
                <div class="label me-3">Password</div>
                <input class="border border-secondary rounded px-2 me-2" type="email" :disabled="!isEditingPassword" :value="user.password">
                <button type="button" v-if="!isEditingPassword" class="btn btn-primary px-2 py-0 d-flex" @click="isEditingPassword = true"><i class="bi bi-pencil pencil"></i></button>
                <button type="button" v-if="isEditingPassword"class="btn btn-success" @click="isEditingPassword = false">Save</button>
            </div>
            <div class="d-flex mt-3 me-3">
                <div class="label">Date of Birth</div>
                <input class="border border-secondary rounded px-2 me-2" type="text" :disabled="!isEditingDateOfBirth" :value="user.date_of_birth">
                <button type="button" v-if="!isEditingDateOfBirth" class="btn btn-primary px-2 py-0 d-flex" @click="isEditingDateOfBirth = !isEditingDateOfBirth"><i class="bi bi-pencil pencil"></i></button>
                <button type="button" v-if="isEditingDateOfBirth"class="btn btn-success" @click="isEditingDateOfBirth = false">Save</button>
            </div>
        </div>
    </div>
  </template>
  
  <script lang="ts">
    import { defineComponent } from "vue";
    import { useUserStore } from "../../stores/user";
    import { CustomUser } from "../../types";
import { useUsersStore } from "../../stores/users";

      
      export default defineComponent({
          data(): {
            errorText: {[key: string]: string}, 
            name: string, 
            validName: boolean, 
            validEmail: boolean, 
            email: string, 
            isEditingName: boolean, 
            isEditingEmail:boolean, 
            isEditingPassword: boolean, 
            isEditingDateOfBirth: boolean, 
            isEditingProfilePicture: boolean} {
              return {
                errorText: {},
                name: '',
                validName: false,
                validEmail: false,
                email: '',
                isEditingName: false,
                isEditingEmail: false,
                isEditingPassword: false,
                isEditingDateOfBirth: false,
                isEditingProfilePicture: false
              }
          },
          methods: {
            validateEmail(event: Event) {
                event.preventDefault()
                const usersStore = useUsersStore()
                if (usersStore.users.filter(userX => userX.id !== this.user.id).map(user => user.email).includes(this.email)) {
                    this.errorText.email = 'Email already exists'
                } else {
                    this.errorText.email = ''
                    this.validEmail = true;
                }
            },
            validateName() {
                if (this.name === '') {
                    this.errorText.name = 'Name cannot be empty'
                } else if (this.name.length > 150) {
                    this.errorText.name = 'Name must be below 151 characters'
                } else if (this.name.match(/^[ ]+.*[ ]*$|[ ]*.*[ ]+$/)) {
                    this.errorText.name = 'Name cannot start or end in space'
                } else if (!this.name.match(/^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$/)) {
                    this.errorText.name = 'Only one space between words'
                } else if (this.name === this.user.name) {
                    this.errorText.name = 'No changes detected'
                } else {
                    this.errorText.name = ''
                    this.validName = true
                    return
                }
                this.validName = false;
            },
            async updateProfile(event: Event) {
                const input: HTMLInputElement = event.target as HTMLInputElement
                if (this.csrf !== '') {
                    let file: FormData = new FormData()
                    let field: string;
                    if (this.isEditingProfilePicture) {
                        if (input && input.files && input.files[0]) { 
                            file.append('profile_picture', input.files[0])
                        } else {
                            file.append('profile_picture', '')
                        }
                        field = 'pic'
                        this.isEditingProfilePicture = false
                    } else if (this.isEditingName) {
                        file.append('name', this.name)
                        field = 'name'
                    } else if (this.isEditingEmail) {
                        file.append('email', this.email)
                        field = 'email'
                    }
                    else {
                        field = ''
                    }
                    let response = await fetch(`http://localhost:8000/api/user/${this.user.id}/${field}/`, {
                        method:'POST', 
                        credentials: 'include', 
                        headers: { 
                            "X-CSRFToken": this.csrf
                        },
                        body: file
                    }) 
                    let data: CustomUser = await response.json()
                    const userStore = useUserStore()
                    userStore.saveUser(data)
                } 
            }
        },
        computed: {
            user(): CustomUser {
                const userStore = useUserStore()
                let user:CustomUser = userStore.user
                this.name = user.name
                this.email = user.email
                return user;
            }, csrf() : string {
                for (let cookie of document.cookie.split(';')) {
                    const csrftoken = cookie.split('=')
                    if (csrftoken[0] === 'csrftoken') {
                        return csrftoken[1]
                    }
                }
                return '';
            },
        }
      })
  </script>
  
<style scoped>
    .pencil {
        font-size: 1.3rem;
    }
</style>
  