<template>
    <div class="fs-3 mt-4 d-flex flex-row border border-dark rounded p-3 ps-5 align-items-center" style="gap: 10rem;">
        <div class="d-flex flex-column gap-4 justify-content-center align-items-center">
            <div>
                <img style="width: 200px; height:200px; object-fit: cover;" class="rounded-circle" :src="user.profile_picture" alt="No Profile Picture">
            </div>
            <div>
                Edit Pictures
                <button class="btn btn-secondary">
                    <i class="bi bi-upload"></i>
                </button>
            </div>
        </div>
        <div class="d-flex flex-column gap-2 w-100">
            <div class="d-flex">
                <div style="width: 13rem;">Full Name</div>
                <div>{{ user.name }}</div>
                <button><i class="bi bi-upload"></i></button>
            </div>
            <div class="d-flex">
                <div style="width: 13rem;">Email</div>
                <div>{{ user.email }}</div>
            </div>
            <div class="d-flex">
                <div style="width: 13rem;">Password</div>
                <div>{{ user.password }}</div>
            </div>
            <div class="d-flex">
                <div style="width: 13rem;">Date of Birth</div>
                <div>{{ user.date_of_birth }}</div>
            </div>
        </div>
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
  
      export default defineComponent({
          data() {
              return {
                  title: "Other Page",
                  user: {
                    "profile_picture" : "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649",
                    "name" : "Person McPerson",
                    "email" : "email@gmail.com",
                    "password" : "password",
                    "date_of_birth" : "01/01/2004",
                  }
              }
          },
          
      })
  </script>
  
  <style scoped>
  </style>
  