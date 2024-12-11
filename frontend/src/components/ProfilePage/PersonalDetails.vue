<template>
    <div class="fs-4 mt-4 d-flex flex-row border rounded p-3 ps-5 align-items-center gap-5 w-100">
        <div class="d-flex fs-5 gap-4 flex-column align-items-center w-100">
            <div class="position-relative">
                <img v-if="user.profile_picture" style="width: 150px; height:150px; object-fit: cover;" class="rounded-circle" :src="`http://localhost:8000/${user.profile_picture}`" alt="Profile Picture">
                <i v-if="!user.profile_picture" class="bi bi-person-circle" style="font-size: 150px; line-height: 0;"></i>
                <button type="button" class="text-danger border-0 bg-transparent position-absolute top-0" style="right: -0.5rem" v-if="user.profile_picture" @click="updateProfilePicture"><i class="bi bi-x fs-1"></i></button>
            </div>
            <div class="d-flex align-items-center">
                <input class="d-none" type="file" accept=".png" @change="updateProfilePicture" id="file">
                <label for="file" class="btn btn-primary">Select</label>
                <span v-if="user.profile_picture" class="ms-2 text-success">File Selected</span>
                <span v-if="!user.profile_picture" class="ms-2 text-danger">No File Selected</span>
            </div>
        </div>
        <div class="d-flex flex-column gap-3 w-100">
            <div class="d-flex">
                <div class="label">Full Name</div>
                <input class="border border-secondary rounded px-2" type="text" :disabled="!isEditingName" :value="user.name">
                <button type="button" v-if="!isEditingName"class="button edit" @click="isEditingName = true"><i class="bi bi-pencil"></i></button>
                <button type="button" v-if="isEditingName"class="button save" @click="isEditingName = false">Save</button>
            </div>
            <div class="d-flex">
                <div class="label">Email</div>
                <input class="border border-secondary rounded px-2" type="text" :disabled="!isEditingEmail" :value="user.email">
                <button type="button" v-if="!isEditingEmail" class="button edit" @click="isEditingEmail = true"><i class="bi bi-pencil"></i></button>
                <button type="button" v-if="isEditingEmail"class="button save" @click="isEditingEmail = false">Save</button>
            </div>
            <div class="d-flex">
                <div class="label">Password</div>
                <input class="border border-secondary rounded px-2" type="text" :disabled="!isEditingPassword" :value="user.password">
                <button type="button" v-if="!isEditingPassword" class="button edit" @click="isEditingPassword = true"><i class="bi bi-pencil"></i></button>
                <button type="button" v-if="isEditingPassword"class="button save" @click="isEditingPassword = false">Save</button>
            </div>
            <div class="d-flex">
                <div class="label">Date of Birth</div>
                <input class="border border-secondary rounded px-2" type="text" :disabled="!isEditingDateOfBirth" :value="user.date_of_birth">
                <button type="button" v-if="!isEditingDateOfBirth" class="button edit" @click="isEditingDateOfBirth = !isEditingDateOfBirth"><i class="bi bi-pencil"></i></button>
                <button type="button" v-if="isEditingDateOfBirth"class="button save" @click="isEditingDateOfBirth = false">Save</button>
            </div>
        </div>
    </div>
  </template>
  
  <script lang="ts">
    import { defineComponent } from "vue";
    import { useUserStore } from "../../stores/user";
    import { CustomUser } from "../../types";

      
      export default defineComponent({
          data(): {isEditingName: boolean, isEditingEmail:boolean, isEditingPassword: boolean, isEditingDateOfBirth: boolean} {
              return {
                  isEditingName: false,
                  isEditingEmail: false,
                  isEditingPassword: false,
                  isEditingDateOfBirth: false,
              }
          },
          methods: {
            async updateProfilePicture(event: Event) {
                const input: HTMLInputElement = event.target as HTMLInputElement
                if (this.csrf !== '') {
                    let file: FormData = new FormData()
                    if (input && input.files && input.files[0]) { 
                        file.append('profile_picture', input.files[0])
                    } else {
                        file.append('profile_picture', '')
                    }
                    let response = await fetch(`http://localhost:8000/api/user/${this.user.id}/`, {
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
                console.log(userStore.user.profile_picture)
                return userStore.user;
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
    .button {
        border-radius: 0.25rem; 
        margin-left: 0.5rem; 
        margin-right: 0.5rem;
        color: #ffffff; /* White text */
        border: none; /* Remove border if needed */
    }
    .edit {
        background-color: #007bff;
    }
    .save {
        padding-left: 1rem; 
        padding-right: 1rem;
        background-color: #28a745; 
        cursor: pointer; 
    }
    .label {
        width: 10rem;
    }
</style>
  