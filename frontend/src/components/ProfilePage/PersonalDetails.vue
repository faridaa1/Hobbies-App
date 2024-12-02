<template>
    <div class="fs-4 mt-4 d-flex flex-row border rounded p-3 ps-5 align-items-center gap-5 w-100">
        <div class="d-flex fs-5 gap-4 flex-column align-items-center w-100">
            <div class="position-relative">
                <img v-if="user.profile_picture" style="width: 200px; height:200px; object-fit: cover;" class="rounded-circle" :src="user.profile_picture" alt="Profile Picture">
                <i v-if="!user.profile_picture" class="bi bi-person-circle" style="font-size: 200px; line-height: 0;"></i>
                <button class="text-danger border-0 bg-transparent position-absolute top-0 end-0" v-if="user.profile_picture" @click="user.profile_picture=''"><i class="bi bi-x fs-1"></i></button>
            </div>
            <div class="d-flex align-items-center">
                <input class="w-75 mx-auto" type="file" @change="updateProfilePicture">
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
          data() {
              return {
                  isEditingName: false,
                  isEditingEmail: false,
                  isEditingPassword: false,
                  isEditingDateOfBirth: false
              }
          },
          methods: {
            updateProfilePicture(event: Event) {
                const input: HTMLInputElement = event.target as HTMLInputElement
                if (input && input.files && input.files[0]) {
                    this.user.profile_picture = URL.createObjectURL(input.files[0])
                }
            }
        },
        computed: {
            user(): CustomUser {
                const userStore = useUserStore()
                return userStore.user;
            }
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
  