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
                <button type="button" v-if="!isEditingPassword" class="btn btn-primary px-2 py-0 d-flex" @click="isEditingPassword = true"><i class="bi bi-pencil pencil"></i></button>
            </div>
            <div v-if="isEditingPassword" class="d-flex flex-column gap-3 fs-5">
                <div class="d-flex">
                    <label class="mt-2" style="width: 14rem;">Current Password</label>
                    <input class="border border-secondary rounded px-2 me-2" :type="showOldPassword ? 'text' : 'password'" :disabled="!isEditingPassword" v-model="password.oldPassword" @input="validPassword=false">
                    <button type="button" class="btn btn-warning fs-5 px-2 py-0 d-flex" @click="showOldPassword = !showOldPassword"><i :class="showOldPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i></button>
                </div>
                <div class="d-flex">
                    <label style="width: 14rem;">New Password</label>
                    <input class="border border-secondary rounded px-2 me-2" :type="showNewPassword ? 'text' : 'password'" :disabled="!isEditingPassword" v-model="password.newPassword" @input="validPassword=false">
                    <button type="button" class="btn btn-warning fs-5 px-2 py-0 d-flex" @click="showNewPassword = !showNewPassword"><i :class="showNewPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i></button>
                </div>
                <div class="d-flex">
                    <label style="width: 14rem;">Re-enter New Password</label>
                    <input class="border border-secondary rounded px-2 me-2" :type="showNewPassword2 ? 'text' : 'password'" :disabled="!isEditingPassword" v-model="password.newPassword2" @input="validPassword=false">
                    <button type="button" class="btn btn-warning fs-5 px-2 py-0 d-flex" @click="showNewPassword2 = !showNewPassword2"><i :class="showNewPassword2 ? 'bi bi-eye-slash' : 'bi bi-eye'"></i></button>
                </div>
                <div v-if="errorText.password" class="text-danger fs-5">{{ errorText.password }}</div>
                <div>
                    <button type="button" v-if="isEditingPassword && !validPassword" class="btn btn-secondary" @click="checkPasswords">Check</button>
                    <button type="button" v-if="isEditingPassword && validPassword" :disabled="!validPassword" class="btn btn-success" @click="(event) => { updateProfile(event); password.newPassword =''; password.oldPassword=''; password.newPassword2=''; isEditingPassword = false}">Save</button>
                    <button type="button" class="btn btn-danger px-2 py-1 ms-1" @click="password.newPassword =''; password.oldPassword=''; password.newPassword2=''; errorText.password=''; isEditingPassword=false;"><i class="bi bi-arrow-counterclockwise fs-5"></i></button>
                </div>
            </div>
            <div class="d-flex mt-3 me-3">
                <div class="label me-3">Date of Birth</div>
                <input class="border border-secondary rounded px-2 me-2" type="date" :max="today" v-model="dob" :disabled="!isEditingDateOfBirth">
                <button type="button" v-if="!isEditingDateOfBirth" class="btn btn-primary px-2 py-0 d-flex" @click="isEditingDateOfBirth = !isEditingDateOfBirth"><i class="bi bi-pencil pencil"></i></button>
                <button type="button" v-if="isEditingDateOfBirth" class="btn btn-success" @click="(event) => { updateProfile(event);  isEditingDateOfBirth=false; }">Save</button>
                <button type="button" v-if="isEditingDateOfBirth"class="btn btn-danger px-2 py-1 ms-1" @click="dob=user.date_of_birth; isEditingDateOfBirth=false;"><i class="bi bi-arrow-counterclockwise fs-5"></i></button>
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
        props: { 
            today: { 
                type: String, 
                required: true
            }
        },
        data(): {
            errorText: {[key: string]: string}, 
            name: string, 
            dob: string,
            validName: boolean, 
            validEmail: boolean, 
            email: string, 
            password: {oldPassword: string, newPassword: string, newPassword2: string},
            showOldPassword: boolean,
            showNewPassword: boolean,
            showNewPassword2: boolean,
            validPassword: boolean,
            isEditingName: boolean, 
            isEditingEmail:boolean, 
            isEditingPassword: boolean, 
            isEditingDateOfBirth: boolean, 
            isEditingProfilePicture: boolean } {
            return {
            errorText: {},
            name: '',
            dob: '',
            password: {
                oldPassword: '',
                newPassword: '',
                newPassword2: ''
            },
            validPassword: false,
            validName: true,
            showOldPassword: true,
            showNewPassword: true,
            showNewPassword2: true,
            validEmail: true,
            email: '',
            isEditingName: false,
            isEditingEmail: false,
            isEditingPassword: false,
            isEditingDateOfBirth: false,
            isEditingProfilePicture: false
            }
            },
            methods: {
            async checkPasswords() {
                if (this.password.oldPassword === '') {
                    this.errorText.password = 'Enter current pasword'
                } else if (this.password.newPassword === '') {
                    this.errorText.password = 'Enter new pasword'
                } else if (this.password.newPassword2 === '') {
                    this.errorText.password = 'Re-enter new pasword'
                } else if (this.password.newPassword.length < 8 || this.password.newPassword.length > 30) {
                    this.errorText.password = "New password must be between 8 and 30 characters"
                } else if (this.password.newPassword2.length < 8 || this.password.newPassword2.length > 30) {
                    this.errorText.password = "Re-entered password must be between 8 and 30 characters"
                } else if (this.password.newPassword !== this.password.newPassword2) {
                    this.errorText.password = "New passwords must match"
                } else if (this.password.oldPassword === this.password.newPassword) {
                    this.errorText.password = "Current and New passwords are the same"
                }
                else {
                    let response = await fetch(`http://localhost:8000/api/user/${this.user.id}/checkpass/`, {
                        method:'PUT', 
                        credentials: 'include', 
                        headers: { 
                            "X-CSRFToken": this.csrf
                        },
                        body: JSON.stringify(this.password)
                    }) 
                    const data = await response.json()
                    if (data.match === false) {
                        this.errorText.password = 'Current Password is Incorrect'
                    } else {
                        this.validPassword = true
                        this.errorText.password = ''
                        return
                    }
                }
                this.validPassword = false
            },
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
                } else {
                    this.errorText.name = ''
                    this.validName = true
                    return
                }
                this.validName = false;
            },
            async updateProfile(event: Event) {
                let response;
                if (this.csrf !== '') {
                    const input: HTMLInputElement = event.target as HTMLInputElement
                    let file: FormData = new FormData()
                    let field: string;
                    if (this.isEditingProfilePicture) {
                        console.log(this.user.id)
                        if (input && input.files && input.files[0]) { 
                            file.append('profile_picture', input.files[0])
                        } else {
                            file.append('profile_picture', '')
                        }
                        field = 'pic'
                        response = await fetch(`http://localhost:8000/api/user/${this.user.id}/${field}/`, {
                            method:'POST', 
                            credentials: 'include', 
                            headers: { 
                                "X-CSRFToken": this.csrf
                            },
                            body: file
                        }) 
                        this.isEditingProfilePicture = false
                    } else { 
                        let userInput: BodyInit | {};
                        if (this.isEditingName) {
                            userInput = this.name
                            field = 'name'
                        } else if (this.isEditingEmail) {
                            userInput = this.email
                            field = 'email'
                        } else if (this.isEditingDateOfBirth) {
                            userInput = this.dob
                            field = 'dob'
                        } else {
                            userInput = {
                                oldPassword: this.password.oldPassword,
                                newPassword: this.password.newPassword,
                            }
                            field = 'password'
                            this.validPassword = false;
                        }
                        response = await fetch(`http://localhost:8000/api/user/${this.user.id}/${field}/`, {
                            method:'PUT', 
                            credentials: 'include', 
                            headers: { 
                                "Content-Type": 'application/json',
                                "X-CSRFToken": this.csrf
                            },
                            body: JSON.stringify(userInput)
                        }) 
                    }
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
                this.dob = user.date_of_birth
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
            }
        }
    })
</script>
  
<style scoped>
    .pencil {
        font-size: 1.3rem;
    }
</style>
  