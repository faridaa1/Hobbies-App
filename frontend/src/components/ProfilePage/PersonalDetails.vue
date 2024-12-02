<template>
    <div class="fs-4 mt-4 d-flex flex-row border rounded p-3 ps-5 align-items-center gap-5 w-100">
        <div class="d-flex fs-5 gap-4 flex-column align-items-center w-100">
            <div class="position-relative">
                <img v-if="user.profile_picture" style="width: 200px; height:200px; object-fit: cover;" class="rounded-circle" :src="user.profile_picture" alt="">
                <i v-if="!user.profile_picture" class="bi bi-person-circle" style="font-size: 200px; line-height: 0;"></i>
                <button class="text-danger border-0 bg-transparent position-absolute top-0 end-0" v-if="user.profile_picture" @click="user.profile_picture=''"><i class="bi bi-x fs-1"></i></button>
            </div>
            <div class="d-flex align-items-center">
                <input class="w-75 mx-auto" type="file" @change="updateProfilePicture">
            </div>
        </div>
        <div class="d-flex flex-column gap-3 w-100">
            <div class="d-flex">
                <div style="width: 10rem;">Full Name</div>
                <input class="border border-secondary rounded px-2" type="text" :disabled="!isEditingName" :value="user.name">
                <button v-if="!isEditingName"class="rounded mx-2 border-primary bg-primary text-white" @click="isEditingName = true"><i class="bi bi-pencil"></i></button>
                <button v-if="isEditingName"class="rounded mx-2 px-3 border-primary bg-success text-white" @click="isEditingName = false">Save</button>
            </div>
            <div class="d-flex">
                <div style="width: 10rem;">Email</div>
                <input class="border border-secondary rounded px-2" type="text" :disabled="!isEditingEmail" :value="user.email">
                <button v-if="!isEditingEmail" class="rounded mx-2 border-primary bg-primary text-white" @click="isEditingEmail = true"><i class="bi bi-pencil"></i></button>
                <button v-if="isEditingEmail"class="rounded mx-2 px-3 border-primary bg-success text-white" @click="isEditingEmail = false">Save</button>
            </div>
            <div class="d-flex">
                <div style="width: 10rem;">Password</div>
                <input class="border border-secondary rounded px-2" type="text" :disabled="!isEditingPassword" :value="user.password">
                <button v-if="!isEditingPassword" class="rounded mx-2 border-primary bg-primary text-white" @click="isEditingPassword = true"><i class="bi bi-pencil"></i></button>
                <button v-if="isEditingPassword"class="rounded mx-2 px-3 border-primary bg-success text-white" @click="isEditingPassword = false">Save</button>
            </div>
            <div class="d-flex">
                <div style="width: 10rem;">Date of Birth</div>
                <input class="border border-secondary rounded px-2" type="text" :disabled="!isEditingDateOfBirth" :value="user.date_of_birth">
                <button v-if="!isEditingDateOfBirth" class="rounded mx-2 border-primary bg-primary text-white" @click="isEditingDateOfBirth = !isEditingDateOfBirth"><i class="bi bi-pencil"></i></button>
                <button v-if="isEditingDateOfBirth"class="rounded mx-2 px-3 border-primary bg-success text-white" @click="isEditingDateOfBirth = false">Save</button>
            </div>
        </div>
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
  
      interface User {
        profile_picture : string;
        name : string;
        email : string;
        password : string;
        date_of_birth : string;
      }
      
      export default defineComponent({
          data() {
              return {
                  title: "Other Page",
                  user: {
                    // profile_picture : "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649",
                    profile_picture : "",
                    name : "Person McPerson",
                    email : "email@gmail.com",
                    password : "password",
                    date_of_birth : "01/01/2004",
                  } as User,
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
        async mounted() {
            // this.user = data
            // const store = useUserStore()
            // store.saveUser(user_id)
          }
      })
  </script>
  
<style scoped>
</style>
  