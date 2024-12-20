<template>
    <div class="fs-5 mt-4 d-flex flex-row border rounded p-3 ps-5 align-items-center gap-5 w-100">
        <div class="d-flex fs-5 gap-4 flex-column align-items-center w-100">
            <div class="position-relative">
                <img v-if="user.profile_picture" style="width: 200px; height:200px; object-fit: cover;" class="rounded-circle" :src="`http://localhost:8000${user.profile_picture}`">
                <i v-if="!user.profile_picture" class="bi bi-person-circle" style="font-size: 200px; line-height: 0;"></i>
                <button name="remove_profile" type="button" class="text-danger border-0 bg-transparent position-absolute top-0" style="right: -0.5rem" v-if="user.profile_picture" @click="updatePicture($event)"><i class="bi bi-x fs-1"></i></button>
            </div>
            <div class="d-flex align-items-center">
                <input name="profile_pic" class="d-none" type="file" accept=".png" @change="(event) => { isEditingProfilePicture=true; updateProfile(event); }" id="file">
                <label for="file" class="btn btn-primary">Select</label>
                <span v-if="user.profile_picture" class="ms-2 text-success">File Selected</span>
                <span v-if="!user.profile_picture" class="ms-2 text-danger">No File Selected</span>
            </div>
        </div>
        <div class="d-flex flex-column w-100">
            <div class="d-flex flex-column gap-2">
                <label>Full Name</label>
                <div class="d-flex">
                    <input name="name" class="border border-secondary rounded px-2 me-2 w-100" type="text" :disabled="!isEditingName" v-model="name" @input="validateName">
                    <button name="name_edit" type="button" v-if="!isEditingName"class="btn btn-primary p-2" @click="isEditingName=true"><i class="bi bi-pencil d-flex"></i></button>
                    <button name="name_save" type="button" :disabled="!validName" v-if="isEditingName"class="btn btn-success me-1" @click="updateProfile($event)">Save</button>
                    <button type="button" v-if="isEditingName"class="btn btn-danger" @click="reset('name')"><i class="bi bi-arrow-counterclockwise"></i></button>
                </div>
            </div>
            <div v-if="errorText.name" class="text-danger fs-5">{{ errorText.name }}</div>
            <form class="d-flex flex-column gap-2 mt-3" @submit="validateEmail">
                <label>Email</label>
                <div class="d-flex">
                    <input name="email" class="border border-secondary rounded px-2 me-2 w-100" type="email" ref="email" :disabled="!isEditingEmail" v-model="email" @input="validEmail=false">
                    <button name="email_edit" type="button" v-if="!isEditingEmail" class="btn btn-primary p-2" @click="isEditingEmail=true"><i class="bi bi-pencil d-flex"></i></button>
                    <button name="email_check" type="submit" v-if="isEditingEmail && !validEmail" class="btn btn-secondary me-1">Check</button>
                    <button name="email_save" type="button" v-if="isEditingEmail && validEmail" class="btn btn-success me-1" @click="updateProfile($event)">Save</button>
                    <button type="button" v-if="isEditingEmail" class="btn btn-danger" @click="reset('email')"><i class="bi bi-arrow-counterclockwise"></i></button>
                </div>
            </form>
            <div v-if="errorText.email" class="text-danger fs-5">{{ errorText.email }}</div>
            <div class="d-flex mt-3">
                <label class="me-3">Password</label>
                <button name="password_edit" type="button" v-if="!isEditingPassword" class="btn btn-primary p-2" @click="isEditingPassword=true"><i class="bi bi-pencil d-flex"></i></button>
            </div>
            <div v-if="isEditingPassword" class="d-flex flex-column gap-3 mt-2">
                <div class="d-flex flex-column">
                    <label>Current Password</label>
                    <div class="d-flex">
                        <input name="current_password" class="border border-secondary rounded px-2 me-2 w-100" :type="showOldPassword ? 'text' : 'password'" :disabled="!isEditingPassword" v-model="password.oldPassword" @input="validPassword=false">
                        <button name="password_edit" type="button" class="btn btn-warning fs-5 px-2 py-0 d-flex" @click="toggleField('oldpass')"><i :class="showOldPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i></button>
                    </div>
                </div>
                <div class="d-flex flex-column">
                    <label>New Password</label>
                    <div class="d-flex">
                        <input name="new_password" class="border border-secondary rounded px-2 me-2 w-100" :type="showNewPassword ? 'text' : 'password'" :disabled="!isEditingPassword" v-model="password.newPassword" @input="validPassword=false">
                        <button type="button" class="btn btn-warning fs-5 px-2 py-0 d-flex" @click="toggleField('newpass')"><i :class="showNewPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i></button>
                    </div>
                </div>
                <div class="d-flex flex-column">
                    <label>Re-Enter New Password</label>
                    <div class="d-flex">
                        <input name="new_password2" class="border border-secondary rounded px-2 me-2 w-100" :type="showNewPassword2 ? 'text' : 'password'" :disabled="!isEditingPassword" v-model="password.newPassword2" @input="validPassword=false">
                        <button type="button" class="btn btn-warning fs-5 px-2 py-0 d-flex" @click="toggleField('newpass2')"><i :class="showNewPassword2 ? 'bi bi-eye-slash' : 'bi bi-eye'"></i></button>
                    </div>
                </div>
                <div v-if="errorText.password" class="text-danger fs-5">{{ errorText.password }}</div>
                <div>
                    <button name="password_check" type="button" v-if="isEditingPassword && !validPassword" class="btn btn-secondary me-1" @click="checkPasswords">Check</button>
                    <button name="password_save" type="button" v-if="isEditingPassword && validPassword" :disabled="!validPassword" class="btn btn-success me-1" @click="updateProfile($event)">Save</button>
                    <button type="button" class="btn btn-danger" @click="reset('password')"><i class="bi bi-arrow-counterclockwise"></i></button>
                </div>
            </div>
            <div class="d-flex flex-column mt-3 me-3 gap-2 w-100">
                <label class="me-3">Date of Birth</label>
                <div class="d-flex">
                    <input name="dob" class="border border-secondary rounded px-2 me-2 w-100" type="date" :max="today" v-model="dob" :disabled="!isEditingDateOfBirth">
                    <button name="dob_edit" type="button" v-if="!isEditingDateOfBirth" class="btn btn-primary p-2" @click="isEditingDateOfBirth=true"><i class="bi bi-pencil d-flex"></i></button>
                    <button name="dob_save" type="button" v-if="isEditingDateOfBirth" class="btn btn-success me-1" @click="updateProfile($event)">Save</button>
                    <button type="button" v-if="isEditingDateOfBirth"class="btn btn-danger" @click="reset('dob')"><i class="bi bi-arrow-counterclockwise"></i></button>
                </div>
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
            password: { oldPassword: string, newPassword: string, newPassword2: string },
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
                showOldPassword: false,
                showNewPassword: false,
                showNewPassword2: false,
                validEmail: true,
                email: '',
                isEditingName: false,
                isEditingEmail: false,
                isEditingPassword: false,
                isEditingDateOfBirth: false,
                isEditingProfilePicture: false
            }
        }, methods: {
            toggleField(field:string): void {
                if (field === 'oldpass') {
                    this.showOldPassword = !this.showOldPassword
                } else if (field === 'newpass') {
                    this.showNewPassword = !this.showNewPassword
                } else if (field === 'newpass2') {
                    this.showNewPassword2 = !this.showNewPassword2
                } 
            },
            reset(field: string): void {
                if (field === 'name') {
                    this.name = this.user.name; 
                    this.errorText.name = ''; 
                    this.isEditingName = false;
                } else if (field === 'email') {
                    this.email = this.user.email; 
                    this.errorText.email = ''; 
                    this.isEditingEmail = false;
                } else if (field === 'password') {
                    this.password.newPassword =''; 
                    this.password.oldPassword = ''; 
                    this.password.newPassword2 = ''; 
                    this.errorText.password = ''; 
                    this.isEditingPassword=false;
                } else if (field === 'dob') {
                    this.dob = this.user.date_of_birth; 
                    this.isEditingDateOfBirth = false;
                }
            },
            updatePicture(event: Event): void {
                this.isEditingProfilePicture = true
                this.updateProfile(event)
            },
            async checkPasswords(): Promise<void> {
                if (this.password.oldPassword === '' || this.password.newPassword === '' || this.password.newPassword2 === '') {
                    this.errorText.password = 'Fill in all fields.'
                } else if (this.password.newPassword.length < 8 || this.password.newPassword.length > 30 
                    || this.password.newPassword2.length < 8 || this.password.newPassword2.length > 30) {
                    this.errorText.password = "New password must be between 8 and 30 characters"
                } else if (this.password.newPassword !== this.password.newPassword2) {
                    this.errorText.password = "New passwords must match"
                } else if (this.password.oldPassword === this.password.newPassword) {
                    this.errorText.password = "Current and New passwords are the same"
                } else {
                    let response: Response = await fetch(`http://localhost:8000/api/user/${this.user.id}/password/${this.password.oldPassword}`, {
                        method: 'GET', 
                        credentials: 'include', 
                        headers: { 
                            "X-CSRFToken": useUserStore().csrf
                        },
                    }) 
                    const data: { match: boolean } = await response.json()
                    if (data.match === false) {
                        this.errorText.password = 'Current Password is Incorrect'
                    } else {
                        this.validPassword = true
                        this.errorText.password = ''
                        return
                    }
                }
                this.validPassword = false
            }, validateEmail(event: Event): void {
                event.preventDefault()
                if (useUsersStore().users.filter(userX => userX.id !== this.user.id).map(user => user.email).includes(this.email)) {
                    this.errorText.email = 'Email already exists'
                } else {
                    this.errorText.email = ''
                    this.validEmail = true;
                }
            }, validateName(): void {
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
            async updateProfile(event: Event): Promise<void> {
                let response: Response;
                if (useUserStore().csrf !== '') {
                    const input = event.target as HTMLInputElement
                    let file: FormData = new FormData()
                    let field: string;
                    if (this.isEditingProfilePicture) {
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
                                "X-CSRFToken": useUserStore().csrf
                            },
                            body: file
                        }) 
                        this.isEditingProfilePicture = false
                    } else { 
                        let userInput: BodyInit | {};
                        if (this.isEditingName) {
                            userInput = this.name
                            field = 'name'
                            this.isEditingName = false
                        } else if (this.isEditingEmail) {
                            userInput = this.email
                            field = 'email'
                            this.isEditingEmail = false
                        } else if (this.isEditingDateOfBirth) {
                            userInput = this.dob
                            field = 'dob'
                            this.isEditingDateOfBirth = false
                        } else {
                            userInput = {
                                oldPassword: this.password.oldPassword,
                                newPassword: this.password.newPassword,
                            }
                            field = 'password'
                            this.reset('password')
                            this.validPassword = false
                        }
                        response = await fetch(`http://localhost:8000/api/user/${this.user.id}/${field}/`, {
                            method: 'PUT', 
                            credentials: 'include', 
                            headers: { 
                                "Content-Type": 'application/json',
                                "X-CSRFToken": useUserStore().csrf
                            },
                            body: JSON.stringify(userInput)
                        }) 
                    }
                    let data: CustomUser = await response.json()
                    if (Object.keys(data).length === 0) {
                        confirm('Unable to save')
                        this.reset(field)
                        return
                    }
                    useUserStore().saveUser(data)
                    if (field === 'password') {
                        // extracting csrf token
                        for (let cookie of document.cookie.split(';')) {
                            const csrftoken: string[] = cookie.split('=')
                            if (csrftoken[0] === 'csrftoken') {
                                useUserStore().csrf = csrftoken[1]
                            }
                        }
                    }
                } 
            }
        },
        computed: {
            user(): CustomUser {
                let user:CustomUser = useUserStore().user
                this.name = user.name
                this.dob = user.date_of_birth
                this.email = user.email
                return user;
            },
        }
    })
</script>
  
<style scoped>
</style>
  