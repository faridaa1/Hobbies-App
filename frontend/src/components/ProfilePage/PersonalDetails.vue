<template>
    <div class="fs-4 mt-4 d-flex flex-row border rounded p-3 ps-5 align-items-center gap-5 w-100">
        <div class="d-flex fs-5 gap-4 flex-column align-items-center w-100">
            <div class="">
                <img style="width: 200px; height:200px; object-fit: cover;" class="rounded-circle" :src="user.profile_picture" alt="">
            </div>
            <div class="d-flex align-items-center">
                <input class="w-75 mx-auto" type="file" @change="updateProfilePicture">
            </div>
        </div>
        <div class="d-flex flex-column gap-2 w-100">
            <div class="d-flex">
                <div style="width: 13rem;">Full Name</div>
                <div>{{ user.name }}</div>
                <button><i class="bi bi-pencil"></i></button>
            </div>
            <div class="d-flex">
                <div style="width: 13rem;">Email</div>
                <div>{{ user.email }}</div>
                <button><i class="bi bi-pencil"></i></button>
            </div>
            <div class="d-flex">
                <div style="width: 13rem;">Password</div>
                <div>{{ user.password }}</div>
                <button><i class="bi bi-pencil"></i></button>
            </div>
            <div class="d-flex">
                <div style="width: 13rem;">Date of Birth</div>
                <div>{{ user.date_of_birth }}</div>
                <button><i class="bi bi-pencil"></i></button>
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
                    profile_picture : "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649",
                    name : "Person McPerson",
                    email : "email@gmail.com",
                    password : "password",
                    date_of_birth : "01/01/2004",
                  } as User
              }
          },
          methods: {
            updateProfilePicture(event: Event) {
                const input: HTMLInputElement = event.target as HTMLInputElement
                if (input && input.files && input.files[0]) {
                    this.user.profile_picture = URL.createObjectURL(input.files[0])
                }
            }
        }
          
      })
  </script>
  
  <style scoped>
  </style>
  